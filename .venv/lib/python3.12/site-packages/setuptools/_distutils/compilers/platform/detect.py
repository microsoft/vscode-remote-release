"""Platform identification used to select and configure compilers."""

from __future__ import annotations

import os
import sys
import sysconfig


def get_host_platform() -> str:
    """A string identifying the platform the build is running on."""
    return sysconfig.get_platform()


def get_platform() -> str:
    """The platform being built for.

    Matches :func:`get_host_platform` except on Windows, where the MSVC
    target architecture (``VSCMD_ARG_TGT_ARCH``) takes precedence to support
    cross-compilation.
    """
    if os.name == 'nt':
        TARGET_TO_PLAT = {
            'x86': 'win32',
            'x64': 'win-amd64',
            'arm': 'win-arm32',
            'arm64': 'win-arm64',
        }
        target = os.environ.get('VSCMD_ARG_TGT_ARCH')
        return TARGET_TO_PLAT.get(target) or get_host_platform()
    return get_host_platform()


def is_mingw() -> bool:
    """Whether the current platform is mingw.

    Python compiled with Mingw-w64 has ``sys.platform == 'win32'`` and
    ``get_platform()`` starts with ``'mingw'``.
    """
    return sys.platform == 'win32' and get_platform().startswith('mingw')
