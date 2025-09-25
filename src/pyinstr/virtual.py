"""
This file is part of PyINSTR.

:copyright: 2025 by Marco Schott.
:license: MIT, see LICENSE for more details.
"""

import copy
from enum import IntFlag, StrEnum
from typing import Any

from pyinstr.adapters import NullAdapter
from pyinstr.control import ControlProperty
from pyinstr.message import (
    Channel,
    ChannelProperty,
    Instrument,
    MessageProtocol,
)
from pyinstr.property import Property
from pyinstr.type_registry import DefaultTypeRegistry

default_registry = DefaultTypeRegistry()
default_registry.register(int, 0)
default_registry.register(float, 0.0)
default_registry.register(str, '')
default_registry.register(bool, False)
default_registry.register(StrEnum, lambda type_: next(iter(type_)))
default_registry.register(IntFlag, lambda type_: type_(0))

_VIRTUAL = '__virtual_instrument__'


def _deepcopy_properties[T](cls: type[T]) -> dict[str, Any]:
    attrs: dict[str, Any] = {}

    # adding attributes of all mro subclasses overwrites all properties
    for base in cls.__mro__:
        if base is object:
            continue
        for key, value in base.__dict__.items():
            if key not in attrs and isinstance(value, Property):
                attrs[key] = copy.deepcopy(value)  # type: ignore[reportUnknownArgumentType]
    return attrs


def _duplicate_class[T](cls: type[T]) -> type[T]:
    return type(cls.__name__, (cls,), _deepcopy_properties(cls))  # type: ignore[reportReturnType]


def _make_virtual_class[T: MessageProtocol](cls: type[T], defaults: dict[str, Any] | None) -> type[T]:
    # create a deep copy of the class to allow injection into properties
    new_cls = _duplicate_class(cls)
    setattr(new_cls, _VIRTUAL, True)
    _replace_properties(new_cls, defaults)
    return new_cls


def _inject_control_property[T](prop: ControlProperty[MessageProtocol, T], default: T | None) -> None:
    if default is not None and not isinstance(default, prop._type_):  # type: ignore[reportPrivateUsage]
        raise ValueError(
            f"""Default value {default} for {prop.name} is not of required
            type {prop._type_}."""  # type: ignore[reportPrivateUsage]
        )

    def _getter(self: MessageProtocol) -> T:
        attr_id = f'_{prop.name}'
        if not hasattr(self, attr_id):
            setattr(
                self,
                attr_id,
                default if default is not None else default_registry.get(prop._type_),  # type: ignore[reportPrivateUsage]
            )
        return getattr(self, attr_id)

    def _setter(self: MessageProtocol, value: T) -> None:
        attr_id = f'_{prop.name}'
        setattr(self, attr_id, value)

    def _deleter(self: MessageProtocol) -> None:
        attr_id = f'_{prop.name}'
        delattr(self, attr_id)

    prop._fget = _getter  # type: ignore[reportPrivateUsage]
    prop._fset = _setter  # type: ignore[reportPrivateUsage]
    prop._fdel = _deleter  # type: ignore[reportPrivateUsage]


def _inject_channel_property[B: MessageProtocol, T: Channel[MessageProtocol], R](
    prop: ChannelProperty[B, T, R], defaults: dict[str, Any] | None
) -> None:
    prop.factory.type_ = _make_virtual_class(prop.factory.type_, defaults)


def _replace_properties[T: MessageProtocol](cls: type[T], defaults: dict[str, Any] | None) -> None:
    for name, val in vars(cls).items():
        if name.startswith('__') or callable(name):
            continue
        if isinstance(val, ControlProperty):
            _inject_control_property(
                val,  # type: ignore[reportUnknownArgumentType]
                None if defaults is None else defaults.get(name),
            )
        elif isinstance(val, ChannelProperty):
            _inject_channel_property(
                val,  # type: ignore[reportUnknownArgumentType]
                None if defaults is None else defaults.get(name),
            )
        elif isinstance(val, Property):
            raise ValueError('Unkown property defined in instrument.')


def make_virtual[T: Instrument](cls: type[T], defaults: dict[str, Any] | None = None) -> T:
    virtual_cls = _make_virtual_class(cls, defaults)

    return virtual_cls(NullAdapter(), False)


def is_virtual(obj: object) -> bool:
    cls = obj if isinstance(obj, type) else type(obj)
    return hasattr(cls, _VIRTUAL)
