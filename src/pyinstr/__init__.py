"""
This file is part of PyINSTR.

:copyright: 2025 by Marco Schott.
:license: MIT, see LICENSE for more details.
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version('package-name')
except PackageNotFoundError:
    # package is not installed
    pass

from .control import (
    BoolFormat,
    basic_control,
    bool_control,
    convert_registry,
    enum_control,
    flag_control,
    instance_control,
    noop,
)
from .message import Adapter, Channel, Instrument, MessageProtocol
from .virtual import default_registry, is_virtual, make_virtual

__all__ = [
    'Adapter',
    'BoolFormat',
    'Channel',
    'Instrument',
    'MessageProtocol',
    'basic_control',
    'bool_control',
    'convert_registry',
    'default_registry',
    'enum_control',
    'flag_control',
    'instance_control',
    'is_virtual',
    'make_virtual',
    'noop',
]
