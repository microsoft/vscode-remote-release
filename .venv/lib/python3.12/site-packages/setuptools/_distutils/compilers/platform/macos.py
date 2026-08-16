"""macOS-specific compiler support."""

from __future__ import annotations

import os
import platform
import sys
import sysconfig
from collections.abc import Mapping
from typing import TypeVar

from ..errors import PlatformError

_MappingT = TypeVar("_MappingT", bound=Mapping)

VERSION_VAR = 'MACOSX_DEPLOYMENT_TARGET'

if sys.platform == 'darwin':
    from _osx_support import compiler_fixup
else:

    def compiler_fixup(compiler_so, cc_args):
        """Off macOS there's nothing to fix up."""
        return compiler_so


def customize_compiler(config_vars) -> None:
    """Apply macOS SDK/architecture fixups to build config vars, in place.

    A no-op off macOS. Mirrors distutils' historical ``_customize_macos`` to
    support interpreters from binary installers, where the user's build tools
    and OS version may differ from the system Python itself was built on.
    """
    if sys.platform == 'darwin':
        import _osx_support

        _osx_support.customize_compiler(config_vars)


_syscfg_target_ver = None


def _clear_cached_target_ver():
    """For testing only. Do not call."""
    global _syscfg_target_ver
    _syscfg_target_ver = None


def _target_ver_from_syscfg():
    """The deployment target latched into the interpreter's configuration."""
    global _syscfg_target_ver
    if _syscfg_target_ver is None:
        _syscfg_target_ver = sysconfig.get_config_var(VERSION_VAR) or ''
    return _syscfg_target_ver


def _split_version(s: str) -> list[int]:
    return [int(n) for n in s.split('.')]


def target_ver() -> str | None:
    """Return the version of macOS for which we are building.

    Defaults to the version latched in sysconfig when the interpreter was
    built, unless overridden by ``MACOSX_DEPLOYMENT_TARGET``. Returns None if
    neither source has a value.
    """
    syscfg_ver = _target_ver_from_syscfg()
    env_ver = os.environ.get(VERSION_VAR)

    if env_ver:
        # An override below 10.3 while the interpreter was configured for 10.3+
        # would build extensions with an LDSHARED that uses
        # '-undefined dynamic_lookup', which only works on >= 10.3.
        if (
            syscfg_ver
            and _split_version(syscfg_ver) >= [10, 3]
            and _split_version(env_ver) < [10, 3]
        ):
            raise PlatformError(
                f'${VERSION_VAR} mismatch: now "{env_ver}" but "{syscfg_ver}" '
                'during configure; must use 10.3 or later'
            )
        return env_ver
    return syscfg_ver or None


def inject_ver(env: _MappingT | None) -> _MappingT | dict[str, str | int] | None:
    """
    Ensure a subprocess inherits the deployment target the build was
    configured with, so extensions link against a consistent macOS version.
    """
    if platform.system() != 'Darwin':
        return env

    ver = target_ver()
    update = {VERSION_VAR: ver} if ver else {}
    resolved = os.environ if env is None else env
    return {**resolved, **update}
