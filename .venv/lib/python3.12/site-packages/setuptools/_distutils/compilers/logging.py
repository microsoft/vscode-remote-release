import logging


def get_logger(name: str) -> logging.Logger:
    """
    Return a logger whose name is stable across this package's import
    location, which migrates over time (``distutils.compilers.C`` now,
    ``setuptools._distutils.compilers.C`` when vendored, and eventually a
    standalone ``compilers.C``).

    Pass ``__name__``; everything before ``compilers.`` is stripped.

    >>> get_logger('distutils.compilers.C.base').name
    'compilers.C.base'
    >>> get_logger('setuptools._distutils.compilers.C.msvc').name
    'compilers.C.msvc'
    >>> get_logger('compilers.C.unix').name
    'compilers.C.unix'
    """
    stable_name = 'compilers.' + name.split('compilers.', 1)[1]
    return logging.getLogger(stable_name)
