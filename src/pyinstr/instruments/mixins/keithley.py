"""
This file is part of PyINSTR.

:copyright: 2025 by Marco Schott.
:license: MIT, see LICENSE for more details.
"""

from enum import StrEnum

from pyinstr import BoolFormat, basic_control, bool_control, enum_control


class KeithleyMixin:
    class TriggerSource(StrEnum):
        Immediate = 'IMM'
        Timer = 'TIM'
        Manual = 'MAN'
        Bus = 'BUS'
        External = 'EXT'

    fetch = basic_control(
        float,
        """Fetch the latest post-processed reading.""",
        ':FETC?',
    )

    read = basic_control(
        float,
        """Performs an ABORt, INITiate, and a FETCh?.""",
        ':READ?',
    )

    trigger_source = enum_control(
        TriggerSource,
        """Gets/sets the trigger source.""",
        ':TRIG:SOUR?',
        ':TRIG:SOUR %s',
    )

    initiate_continuous_enabled = bool_control(
        BoolFormat.OneZero,
        """Gets/sets continous measurement.""",
        ':INIT:CONT?',
        ':INIT:CONT %s',
    )
