"""Exceptions raised by the C/C++ compilers."""

from ..errors import Error


class PreprocessError(Error):
    """Failure to preprocess one or more C/C++ files."""


class CompileError(Error):
    """Failure to compile one or more C/C++ source files."""


class LibError(Error):
    """Failure to create a static library from one or more C/C++ object
    files."""


class LinkError(Error):
    """Failure to link one or more C/C++ object files into an executable
    or shared library file."""
