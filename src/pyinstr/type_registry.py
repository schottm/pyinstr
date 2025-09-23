"""
This file is part of PyINSTR.

:copyright: 2025 by Marco Schott.
:license: MIT, see LICENSE for more details.
"""

import inspect
from collections.abc import Callable
from typing import Any, overload, override


class TypeRegistry[V]:
    def __init__(self) -> None:
        self._registry: dict[type, V] = {}

    def register(self, type_: type, value: V) -> None:
        self._registry[type_] = value

    def get(self, type_: type) -> V:
        # Find closest registered superclass
        candidates = [typ for typ in self._registry if issubclass(type_, typ)]
        if not candidates:
            raise KeyError(f'No registration for type {type_}')
        closest = min(candidates, key=lambda typ: self._type_distance(type_, typ))
        return self._registry[closest]

    @staticmethod
    def _type_distance(child: type, parent: type) -> int | float:
        try:
            return inspect.getmro(child).index(parent)
        except ValueError:
            return float('inf')


class CallableTypeRegistry[I](TypeRegistry[Callable[[type, I], Any]]):
    @overload
    def register[T](self, type_: type[T], value: Callable[[type[T], I], T]) -> None: ...
    @overload
    def register[T](
        self, type_: type[T]
    ) -> Callable[[Callable[[type[T], I], T]], None]: ...

    @override
    def register[T](
        self, type_: type[T], value: Callable[[type[T], I], T] | None = None
    ) -> Callable[[Callable[[type[T], I], T]], None] | None:
        if value is None:

            def decorator(other: Callable[[type[T], I], T]) -> None:
                super(CallableTypeRegistry, self).register(type_, other)

            return decorator
        super().register(type_, value)

    @override
    def get[T](self, type_: type[T]) -> Callable[[type[T], I], T]:
        return super().get(type_)


class DefaultTypeRegistry(TypeRegistry[Callable[[type], Any]]):
    def __init__(self) -> None:
        super().__init__()
        self._defaults: dict[type, Any] = {}

    @overload
    def register[T](
        self, type_: type[T], value: T | Callable[[type[T]], T]
    ) -> None: ...
    @overload
    def register[T](
        self, type_: type[T]
    ) -> Callable[[Callable[[type[T]], T]], None]: ...

    @override
    def register[T](
        self, type_: type[T], value: T | Callable[[type[T]], T] | None = None
    ) -> Callable[[Callable[[type[T]], T]], None] | None:
        if value is None:

            def decorator(other: Callable[[type[T]], T]) -> None:
                super(DefaultTypeRegistry, self).register(type_, other)

            return decorator
        elif isinstance(value, type_):
            super().register(type_, lambda _: value)
        elif callable(value):
            super().register(type_, value)
        else:
            raise ValueError('Something unexpected happended!')

    @override
    def get[T](self, type_: type[T]) -> T:
        if type_ in self._defaults:
            return self._defaults[type_]
        factory = super().get(type_)
        value = factory(type_)
        self._defaults[type_] = value
        return value
