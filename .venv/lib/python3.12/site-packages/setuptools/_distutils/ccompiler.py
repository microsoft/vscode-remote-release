from .compat.numpy import (  # noqa: F401
    _default_compilers,
    compiler_class,
)
from .compilers.C import base
from .compilers.C.base import (
    gen_lib_options,
    gen_preprocess_options,
    get_compilers,
    get_default_compiler,
    new_compiler,
)
from .compilers.C.errors import CompileError, LinkError

__all__ = [
    'CompileError',
    'LinkError',
    'gen_lib_options',
    'gen_preprocess_options',
    'get_default_compiler',
    'new_compiler',
    'show_compilers',
]


CCompiler = base.Compiler


def show_compilers() -> None:
    """Print list of available compilers (used by the "--help-compiler"
    options to "build", "build_ext", "build_clib").
    """
    # XXX this "knows" that the compiler option it's describing is
    # "--compiler", which just happens to be the case for the three
    # commands that use it.
    from .fancy_getopt import FancyGetopt

    compilers = sorted(
        ("compiler=" + name, None, cls.description)
        for name, cls in get_compilers().items()
    )
    FancyGetopt(compilers).print_help("List of available compilers:")
