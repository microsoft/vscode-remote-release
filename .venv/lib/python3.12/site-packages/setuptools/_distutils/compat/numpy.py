# required for older numpy versions on Pythons prior to 3.12; see pypa/setuptools#4876
from ..compilers.C.base import _default_compilers  # noqa: F401

# Map compiler short names to (module_name, class_name, description). Retained
# for older numpy, which reads ``distutils.ccompiler.compiler_class``; the
# compilers package itself now discovers compilers via
# ``compilers.C.base.get_compilers()``.
compiler_class = {
    'unix': ('unixccompiler', 'UnixCCompiler', "standard UNIX-style compiler"),
    'msvc': ('_msvccompiler', 'MSVCCompiler', "Microsoft Visual C++"),
    'cygwin': (
        'cygwinccompiler',
        'CygwinCCompiler',
        "Cygwin port of GNU C Compiler for Win32",
    ),
    'mingw32': (
        'cygwinccompiler',
        'Mingw32CCompiler',
        "Mingw32 port of GNU C Compiler for Win32",
    ),
    'bcpp': ('bcppcompiler', 'BCPPCompiler', "Borland C++ Compiler"),
    'zos': ('zosccompiler', 'zOSCCompiler', 'IBM XL C/C++ Compilers'),
}
