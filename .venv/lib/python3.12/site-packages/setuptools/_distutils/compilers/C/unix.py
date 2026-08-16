"""distutils.unixccompiler

Contains the UnixCCompiler class, a subclass of CCompiler that handles
the "typical" Unix-style command-line C compiler:
  * macros defined with -Dname[=value]
  * macros undefined with -Uname
  * include search directories specified with -Idir
  * libraries specified with -lllib
  * library search directories specified with -Ldir
  * compile handled by 'cc' (or similar) executable with -c option:
    compiles .c to .o
  * link static library handled by 'ar' command (possibly with 'ranlib')
  * link shared library handled by 'cc -shared'
"""

from __future__ import annotations

import itertools
import os
import re
import shlex
import subprocess
import sys
import sysconfig
from collections.abc import Iterable
from typing import ClassVar

from jaraco.functools import pass_none

from .._modified import newer
from ..logging import get_logger
from ..platform import macos
from ..platform.macos import compiler_fixup
from . import base
from .base import _Macro, gen_lib_options, gen_preprocess_options
from .errors import CompileError, LibError, LinkError

log = get_logger(__name__)


def _require_config_vars(*names):
    values = sysconfig.get_config_vars(*names)
    missing = [
        name for name, value in zip(names, values, strict=False) if value is None
    ]
    assert not missing, f"Unexpected None in config vars: {missing}"
    return values


@pass_none
def _add_flags(value: str, flag_type: str) -> str:
    """Append any ``$<flag_type>FLAGS`` from the environment to ``value``."""
    flags = os.environ.get(f'{flag_type}FLAGS')
    return f'{value} {flags}' if flags else value


# XXX Things not currently handled:
#   * optimization/debug/warning flags; we just use whatever's in Python's
#     Makefile and live with it.  Is this adequate?  If not, we might
#     have to have a bunch of subclasses GNUCCompiler, SGICCompiler,
#     SunCCompiler, and I suspect down that road lies madness.
#   * even if we don't know a warning flag from an optimization flag,
#     we need some way for outsiders to feed preprocessor/compiler/linker
#     flags in to us -- eg. a sysadmin might want to mandate certain flags
#     via a site config file, or a user might want to set something for
#     compiling this module distribution only via the setup.py command
#     line, whatever.  As long as these options come from something on the
#     current system, they can be as system-dependent as they like, and we
#     should just happily stuff them into the preprocessor/compiler/linker
#     options and carry on.


def _split_env(cmd):
    """
    For macOS, split command into 'env' portion (if any)
    and the rest of the linker command.

    >>> _split_env(['a', 'b', 'c'])
    ([], ['a', 'b', 'c'])
    >>> _split_env(['/usr/bin/env', 'A=3', 'gcc'])
    (['/usr/bin/env', 'A=3'], ['gcc'])
    """
    pivot = 0
    if os.path.basename(cmd[0]) == "env":
        pivot = 1
        while '=' in cmd[pivot]:
            pivot += 1
    return cmd[:pivot], cmd[pivot:]


def _split_aix(cmd):
    """
    AIX platforms prefix the compiler with the ld_so_aix
    script, so split that from the linker command.

    >>> _split_aix(['a', 'b', 'c'])
    ([], ['a', 'b', 'c'])
    >>> _split_aix(['/bin/foo/ld_so_aix', 'gcc'])
    (['/bin/foo/ld_so_aix'], ['gcc'])
    """
    pivot = os.path.basename(cmd[0]) == 'ld_so_aix'
    return cmd[:pivot], cmd[pivot:]


def _linker_params(linker_cmd, compiler_cmd):
    """
    The linker command usually begins with the compiler
    command (possibly multiple elements), followed by zero or more
    params for shared library building.

    If the LDSHARED env variable overrides the linker command,
    however, the commands may not match.

    Return the best guess of the linker parameters by stripping
    the linker command. If the compiler command does not
    match the linker command, assume the linker command is
    just the first element.

    >>> _linker_params('gcc foo bar'.split(), ['gcc'])
    ['foo', 'bar']
    >>> _linker_params('gcc foo bar'.split(), ['other'])
    ['foo', 'bar']
    >>> _linker_params('ccache gcc foo bar'.split(), 'ccache gcc'.split())
    ['foo', 'bar']
    >>> _linker_params(['gcc'], ['gcc'])
    []
    """
    c_len = len(compiler_cmd)
    pivot = c_len if linker_cmd[:c_len] == compiler_cmd else 1
    return linker_cmd[pivot:]


class Compiler(base.Compiler):
    compiler_type = 'unix'
    description = "standard UNIX-style compiler"

    # These are used by CCompiler in two places: the constructor sets
    # instance attributes 'preprocessor', 'compiler', etc. from them, and
    # 'set_executable()' allows any of these to be set.  The defaults here
    # are pretty generic; they will probably have to be set by an outsider
    # (eg. using information discovered by the sysconfig about building
    # Python extensions).
    executables: ClassVar[dict] = {
        'preprocessor': None,
        'compiler': ["cc"],
        'compiler_so': ["cc"],
        'compiler_cxx': ["c++"],
        'compiler_so_cxx': ["c++"],
        'linker_so': ["cc", "-shared"],
        'linker_so_cxx': ["c++", "-shared"],
        'linker_exe': ["cc"],
        'linker_exe_cxx': ["c++", "-shared"],
        'archiver': ["ar", "-cr"],
        'ranlib': None,
    }

    if sys.platform[:6] == "darwin":
        executables['ranlib'] = ["ranlib"]

    # Needed for the filename generation methods provided by the base
    # class, CCompiler.  NB. whoever instantiates/uses a particular
    # UnixCCompiler instance should set 'shared_lib_ext' -- we set a
    # reasonable common default here, but it's not necessarily used on all
    # Unices!

    src_extensions: ClassVar[list[str] | None] = [
        ".c",
        ".C",
        ".cc",
        ".cxx",
        ".cpp",
        ".m",
    ]
    obj_extension = ".o"
    static_lib_extension = ".a"
    shared_lib_extension = ".so"
    dylib_lib_extension = ".dylib"
    xcode_stub_lib_extension = ".tbd"
    static_lib_format = shared_lib_format = dylib_lib_format = "lib%s%s"
    xcode_stub_lib_format = dylib_lib_format
    if sys.platform == "cygwin":
        exe_extension = ".exe"
        shared_lib_extension = ".dll.a"
        dylib_lib_extension = ".dll"
        dylib_lib_format = "cyg%s%s"

    def configure_system(self) -> None:
        """Configure this compiler from the interpreter's build configuration.

        Applies the compiler, flag, and archiver settings CPython recorded in
        sysconfig when it was built -- honoring the usual environment-variable
        overrides (CC, CXX, CFLAGS, LDSHARED, AR, RANLIB, …) -- so extensions
        build consistently with the interpreter.
        """
        macos.customize_compiler(sysconfig.get_config_vars())

        (
            cc,
            cxx,
            cflags,
            ccshared,
            ldshared,
            ldcxxshared,
            shlib_suffix,
            ar,
            ar_flags,
        ) = _require_config_vars(
            'CC',
            'CXX',
            'CFLAGS',
            'CCSHARED',
            'LDSHARED',
            'LDCXXSHARED',
            'SHLIB_SUFFIX',
            'AR',
            'ARFLAGS',
        )

        cxxflags = cflags

        if 'CC' in os.environ:
            newcc = os.environ['CC']
            if 'LDSHARED' not in os.environ and ldshared.startswith(cc):
                # If CC is overridden, use that as the default command for
                # LDSHARED as well.
                ldshared = newcc + ldshared[len(cc) :]
            cc = newcc
        cxx = os.environ.get('CXX', cxx)
        ldshared = os.environ.get('LDSHARED', ldshared)
        ldcxxshared = os.environ.get('LDCXXSHARED', ldcxxshared)
        cpp = os.environ.get('CPP', cc + " -E")

        ldshared = _add_flags(ldshared, 'LD')
        ldcxxshared = _add_flags(ldcxxshared, 'LD')
        cflags = os.environ.get('CFLAGS', cflags)
        ldshared = _add_flags(ldshared, 'C')
        cxxflags = os.environ.get('CXXFLAGS', cxxflags)
        ldcxxshared = _add_flags(ldcxxshared, 'CXX')
        cpp = _add_flags(cpp, 'CPP')
        cflags = _add_flags(cflags, 'CPP')
        cxxflags = _add_flags(cxxflags, 'CPP')
        ldshared = _add_flags(ldshared, 'CPP')
        ldcxxshared = _add_flags(ldcxxshared, 'CPP')

        ar = os.environ.get('AR', ar)

        archiver = ar + ' ' + os.environ.get('ARFLAGS', ar_flags)
        cc_cmd = cc + ' ' + cflags
        cxx_cmd = cxx + ' ' + cxxflags

        self.set_executables(
            preprocessor=cpp,
            compiler=cc_cmd,
            compiler_so=cc_cmd + ' ' + ccshared,
            compiler_cxx=cxx_cmd,
            compiler_so_cxx=cxx_cmd + ' ' + ccshared,
            linker_so=ldshared,
            linker_so_cxx=ldcxxshared,
            linker_exe=cc,
            linker_exe_cxx=cxx,
            archiver=archiver,
        )

        if 'RANLIB' in os.environ and self.executables.get('ranlib', None):
            self.set_executables(ranlib=os.environ['RANLIB'])

        self.shared_lib_extension = shlib_suffix  # type: ignore[misc] # Assigning to ClassVar

    def _fix_lib_args(self, libraries, library_dirs, runtime_library_dirs):
        """Remove standard library path from rpath"""
        libraries, library_dirs, runtime_library_dirs = super()._fix_lib_args(
            libraries, library_dirs, runtime_library_dirs
        )
        libdir = sysconfig.get_config_var('LIBDIR')
        if (
            runtime_library_dirs
            and libdir.startswith("/usr/lib")
            and (libdir in runtime_library_dirs)
        ):
            runtime_library_dirs.remove(libdir)
        return libraries, library_dirs, runtime_library_dirs

    def preprocess(
        self,
        source: str | os.PathLike[str],
        output_file: str | os.PathLike[str] | None = None,
        macros: list[_Macro] | None = None,
        include_dirs: list[str] | tuple[str, ...] | None = None,
        extra_preargs: list[str] | None = None,
        extra_postargs: Iterable[str] | None = None,
    ):
        fixed_args = self._fix_compile_args(None, macros, include_dirs)
        _ignore, macros, include_dirs = fixed_args
        pp_opts = gen_preprocess_options(macros, include_dirs)
        pp_args = self.preprocessor + pp_opts
        if output_file:
            pp_args.extend(['-o', output_file])
        if extra_preargs:
            pp_args[:0] = extra_preargs
        if extra_postargs:
            pp_args.extend(extra_postargs)
        pp_args.append(source)

        # reasons to preprocess:
        # - force is indicated
        # - output is directed to stdout
        # - source file is newer than the target
        preprocess = self.force or output_file is None or newer(source, output_file)
        if not preprocess:
            return

        if output_file:
            self.mkpath(os.path.dirname(output_file))

        try:
            self.call(pp_args)
        except (subprocess.CalledProcessError, OSError) as msg:
            raise CompileError(msg)

    def _compile(self, obj, src, ext, cc_args, extra_postargs, pp_opts):
        compiler_so = compiler_fixup(self.compiler_so, cc_args + extra_postargs)
        compiler_so_cxx = compiler_fixup(self.compiler_so_cxx, cc_args + extra_postargs)
        try:
            if self.detect_language(src) == 'c++':
                self.call(compiler_so_cxx + cc_args + [src, '-o', obj] + extra_postargs)
            else:
                self.call(compiler_so + cc_args + [src, '-o', obj] + extra_postargs)
        except (subprocess.CalledProcessError, OSError) as msg:
            raise CompileError(msg)

    def create_static_lib(
        self, objects, output_libname, output_dir=None, debug=False, target_lang=None
    ):
        objects, output_dir = self._fix_object_args(objects, output_dir)

        output_filename = self.library_filename(output_libname, output_dir=output_dir)

        if self._need_link(objects, output_filename):
            self.mkpath(os.path.dirname(output_filename))
            self.call(self.archiver + [output_filename] + objects + self.objects)

            # Not many Unices required ranlib anymore -- SunOS 4.x is, I
            # think the only major Unix that does.  Maybe we need some
            # platform intelligence here to skip ranlib if it's not
            # needed -- or maybe Python's configure script took care of
            # it for us, hence the check for leading colon.
            if self.ranlib:
                try:
                    self.call(self.ranlib + [output_filename])
                except (subprocess.CalledProcessError, OSError) as msg:
                    raise LibError(msg)
        else:
            log.debug("skipping %s (up-to-date)", output_filename)

    def link(
        self,
        target_desc,
        objects: list[str] | tuple[str, ...],
        output_filename,
        output_dir: str | None = None,
        libraries: list[str] | tuple[str, ...] | None = None,
        library_dirs: list[str] | tuple[str, ...] | None = None,
        runtime_library_dirs: list[str] | tuple[str, ...] | None = None,
        export_symbols=None,
        debug=False,
        extra_preargs=None,
        extra_postargs=None,
        build_temp=None,
        target_lang=None,
    ):
        objects, output_dir = self._fix_object_args(objects, output_dir)
        fixed_args = self._fix_lib_args(libraries, library_dirs, runtime_library_dirs)
        libraries, library_dirs, runtime_library_dirs = fixed_args

        lib_opts = gen_lib_options(self, library_dirs, runtime_library_dirs, libraries)
        if not isinstance(output_dir, (str, type(None))):
            raise TypeError("'output_dir' must be a string or None")
        if output_dir is not None:
            output_filename = os.path.join(output_dir, output_filename)

        if self._need_link(objects, output_filename):
            ld_args = objects + self.objects + lib_opts + ['-o', output_filename]
            if debug:
                ld_args[:0] = ['-g']
            if extra_preargs:
                ld_args[:0] = extra_preargs
            if extra_postargs:
                ld_args.extend(extra_postargs)
            self.mkpath(os.path.dirname(output_filename))
            try:
                # Select a linker based on context: linker_exe when
                # building an executable or linker_so (with shared options)
                # when building a shared library.
                building_exe = target_desc == base.Compiler.EXECUTABLE
                target_cxx = target_lang == "c++"
                linker = (
                    (self.linker_exe_cxx if target_cxx else self.linker_exe)
                    if building_exe
                    else (self.linker_so_cxx if target_cxx else self.linker_so)
                )[:]

                if target_cxx and self.compiler_cxx:
                    env, linker_ne = _split_env(linker)
                    aix, linker_na = _split_aix(linker_ne)
                    _, compiler_cxx_ne = _split_env(self.compiler_cxx)
                    _, linker_exe_ne = _split_env(self.linker_exe_cxx)

                    params = _linker_params(linker_na, linker_exe_ne)
                    linker = env + aix + compiler_cxx_ne + params

                linker = compiler_fixup(linker, ld_args)

                self.call(linker + ld_args)
            except (subprocess.CalledProcessError, OSError) as msg:
                raise LinkError(msg)
        else:
            log.debug("skipping %s (up-to-date)", output_filename)

    # -- Miscellaneous methods -----------------------------------------
    # These are all used by the 'gen_lib_options() function, in
    # ccompiler.py.

    def library_dir_option(self, dir):
        return "-L" + dir

    def _is_gcc(self):
        cc_var = sysconfig.get_config_var("CC")
        compiler = os.path.basename(shlex.split(cc_var)[0])
        return "gcc" in compiler or "g++" in compiler

    def runtime_library_dir_option(self, dir: str) -> str | list[str]:
        # XXX Hackish, at the very least.  See Python bug #445902:
        # https://bugs.python.org/issue445902
        # Linkers on different platforms need different options to
        # specify that directories need to be added to the list of
        # directories searched for dependencies when a dynamic library
        # is sought.  GCC on GNU systems (Linux, FreeBSD, ...) has to
        # be told to pass the -R option through to the linker, whereas
        # other compilers and gcc on other systems just know this.
        # Other compilers may need something slightly different.  At
        # this time, there's no way to determine this information from
        # the configuration data stored in the Python installation, so
        # we use this hack.
        if sys.platform[:6] == "darwin":
            from ..platform import macos

            target_ver = macos.target_ver()
            if target_ver and [int(n) for n in target_ver.split('.')] >= [10, 5]:
                return "-Wl,-rpath," + dir
            else:  # no support for -rpath on earlier macOS versions
                return "-L" + dir
        elif sys.platform[:7] == "freebsd":
            return "-Wl,-rpath=" + dir
        elif sys.platform[:5] == "hp-ux":
            return [
                "-Wl,+s" if self._is_gcc() else "+s",
                "-L" + dir,
            ]

        # For all compilers, `-Wl` is the presumed way to pass a
        # compiler option to the linker
        if sysconfig.get_config_var("GNULD") == "yes":
            return [
                # Force RUNPATH instead of RPATH
                "-Wl,--enable-new-dtags",
                "-Wl,-rpath," + dir,
            ]
        else:
            return "-Wl,-R" + dir

    def library_option(self, lib):
        return "-l" + lib

    @staticmethod
    def _library_root(dir):
        """
        macOS users can specify an alternate SDK using'-isysroot'.
        Calculate the SDK root if it is specified.

        Note that, as of Xcode 7, Apple SDKs may contain textual stub
        libraries with .tbd extensions rather than the normal .dylib
        shared libraries installed in /.  The Apple compiler tool
        chain handles this transparently but it can cause problems
        for programs that are being built with an SDK and searching
        for specific libraries.  Callers of find_library_file need to
        keep in mind that the base filename of the returned SDK library
        file might have a different extension from that of the library
        file installed on the running system, for example:
          /Applications/Xcode.app/Contents/Developer/Platforms/
              MacOSX.platform/Developer/SDKs/MacOSX10.11.sdk/
              usr/lib/libedit.tbd
        vs
          /usr/lib/libedit.dylib
        """
        cflags = sysconfig.get_config_var('CFLAGS')
        match = re.search(r'-isysroot\s*(\S+)', cflags)

        apply_root = (
            sys.platform == 'darwin'
            and match
            and (
                dir.startswith('/System/')
                or (dir.startswith('/usr/') and not dir.startswith('/usr/local/'))
            )
        )

        return os.path.join(match.group(1), dir[1:]) if apply_root else dir

    def find_library_file(self, dirs, lib, debug=False):
        """
        Second-guess the linker with not much hard
        data to go on: GCC seems to prefer the shared library, so
        assume that *all* Unix C compilers do,
        ignoring even GCC's "-static" option.
        """
        lib_names = (
            self.library_filename(lib, lib_type=type)
            for type in ('dylib', 'xcode_stub', 'shared', 'static')
        )

        roots = map(self._library_root, dirs)

        searched = itertools.starmap(os.path.join, itertools.product(roots, lib_names))

        found = filter(os.path.exists, searched)

        # Return None if it could not be found in any dir.
        return next(found, None)
