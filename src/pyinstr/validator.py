"""
This file is part of PyINSTR.

:copyright: 2025 by Marco Schott.
:license: MIT, see LICENSE for more details.
"""

from collections.abc import Callable
from typing import Any, Protocol, runtime_checkable

from pyinstr.message import Channel, MessageProtocol


@runtime_checkable
class SupportsComparison(Protocol):
    def __lt__[T](self: T, other: T, /) -> bool: ...
    def __le__[T](self: T, other: T, /) -> bool: ...
    def __gt__[T](self: T, other: T, /) -> bool: ...
    def __ge__[T](self: T, other: T, /) -> bool: ...


def in_range[T: SupportsComparison](value_min: T, value_max: T) -> Callable[[Any, T], bool]:
    def wrapper(_: Any, value: T) -> bool:  # noqa: ANN401
        return value >= value_min and value < value_max

    return wrapper


def in_range_inc[T: SupportsComparison](value_min: T, value_max: T) -> Callable[[Any, T], bool]:
    def wrapper(_: Any, value: T) -> bool:  # noqa: ANN401
        return value >= value_min and value <= value_max

    return wrapper


def in_set[T](*values: T) -> Callable[[Any, T], bool]:
    def wrapper(_: Any, value: T) -> bool:  # noqa: ANN401
        return value in values

    return wrapper


def for_channel[C: Channel[MessageProtocol], T](entries: dict[str, Callable[[C, T], bool]]) -> Callable[[C, T], bool]:
    def wrapper(self: C, value: T) -> bool:
        entry = entries.get(self.name, None)
        if entry is None:
            raise ValueError(f'No validator specified for channel {self.name}.')
        return entry(self, value)

    return wrapper
