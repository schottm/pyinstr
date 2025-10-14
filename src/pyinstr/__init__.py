"""
This file is part of PyINSTR.

:copyright: 2025 by Marco Schott.
:license: MIT, see LICENSE for more details.
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version('pyinstr')
except PackageNotFoundError:
    # package is not installed
    pass

from .control import (
    BoolFormat,
    always,
    basic_control,
    bool_control,
    convert_registry,
    enum_control,
    flag_control,
    ignore,
    list_control,
    noop,
    optional_control,
)
from .message import Adapter, Channel, Instrument, MessageProtocol
from .virtual import default_registry, inject_real, inject_virtual, is_virtual, make_virtual

__all__ = [
    'Adapter',
    'BoolFormat',
    'Channel',
    'Instrument',
    'MessageProtocol',
    'always',
    'basic_control',
    'bool_control',
    'convert_registry',
    'default_registry',
    'enum_control',
    'flag_control',
    'ignore',
    'inject_real',
    'inject_virtual',
    'is_virtual',
    'list_control',
    'make_virtual',
    'noop',
    'optional_control',
]
