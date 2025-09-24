"""
This file is part of PyINSTR.

:copyright: 2025 by Marco Schott.
:license: MIT, see LICENSE for more details.
"""

from collections.abc import Callable, Container
from typing import Protocol, runtime_checkable


@runtime_checkable
class SupportsComparison(Protocol):
    def __lt__[T](self: T, other: T, /) -> bool: ...
    def __le__[T](self: T, other: T, /) -> bool: ...
    def __gt__[T](self: T, other: T, /) -> bool: ...
    def __ge__[T](self: T, other: T, /) -> bool: ...


def in_range[T: SupportsComparison](value_min: T, value_max: T) -> Callable[[T], bool]:
    def wrapper(value: T) -> bool:
        return value >= value_min and value < value_max

    return wrapper


def in_range_inc[T: SupportsComparison](value_min: T, value_max: T) -> Callable[[T], bool]:
    def wrapper(value: T) -> bool:
        return value >= value_min and value <= value_max

    return wrapper


def in_set[T](values: Container[T]) -> Callable[[T], bool]:
    def wrapper(value: T) -> bool:
        return value in values

    return wrapper
