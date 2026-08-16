"""distutils.spawn

Provides the 'spawn()' function, a front-end to various platform-
specific functions for launching another program in a sub-process.
"""

from __future__ import annotations

import contextlib
import os
import subprocess
import sys
import warnings
from collections.abc import MutableSequence

from ._log import log
from .errors import DistutilsExecError


@contextlib.contextmanager
def _translate_errors(cmd):
    """Reraise a subprocess failure running 'cmd' as a DistutilsExecError."""
    try:
        yield
    except OSError as exc:
        raise DistutilsExecError(f"command {cmd[0]!r} failed: {exc.args[-1]}") from exc
    except subprocess.CalledProcessError as err:
        raise DistutilsExecError(
            f"command {cmd[0]!r} failed with exit code {err.returncode}"
        ) from err


def spawn(cmd: MutableSequence[bytes | str | os.PathLike[str]], **kwargs) -> None:
    """Run another program, specified as a command list 'cmd', in a new process.

    'cmd' is just the argument list for the new process, ie.
    cmd[0] is the program to run and cmd[1:] are the rest of its arguments.
    Any keyword arguments are passed through to ``subprocess.check_call``.

    Raise DistutilsExecError if running the program fails in any way; just
    return on success.
    """
    log.info(subprocess.list2cmdline(cmd))
    with _translate_errors(cmd):
        subprocess.check_call(cmd, **kwargs)


def find_executable(executable: str, path: str | None = None) -> str | None:
    """Tries to find 'executable' in the directories listed in 'path'.

    A string listing directories separated by 'os.pathsep'; defaults to
    os.environ['PATH'].  Returns the complete filename or None if not found.
    """
    warnings.warn(
        'Use shutil.which instead of find_executable', DeprecationWarning, stacklevel=2
    )
    _, ext = os.path.splitext(executable)
    if (sys.platform == 'win32') and (ext != '.exe'):
        executable = executable + '.exe'

    if os.path.isfile(executable):
        return executable

    if path is None:
        path = os.environ.get('PATH', None)
        # bpo-35755: Don't fall through if PATH is the empty string
        if path is None:
            try:
                path = os.confstr("CS_PATH")
            except (AttributeError, ValueError):
                # os.confstr() or CS_PATH is not available
                path = os.defpath

    # PATH='' doesn't match, whereas PATH=':' looks in the current directory
    if not path:
        return None

    paths = path.split(os.pathsep)
    for p in paths:
        f = os.path.join(p, executable)
        if os.path.isfile(f):
            # the file exists, we have a shot at spawn working
            return f
    return None
