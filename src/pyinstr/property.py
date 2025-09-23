"""
This file is part of PyINSTR.

:copyright: 2025 by Marco Schott.
:license: MIT, see LICENSE for more details.
"""

from collections.abc import Callable
from typing import Self, overload


class Property[S, T]:
    """Property class with type-hints, similar to built-in property."""

    def __init__(
        self,
        fget: Callable[[S], T] | None = None,
        fset: Callable[[S, T], None] | None = None,
        fdel: Callable[[S], None] | None = None,
        name: str | None = None,
        doc: str | None = None,
    ) -> None:
        self._fget = fget
        self._fset = fset
        self._fdel = fdel

        self._name = '_unknown_' if name is None else name
        self.__doc__ = doc

    def __set_name__(self, owner: type, name: str) -> None:
        if self._name == '_unknown_':
            self._name = name

    @property
    def name(self) -> str:
        return self._name

    @overload
    def __get__(self, instance: None, owner: type, /) -> Self: ...
    @overload
    def __get__(self, instance: S, owner: type | None = None, /) -> T: ...

    def __get__(self, instance: S | None, owner: type | None = None, /) -> Self | T:
        if instance is None:
            return self
        if self._fget is None:
            raise ValueError(f'Unreadable attribute{self._name}')
        return self._fget(instance)

    def __set__(self, instance: S, value: T, /) -> None:
        if self._fset is None:
            raise ValueError(f"Can't set attribute{self._name}")
        return self._fset(instance, value)

    def __delete__(self, instance: S, /) -> None:
        if self._fdel is None:
            raise ValueError(f"Can't delete attribute{self._name}")
        return self._fdel(instance)
