from __future__ import annotations

import sys
from collections.abc import Callable
from typing import TYPE_CHECKING, Any, TypeVar

_T = TypeVar("_T")

if sys.version_info >= (3, 11):
    from typing import dataclass_transform
else:
    if TYPE_CHECKING:
        # typing_extensions usually "exist" when type-checking,
        # without the need for extra runtime dependencies
        from typing_extensions import dataclass_transform
    else:
        # Runtime no-op
        def dataclass_transform(  # type: ignore[misc]
            *,
            eq_default: bool | None = None,
            order_default: bool | None = None,
            kw_only_default: bool | None = None,
            field_specifiers: tuple[type[Any], ...] = (),
            **_: Any,
        ) -> Callable[[_T], _T]:
            def _decorator(obj: _T) -> _T:
                return obj

            return _decorator
