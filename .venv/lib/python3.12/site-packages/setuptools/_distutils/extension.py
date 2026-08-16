"""distutils.extension

Provides the Extension class, used to describe C/C++ extension
modules in setup scripts."""

from __future__ import annotations

import os
from collections.abc import Iterable
from dataclasses import field, fields

from ._dataclass import lenient_dataclass

# This class is really only used by the "build_ext" command, so it might
# make sense to put it in distutils.command.build_ext.  However, that
# module is already big enough, and I want to make this class a bit more
# complex to simplify some common cases ("foo" module in "foo.c") and do
# better error-checking ("foo.c" actually exists).
#
# Also, putting this in build_ext.py means every setup script would have to
# import that large-ish module (indirectly, through distutils.core) in
# order to do anything.


@lenient_dataclass()
class Extension:
    """Just a collection of attributes that describes an extension
    module and everything needed to build it (hopefully in a portable
    way, but there are hooks that let you be as unportable as you need).
    """

    name: str
    """
    the full name of the extension, including any packages -- ie.
    *not* a filename or pathname, but Python dotted name
    """

    sources: Iterable[str | os.PathLike[str]]
    """
    iterable of source filenames (except strings, which could be misinterpreted
    as a single filename), relative to the distribution root (where the setup
    script lives), in Unix form (slash-separated) for portability. Can be any
    non-string iterable (list, tuple, set, etc.) containing strings or
    PathLike objects. Source files may be C, C++, SWIG (.i), platform-specific
    resource files, or whatever else is recognized by the "build_ext" command
    as source for a Python extension.
    """

    include_dirs: list[str] = field(default_factory=list)
    """
    list of directories to search for C/C++ header files (in Unix
    form for portability)
    """

    define_macros: list[tuple[str, str | None]] = field(default_factory=list)
    """
    list of macros to define; each macro is defined using a 2-tuple,
    where 'value' is either the string to define it to or None to
    define it without a particular value (equivalent of "#define
    FOO" in source or -DFOO on Unix C compiler command line)
    """

    undef_macros: list[str] = field(default_factory=list)
    """list of macros to undefine explicitly"""

    library_dirs: list[str] = field(default_factory=list)
    """list of directories to search for C/C++ libraries at link time"""

    libraries: list[str] = field(default_factory=list)
    """list of library names (not filenames or paths) to link against"""

    runtime_library_dirs: list[str] = field(default_factory=list)
    """
    list of directories to search for C/C++ libraries at run time
    (for shared extensions, this is when the extension is loaded)
    """

    extra_objects: list[str] = field(default_factory=list)
    """
    list of extra files to link with (eg. object files not implied
    by 'sources', static library that must be explicitly specified,
    binary resource files, etc.)
    """

    extra_compile_args: list[str] = field(default_factory=list)
    """
    any extra platform- and compiler-specific information to use
    when compiling the source files in 'sources'.  For platforms and
    compilers where "command line" makes sense, this is typically a
    list of command-line arguments, but for other platforms it could
    be anything.
    """

    extra_link_args: list[str] = field(default_factory=list)
    """
    any extra platform- and compiler-specific information to use
    when linking object files together to create the extension (or
    to create a new static Python interpreter).  Similar
    interpretation as for 'extra_compile_args'.
    """

    export_symbols: list[str] = field(default_factory=list)
    """
    list of symbols to be exported from a shared extension.  Not
    used on all platforms, and not generally necessary for Python
    extensions, which typically export exactly one symbol: "init" +
    extension_name.
    """

    swig_opts: list[str] = field(default_factory=list)
    """
    any extra options to pass to SWIG if a source file has the .i
    extension.
    """

    depends: list[str] = field(default_factory=list)
    """list of files that the extension depends on"""

    language: str | None = None
    """
    extension language (i.e. "c", "c++", "objc"). Will be detected
    from the source extensions if not provided.
    """

    optional: bool = False
    """
    specifies that a build failure in the extension should not abort the
    build process, but simply not install the failing extension.
    """

    def __post_init__(self):
        if not isinstance(self.name, str):
            raise TypeError("'name' must be a string")

        # handle the string case first; since strings are iterable, disallow them
        if isinstance(self.sources, str):
            raise TypeError(
                "'sources' must be an iterable of strings or PathLike objects, not a string"
            )

        # now we check if it's iterable and contains valid types
        try:
            self.sources = list(map(os.fspath, self.sources))
        except TypeError:
            raise TypeError(
                "'sources' must be an iterable of strings or PathLike objects"
            )


_safe = tuple(f.name for f in fields(Extension))
"""Legal keyword arguments for the Extension constructor."""


def read_setup_file(filename):  # noqa: C901
    """Reads a Setup file and returns Extension instances."""
    from distutils.sysconfig import _variable_rx, expand_makefile_vars, parse_makefile
    from distutils.text_file import TextFile
    from distutils.util import split_quoted

    # First pass over the file to gather "VAR = VALUE" assignments.
    vars = parse_makefile(filename)

    # Second pass to gobble up the real content: lines of the form
    #   <module> ... [<sourcefile> ...] [<cpparg> ...] [<library> ...]
    file = TextFile(
        filename,
        strip_comments=True,
        skip_blanks=True,
        join_lines=True,
        lstrip_ws=True,
        rstrip_ws=True,
    )
    try:
        extensions = []

        while True:
            line = file.readline()
            if line is None:  # eof
                break
            if _variable_rx.match(line):  # VAR=VALUE, handled in first pass
                continue

            if line[0] == line[-1] == "*":
                file.warn(f"'{line}' lines not handled yet")
                continue

            line = expand_makefile_vars(line, vars)
            words = split_quoted(line)

            # NB. this parses a slightly different syntax than the old
            # makesetup script: here, there must be exactly one extension per
            # line, and it must be the first word of the line.  I have no idea
            # why the old syntax supported multiple extensions per line, as
            # they all wind up being the same.

            module = words[0]
            ext = Extension(module, [])
            append_next_word = None

            for word in words[1:]:
                if append_next_word is not None:
                    append_next_word.append(word)
                    append_next_word = None
                    continue

                suffix = os.path.splitext(word)[1]
                switch = word[0:2]
                value = word[2:]

                if suffix in (".c", ".cc", ".cpp", ".cxx", ".c++", ".m", ".mm"):
                    # hmm, should we do something about C vs. C++ sources?
                    # or leave it up to the CCompiler implementation to
                    # worry about?
                    ext.sources.append(word)
                elif switch == "-I":
                    ext.include_dirs.append(value)
                elif switch == "-D":
                    equals = value.find("=")
                    if equals == -1:  # bare "-DFOO" -- no value
                        ext.define_macros.append((value, None))
                    else:  # "-DFOO=blah"
                        ext.define_macros.append((value[0:equals], value[equals + 2 :]))
                elif switch == "-U":
                    ext.undef_macros.append(value)
                elif switch == "-C":  # only here 'cause makesetup has it!
                    ext.extra_compile_args.append(word)
                elif switch == "-l":
                    ext.libraries.append(value)
                elif switch == "-L":
                    ext.library_dirs.append(value)
                elif switch == "-R":
                    ext.runtime_library_dirs.append(value)
                elif word == "-rpath":
                    append_next_word = ext.runtime_library_dirs
                elif word == "-Xlinker":
                    append_next_word = ext.extra_link_args
                elif word == "-Xcompiler":
                    append_next_word = ext.extra_compile_args
                elif switch == "-u":
                    ext.extra_link_args.append(word)
                    if not value:
                        append_next_word = ext.extra_link_args
                elif suffix in (".a", ".so", ".sl", ".o", ".dylib"):
                    # NB. a really faithful emulation of makesetup would
                    # append a .o file to extra_objects only if it
                    # had a slash in it; otherwise, it would s/.o/.c/
                    # and append it to sources.  Hmmmm.
                    ext.extra_objects.append(word)
                else:
                    file.warn(f"unrecognized argument '{word}'")

            extensions.append(ext)
    finally:
        file.close()

    return extensions
