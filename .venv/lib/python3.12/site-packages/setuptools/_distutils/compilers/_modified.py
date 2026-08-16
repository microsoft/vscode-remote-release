"""Timestamp comparison of files and groups of files."""

from __future__ import annotations

import os.path
from collections.abc import Iterable
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from typing import TypeAlias

_Path: TypeAlias = "str | bytes | os.PathLike[str] | os.PathLike[bytes]"


def _newer(source, target) -> bool:
    return not os.path.exists(target) or (
        os.path.getmtime(source) > os.path.getmtime(target)
    )


def newer(source: _Path, target: _Path) -> bool:
    """
    Is source modified more recently than target.

    Returns True if 'source' is modified more recently than 'target' or if
    'target' does not exist. Raises FileNotFoundError if 'source' does not
    exist.
    """
    if not os.path.exists(source):
        raise FileNotFoundError(f"file {os.path.abspath(source)!r} does not exist")

    return _newer(source, target)


def newer_group(
    sources: Iterable[_Path],
    target: _Path,
    missing: Literal["error", "ignore", "newer"] = "error",
) -> bool:
    """
    Is target out-of-date with respect to any file in sources.

    Return True if 'target' is out-of-date with respect to any file listed in
    'sources'. In other words, if 'target' exists and is newer than every file
    in 'sources', return False; otherwise return True. ``missing`` controls how
    to handle a missing source file:

    - error (default): allow the ``stat()`` call to fail.
    - ignore: silently disregard any missing source files.
    - newer: treat missing source files as "target out of date".
    """

    def missing_as_newer(source):
        return missing == 'newer' and not os.path.exists(source)

    ignored = os.path.exists if missing == 'ignore' else None
    return not os.path.exists(target) or any(
        missing_as_newer(source) or _newer(source, target)
        for source in filter(ignored, sources)
    )
