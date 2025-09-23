"""
This file is part of PyINSTR.

:copyright: 2025 by Marco Schott.
:license: MIT, see LICENSE for more details.
"""

import time
from abc import ABC, abstractmethod
from collections import defaultdict
from threading import Lock
from typing import Any, ClassVar, Protocol, override, runtime_checkable

from pyinstr.adapter import Adapter
from pyinstr.property import Property


class GenericBase(ABC):
    @abstractmethod
    def send(self, command: str) -> None: ...
    @abstractmethod
    def query(self, command: str, delay: float | None = None) -> str: ...


@runtime_checkable
class MessageProtocol(Protocol):
    def send(self, command: str) -> None: ...
    def query(self, command: str, delay: float | None = None) -> str: ...


class Instrument(GenericBase):
    adapter_options: ClassVar[dict[type[Adapter], dict[str, Any]]] = {}

    def __init__(self, adapter: Adapter, sync: bool = True) -> None:
        self._lock = Lock() if sync else None
        self._adapter = adapter

        if (options := self.adapter_options.get(type(self._adapter))) is not None:
            self._adapter.apply(options)

    @override
    def send(self, command: str) -> None:
        if command == '':
            return
        if self._lock is not None:
            with self._lock:
                self._adapter.write(command)
                return
        self._adapter.write(command)

    @override
    def query(self, command: str, delay: float | None = None) -> str:
        if command == '':
            return ''
        if self._lock is not None:
            with self._lock:
                self._adapter.write(command)
                if delay is not None:
                    time.sleep(delay)
                return self._adapter.read()
        self._adapter.write(command)
        if delay is not None:
            time.sleep(delay)
        return self._adapter.read()


class ChannelDict[B: MessageProtocol, T: Channel[MessageProtocol]](defaultdict[str, T]):
    def __init__(
        self, type_: type[T], base: B, *channel_ids: str, dynamic: bool = False
    ) -> None:
        super().__init__()
        self._type_ = type_
        self._base = base
        self._dynamic = dynamic
        for channel_id in channel_ids:
            self[channel_id] = type_(self._base, channel_id)

    @property
    def type_(self) -> type[T]:
        return self._type_

    @property
    def base(self) -> B:
        return self._base

    @property
    def dynamic(self) -> bool:
        return self._dynamic

    def __missing__(self, key: str) -> T:
        if not self._dynamic:
            raise ValueError('This is not a dynamic channel dictionary.')
        value = self._type_(self._base, key)
        self[key] = value
        return value


class ChannelFactory[B: MessageProtocol, T: Channel[MessageProtocol], R]:
    def __init__(self, type_: type[T]) -> None:
        self._type_ = type_

    @property
    def type_(self) -> type[T]:
        return self._type_

    @type_.setter
    def type_(self, value: type[T]) -> None:
        self._type_ = value

    def make(self, base: B) -> R:
        raise NotImplementedError('Not implemented!')


class SingleChannelFactory[B: MessageProtocol, T: Channel[MessageProtocol]](
    ChannelFactory[B, T, T]
):
    def __init__(self, type_: type[T], channel_id: str) -> None:
        super().__init__(type_)
        self._channel_id = channel_id

    def make(self, base: B) -> T:
        return self._type_(base, self._channel_id)


class MultiChannelFactory[B: MessageProtocol, T: Channel[MessageProtocol]](
    ChannelFactory[B, T, dict[str, T]]
):
    def __init__(
        self, type_: type[T], *channel_ids: str, dynamic: bool = False
    ) -> None:
        super().__init__(type_)
        self._channel_ids = channel_ids
        self._dynamic = dynamic

    @override
    def make(self, base: B) -> dict[str, T]:
        return ChannelDict(self._type_, base, *self._channel_ids, dynamic=self._dynamic)


class ChannelProperty[B: MessageProtocol, C: Channel[MessageProtocol], T](
    Property[B, T]
):
    def __init__(
        self,
        factory: ChannelFactory[B, C, T],
        name: str | None = None,
        doc: str | None = None,
    ) -> None:
        self._factory = factory

        super().__init__(
            fget=self._getter, fset=None, fdel=self._deleter, name=name, doc=doc
        )

    @property
    def factory(self) -> ChannelFactory[B, C, T]:
        return self._factory

    def _getter(self, base: B) -> T:
        attr_id = f'_{self._name}'
        if not hasattr(base, attr_id):
            setattr(base, attr_id, self._factory.make(base))
        return getattr(base, attr_id)

    def _deleter(self, base: B) -> None:
        attr_id = f'_{self._name}'
        delattr(base, attr_id)


class Channel[P: MessageProtocol](GenericBase):
    def __init__(self, parent: P, channel_id: str, placeholder: str = 'ch') -> None:
        self._parent = parent
        self._channel_id = channel_id
        self._placeholder = placeholder

    @override
    def send(self, command: str) -> None:
        self._parent.send(command.format_map({self._placeholder: self._channel_id}))

    @override
    def query(self, command: str, delay: float | None = None) -> str:
        return self._parent.query(
            command.format_map({self._placeholder: self._channel_id}), delay
        )

    @classmethod
    def make[T: Channel[MessageProtocol]](
        cls: type[T], channel_id: str, doc: str | None = None
    ) -> Property[MessageProtocol, T]:
        return ChannelProperty(SingleChannelFactory(cls, channel_id), doc=doc)

    @classmethod
    def make_multiple[T: Channel[MessageProtocol]](
        cls: type[T], *channel_ids: str, doc: str | None = None
    ) -> Property[MessageProtocol, dict[str, T]]:
        return ChannelProperty(
            MultiChannelFactory(cls, *channel_ids, dynamic=False),
            doc=doc,
        )

    @classmethod
    def make_dynamic[T: Channel[MessageProtocol]](
        cls: type[T], doc: str | None = None
    ) -> Property[MessageProtocol, dict[str, T]]:
        return ChannelProperty(
            MultiChannelFactory(cls, dynamic=True),
            doc=doc,
        )
