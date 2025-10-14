"""
This file is part of PyINSTR.

:copyright: 2025 by Marco Schott.
:license: MIT, see LICENSE for more details.
"""

import time
from abc import ABC, abstractmethod
from collections import defaultdict
from contextlib import nullcontext
from types import TracebackType
from typing import Any, ClassVar, Protocol, override, runtime_checkable

from pyinstr.property import Property


class Adapter(ABC):
    @abstractmethod
    def read(self) -> str:
        pass

    @abstractmethod
    def write(self, command: str) -> None:
        pass

    @abstractmethod
    def apply(self, options: dict[str, Any]) -> None:
        pass


class MessageBase(ABC):
    @abstractmethod
    def send(self, command: str) -> None: ...
    @abstractmethod
    def query(self, command: str, delay: float | None = None) -> str: ...


@runtime_checkable
class MessageProtocol(Protocol):
    def send(self, command: str) -> None: ...
    def query(self, command: str, delay: float | None = None) -> str: ...


class ContextProtocol[T](Protocol):
    def __enter__(self, /) -> T: ...

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        exc_traceback: TracebackType | None,
        /,
    ) -> bool | None: ...


_NullContext = nullcontext()


class Instrument(MessageBase):
    adapter_options: ClassVar[dict[type[Adapter], dict[str, Any]]] = {}

    def __init__(self, adapter: Adapter, context: ContextProtocol[Any] = _NullContext) -> None:
        self._context = context
        self._adapter = adapter

        if (options := self.adapter_options.get(type(self._adapter))) is not None:
            self._adapter.apply(options)

    @override
    def send(self, command: str) -> None:
        if command == '':
            return
        with self._context:
            self._adapter.write(command)
            return
        self._adapter.write(command)

    @override
    def query(self, command: str, delay: float | None = None) -> str:
        if command == '':
            return ''
        with self._context:
            self._adapter.write(command)
            if delay is not None:
                time.sleep(delay)
            return self._adapter.read()
        self._adapter.write(command)
        if delay is not None:
            time.sleep(delay)
        return self._adapter.read()

    def close(self) -> None:
        with self._context:
            del self._adapter  # this will throw errors if the communication is used after closing the instrument.


class ChannelDict[B: MessageProtocol, I, T: Channel[MessageProtocol]](defaultdict[I, T]):
    def __init__(self, type_: type[T], base: B, *channel_ids: I, dynamic: bool = False) -> None:
        super().__init__()
        self._type_ = type_
        self._base = base
        self._dynamic = dynamic
        for channel_id in channel_ids:
            self[channel_id] = type_(self._base, str(channel_id))

    @property
    def type_(self) -> type[T]:
        return self._type_

    @property
    def base(self) -> B:
        return self._base

    @property
    def dynamic(self) -> bool:
        return self._dynamic

    def __missing__(self, key: I) -> T:
        if not self._dynamic:
            raise ValueError('This is not a dynamic channel dictionary.')
        value = self._type_(self._base, str(key))
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


class SingleChannelFactory[B: MessageProtocol, T: Channel[MessageProtocol]](ChannelFactory[B, T, T]):
    def __init__(self, type_: type[T], channel_id: str) -> None:
        super().__init__(type_)
        self._channel_id = channel_id

    def make(self, base: B) -> T:
        return self._type_(base, self._channel_id)


class MultiChannelFactory[B: MessageProtocol, I, T: Channel[MessageProtocol]](ChannelFactory[B, T, dict[I, T]]):
    def __init__(self, type_: type[T], *channel_ids: I, dynamic: bool = False) -> None:
        super().__init__(type_)
        self._channel_ids = channel_ids
        self._dynamic = dynamic

    @override
    def make(self, base: B) -> dict[I, T]:
        return ChannelDict(self._type_, base, *self._channel_ids, dynamic=self._dynamic)


class ChannelProperty[B: MessageProtocol, C: Channel[MessageProtocol], T](Property[B, T]):
    def __init__(
        self,
        factory: ChannelFactory[B, C, T],
        name: str | None = None,
        doc: str | None = None,
    ) -> None:
        self._factory = factory

        super().__init__(fget=self._getter, fset=None, fdel=self._deleter, name=name, doc=doc)

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


class Channel[P: MessageProtocol](MessageBase):
    def __init__(self, parent: P, channel_id: str, placeholder: str = 'ch') -> None:
        self._parent = parent
        self._channel_id = channel_id
        self._placeholder = placeholder

    @property
    def parent(self) -> P:
        return self._parent

    @property
    def name(self) -> str:
        return self._channel_id

    @override
    def send(self, command: str) -> None:
        self._parent.send(command.format_map({self._placeholder: self._channel_id}))

    @override
    def query(self, command: str, delay: float | None = None) -> str:
        return self._parent.query(command.format_map({self._placeholder: self._channel_id}), delay)

    @classmethod
    def make[T: Channel[MessageProtocol]](
        cls: type[T], channel_id: str, doc: str | None = None
    ) -> Property[MessageProtocol, T]:
        return ChannelProperty(SingleChannelFactory(cls, channel_id), doc=doc)

    @classmethod
    def make_multiple[I, T: Channel[MessageProtocol]](
        cls: type[T], *channel_ids: I, doc: str | None = None
    ) -> Property[MessageProtocol, dict[I, T]]:
        return ChannelProperty(
            MultiChannelFactory(cls, *channel_ids, dynamic=False),
            doc=doc,
        )

    @classmethod
    def make_dynamic[T: Channel[MessageProtocol]](
        cls: type[T], doc: str | None = None
    ) -> Property[MessageProtocol, dict[str, T]]:
        return ChannelProperty(
            MultiChannelFactory[MessageProtocol, str, T](cls, dynamic=True),
            doc=doc,
        )
