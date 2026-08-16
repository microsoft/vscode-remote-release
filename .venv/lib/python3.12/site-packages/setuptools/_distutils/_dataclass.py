# This is a private module, but setuptools has the explicit permission to use it.
from __future__ import annotations

import warnings
from dataclasses import dataclass, fields
from functools import wraps
from typing import TypeVar

from .compat.py310 import dataclass_transform

_T = TypeVar("_T", bound=type)


@dataclass_transform()
def lenient_dataclass(**dc_kwargs):
    """
    Build a dataclass whose ``__init__`` ignores unknown keyword arguments.

    Customize ``__init__`` to preserve backwards compatibility and keep
    tolerating arbitrary keywords, but keep the dataclass-generated
    ``__init__`` to avoid redefining the typing for all the arguments.

    Drop this customization once lenient behaviour and backward
    compatibility are no longer needed and use a regular ``dataclass``
    instead.
    """

    @wraps(dataclass)
    def _wrap(cls: _T) -> _T:  # type: ignore[var-annotated]
        cls = dataclass(**dc_kwargs)(cls)
        # Allowed field names in order
        safe = tuple(f.name for f in fields(cls))
        orig_init = cls.__init__

        @wraps(orig_init)
        def _wrapped_init(self, *args, **kwargs):
            extra = {repr(k): kwargs.pop(k) for k in tuple(kwargs) if k not in safe}
            if extra:
                msg = f"""
                Please remove unknown `{cls.__name__}` options: {','.join(extra)}
                this kind of usage is deprecated and may cause errors in the future.
                """
                warnings.warn(msg)

            # Ensure default values (e.g. []) are used instead of None:
            positional = {
                k: v for k, v in zip(safe, args, strict=False) if v is not None
            }
            keywords = {k: v for k, v in kwargs.items() if v is not None}
            return orig_init(self, **positional, **keywords)

        cls.__init__ = _wrapped_init
        return cls

    return _wrap
