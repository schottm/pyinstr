"""
This file is part of PyINSTR.

:copyright: 2025 by Marco Schott.
:license: MIT, see LICENSE for more details.
"""

import logging
from enum import Enum
from typing import Any, TypedDict, override

from pyvisa import ResourceManager
from pyvisa.constants import ControlFlow, Parity, StopBits
from pyvisa.resources import MessageBasedResource

from pyinstr import Adapter

log = logging.getLogger(__name__)


class VISAOptionDict(TypedDict):
    timeout: int
    read_termination: str
    write_termination: str


class InterfaceOption(Enum):
    Instrument = 'INSTR'
    Interface = 'INTFC'
    Socket = 'SOCKET'


class VISAAdapter(Adapter):
    def __init__(self, name: str, **kwargs: Any) -> None:  # noqa: ANN401
        manager = ResourceManager()
        resource = manager.open_resource(name, **kwargs)
        if not isinstance(resource, MessageBasedResource):
            raise ValueError('The specified resource is not message based.')
        self._resource = resource

    @classmethod
    def make_gpib[T: VISAAdapter](
        cls: type[T],
        address: int,
        board: int | None = None,
        sub_address: int | None = None,
        interface: InterfaceOption | None = None,
        **kwargs: VISAOptionDict,
    ) -> T:
        name = 'GPIB'
        if board is not None:
            name = f'{name}{board}'
        name = f'{name}::{address}'
        if sub_address is not None:
            name = f'{name}::{sub_address}'
        if interface is not None:
            name = f'{name}::{interface.value}'
        return cls(name=name, **kwargs)

    @classmethod
    def make_serial[T: VISAAdapter](
        cls: type[T],
        address: int,
        baud_rate: int | None = None,
        data_bits: int | None = None,
        parity: Parity | None = None,
        stop_bits: StopBits | None = None,
        flow_control: ControlFlow | None = None,
        **kwargs: VISAOptionDict,
    ) -> T:
        kwargs_edit: dict[str, Any] = kwargs
        if baud_rate is not None:
            kwargs_edit.setdefault('baud_rate', baud_rate)
        if data_bits is not None:
            kwargs_edit.setdefault('data_bits', data_bits)
        if parity is not None:
            kwargs_edit.setdefault('parity', parity)
        if stop_bits is not None:
            kwargs_edit.setdefault('stop_bits', stop_bits)
        if flow_control is not None:
            kwargs_edit.setdefault('flow_control', flow_control)
        return cls(
            name=f'ASRL{address}::INSTR',
            **kwargs,
        )

    @classmethod
    def make_tcpip[T: VISAAdapter](
        cls: type[T],
        address: str,
        port: int,
        board: int | None = None,
        **kwargs: VISAOptionDict,
    ) -> T:
        name = 'TCPIP'
        if board is not None:
            name = f'{name}{board}'
        name = f'{name}::{address}::{port}::SOCKET'
        return cls(name=name, **kwargs)

    @override
    def read(self) -> str:
        return self._resource.read()

    @override
    def write(self, command: str) -> None:
        self._resource.write(command)

    @override
    def apply(self, options: dict[str, Any]) -> None:
        for name, value in options.items():
            if hasattr(self._resource, name):
                setattr(self._resource, name, value)
            else:
                log.warning(
                    f"""The option {name} does not exist for
                    {self._resource.resource_name} of
                    type {self._resource.interface_type.name}."""
                )
