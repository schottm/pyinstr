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

from .adapter import Adapter
from .control import (
    BoolFormat,
    basic_control,
    bool_control,
    enum_control,
    flag_control,
    instance_control,
    noop,
)
from .instrument import Channel, Instrument, MessageProtocol
from .virtual import make_virtual

__all__ = [
    'Adapter',
    'BoolFormat',
    'Channel',
    'Instrument',
    'MessageProtocol',
    'basic_control',
    'bool_control',
    'enum_control',
    'flag_control',
    'instance_control',
    'make_virtual',
    'noop',
]
