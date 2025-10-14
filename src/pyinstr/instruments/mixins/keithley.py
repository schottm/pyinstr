"""
This file is part of PyINSTR.

:copyright: 2025 by Marco Schott.
:license: MIT, see LICENSE for more details.
"""

from enum import StrEnum
from typing import ClassVar

from pyinstr import BoolFormat, MessageProtocol, basic_control, bool_control, enum_control
from pyinstr.adapters import VISAAdapter
from pyinstr.validator import in_range_inc


class KeithleyMixin:
    adapter_options: ClassVar = {
        VISAAdapter: {
            'read_termination': '\n',
            'write_termination': '\n',
        }
    }

    class ChannelFunction(StrEnum):
        Voltage = '"VOLT:DC"'
        VoltageAlternating = '"VOLT:AC"'
        Current = '"CURRENT:DC"'
        CurrentAlternating = '"CURRENT:AC"'
        Resistance = '"RES"'
        Fresistance = '"FRES"'
        Temperature = '"TEMP"'
        Frequency = '"FREQ"'
        Period = '"PER"'
        Continuity = '"CONT"'

    class TriggerSource(StrEnum):
        Immediate = 'IMM'
        Timer = 'TIM'
        Manual = 'MAN'
        Bus = 'BUS'
        External = 'EXT'

    class FormatElement(StrEnum):
        Reading = 'READ'
        Units = 'UNIT'
        Timestamp = 'TST'
        ReadingNumber = 'RNUM'
        Channel = 'CHAN'
        Limits = 'LIM'

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

    fresh = basic_control(
        float,
        """Return a new (fresh) reading. Waits if no reading is available.""",
        ':SENS:DATA:FRESh?',
    )

    function = enum_control(
        ChannelFunction,
        """Control the measurement mode of the active channel.""",
        ':SENS:FUNC?',
        ':SENS:FUNC %s',
    )

    trigger_source = enum_control(
        TriggerSource,
        """Gets/sets the trigger source.""",
        ':TRIG:SOUR?',
        ':TRIG:SOUR %s',
    )

    trigger_count = basic_control(
        int,
        """Controls the trigger count.""",
        ':TRIG:COUN?',
        ':TRIG:COUN %d',
        validate=in_range_inc(1, 55000),
    )

    initiate_continuous_enabled = bool_control(
        BoolFormat.OneZero,
        """Gets/sets continous measurement.""",
        ':INIT:CONT?',
        ':INIT:CONT %s',
    )

    display_enabled = bool_control(
        BoolFormat.OneZero,
        """Controls whether the front display is enabled.""",
        ':DISP:ENAB?',
        ':DISP:ENAB %s',
    )

    voltage_nplc = basic_control(
        float,
        """Control the number of power line cycles (NPLC) for voltage measurements,
        which sets the integration period and measurement speed.
        Valid values are from 0.01 to 50 or 60, depending on the line frequency.
        Default is 5.""",
        ':SENS:VOLT:NPLC?',
        ':SENS:VOLT:NPLC %g',
        validate=in_range_inc(0.01, 60.0),
    )

    voltage_digits = basic_control(
        int,
        """Specify measurement resolution.""",
        ':SENS:VOLT:DIG?',
        ':SENS:VOLT:DIG %d',
        validate=in_range_inc(4, 7),
    )

    format = enum_control(
        FormatElement,
        """Set the element returned in the reading.""",
        ':FORM:ELEM?',
        ':FORM:ELEM %s',
    )

    def abort(self: MessageProtocol) -> None:
        self.send(':ABOR')

    def initiate(self: MessageProtocol) -> None:
        self.send(':INIT')
