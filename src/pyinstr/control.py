"""
This file is part of PyINSTR.

:copyright: 2025 by Marco Schott.
:license: MIT, see LICENSE for more details.
"""

from collections.abc import Callable
from enum import Enum, IntFlag, StrEnum
from typing import Any

from pyinstr.message import MessageProtocol
from pyinstr.property import Property
from pyinstr.type_registry import CallableTypeRegistry

convert_registry = CallableTypeRegistry[str]()

convert_registry.register(str, lambda _, value: value)
convert_registry.register(int, lambda _, value: int(value))
convert_registry.register(float, lambda _, value: float(value))
convert_registry.register(bool, lambda _, value: value.lower() in ['true', '1', 'on', 't', 'y', 'yes'])


@convert_registry.register(StrEnum)
def _string_to_enum(type_: type[StrEnum], value: str) -> StrEnum:
    for key in type_:
        if value == key.value:
            return key
    raise KeyError(f'Value {input} not found in mapped values')


@convert_registry.register(IntFlag)
def _string_to_flag(type_: type[IntFlag], value: str) -> IntFlag:
    return type_(int(value))


class ControlProperty[S, T](Property[S, T]):
    """Attribute property class with types and assigned name."""

    def __init__(
        self,
        type_: type[T],
        fget: Callable[[S], T] | None = None,
        fset: Callable[[S, T], None] | None = None,
        fdel: Callable[[S], None] | None = None,
        name: str | None = None,
        doc: str | None = None,
    ) -> None:
        self._type_ = type_
        super().__init__(fget=fget, fset=fset, fdel=fdel, name=name, doc=doc)


def instance_control[S: MessageProtocol, T](
    type_: type[T],
    doc: str,
    get_cmd: str | None = None,
    set_cmd: str | None = None,
    /,
    get_format: Callable[[str], T] | None = None,
    set_format: Callable[[T], Any] | None = None,
    pre_format: Callable[[str], str] | None = None,
    validate: Callable[[S, T], bool] | None = None,
    response: Callable[[str], None] | None = None,
) -> Property[S, T]:
    if get_cmd is None and set_cmd is None:
        raise ValueError('No commands specified.')
    if get_format is None:
        convert = convert_registry.get(type_)

        def nget_format(value: str) -> T:
            return convert(type_, value)

        get_format = nget_format

    def _getter(self: S) -> T:
        if get_cmd is None:
            raise ValueError('Cannot get value without command!')
        result = self.query(get_cmd)
        if pre_format is not None:
            result = pre_format(result)
        return get_format(result)

    def _setter(self: S, value: T) -> None:
        if set_cmd is None:
            raise ValueError('Cannot set value without command!')
        if not isinstance(value, type_):
            raise ValueError(f'{value} is not of type {type_}.')
        if validate is not None:
            if not validate(self, value):
                raise ValueError('Invalid value given!')
        proc_value = value if set_format is None else set_format(value)
        command = set_cmd % proc_value
        if response is None:
            self.send(command)
        else:
            result = self.query(command)
            if pre_format is not None:
                result = pre_format(result)
            response(result)

    def _deleter(self: S) -> None:
        pass

    return ControlProperty[S, T](
        type_=type_,
        fget=None if get_cmd is None else _getter,
        fset=None if set_cmd is None else _setter,
        fdel=_deleter,
        doc=doc,
    )


def basic_control[T](
    type_: type[T],
    doc: str,
    get_cmd: str | None = None,
    set_cmd: str | None = None,
    /,
    get_format: Callable[[str], T] | None = None,
    set_format: Callable[[T], Any] | None = None,
    pre_format: Callable[[str], str] | None = None,
    validate: Callable[[T], bool] | None = None,
    response: Callable[[str], None] | None = None,
) -> Property[MessageProtocol, T]:
    return instance_control(
        type_,
        doc,
        get_cmd,
        set_cmd,
        get_format=get_format,
        set_format=set_format,
        pre_format=pre_format,
        validate=None if validate is None else (lambda _, t: validate(t)),
        response=response,
    )


class BoolFormat(Enum):
    Default = ('true', 'false')
    DefaultShort = ('t', 'f')
    YesNo = ('yes', 'no')
    YesNoShort = ('y', 'n')
    OnOff = ('on', 'off')
    OneZero = ('1', '0')

    def to_bool(self, value: str) -> bool:
        if value.lower() == self.value[0]:
            return True
        if value.lower() == self.value[1]:
            return True
        raise ValueError(f'Cannot convert {value} to bool with format {self.name}')

    def to_string(self, value: bool) -> str:
        if value:
            return self.value[0]
        else:
            return self.value[1]


def bool_control(
    formatter: BoolFormat,
    doc: str,
    get_cmd: str | None = None,
    set_cmd: str | None = None,
    /,
    pre_format: Callable[[str], str] | None = None,
    response: Callable[[str], None] | None = None,
) -> Property[MessageProtocol, bool]:
    return basic_control(
        bool,
        doc,
        get_cmd,
        set_cmd,
        get_format=None,  # accepts all formats
        set_format=formatter.to_string,
        pre_format=pre_format,
        validate=lambda value: value in [True, False],
        response=response,
    )


def enum_control[E: StrEnum](
    enum: type[E],
    doc: str,
    get_cmd: str | None = None,
    set_cmd: str | None = None,
    /,
    pre_format: Callable[[str], str] | None = None,
    response: Callable[[str], None] | None = None,
) -> Property[MessageProtocol, E]:
    return basic_control(
        enum,
        doc,
        get_cmd,
        set_cmd,
        get_format=_string_to_enum,
        set_format=lambda value: value.value,
        pre_format=pre_format,
        validate=lambda value: value in enum,
        response=response,
    )


def flag_control[F: IntFlag](
    flag: type[F],
    doc: str,
    get_cmd: str | None = None,
    set_cmd: str | None = None,
    /,
    pre_format: Callable[[str], str] | None = None,
    response: Callable[[str], None] | None = None,
) -> Property[MessageProtocol, F]:
    return basic_control(
        flag,
        doc,
        get_cmd,
        set_cmd,
        get_format=_string_to_flag,
        set_format=lambda value: flag(value).value,
        pre_format=pre_format,
        validate=lambda value: isinstance(flag(value), flag),
        response=response,
    )


def list_control[T](type_: type[T], doc: str) -> Property[MessageProtocol, list[T]]:
    raise NotImplementedError('Not implemented!')


def noop(_: str) -> None:
    pass
