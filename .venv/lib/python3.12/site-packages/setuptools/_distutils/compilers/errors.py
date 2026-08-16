"""Language-agnostic compiler exceptions."""


class Error(Exception):
    """A compiler operation failed."""


class UnknownFileType(Error):
    """Attempt to process an unknown file type."""


class PlatformError(Error):
    """A compiler operation isn't supported on the current platform."""
