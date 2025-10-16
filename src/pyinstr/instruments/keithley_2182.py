"""
This file is part of PyINSTR.

:copyright: 2025 by Marco Schott.
:license: MIT, see LICENSE for more details.
"""

from pyinstr import BoolFormat, Channel, Instrument, MessageProtocol, basic_control, bool_control
from pyinstr.instruments.mixins import KeithleyBufferMixin, KeithleyMixin, SCPIMixin
from pyinstr.validator import for_channel, in_range_inc, in_set


class Keithley2182Channel(Channel[MessageProtocol]):
    voltage_range = basic_control(
        float,
        """Control the positive full-scale measurement voltage range in Volts.
        The Keithley 2182 selects a measurement range based on the expected voltage.
        DCV1 has five ranges: 10 mV, 100 mV, 1 V, 10 V, and 100 V.
        DCV2 has three ranges: 100 mV, 1 V, and 10 V.
        Valid limits are from 0 to 120 V for Ch. 1, and 0 to 12 V for Ch. 2.
        Auto-range is automatically disabled when this property is set.""",
        ':SENS:VOLT:CHAN{ch}:RANG?',
        ':SENS:VOLT:CHAN{ch}:RANG %g',
        validate=for_channel({'1': in_set(0.01, 0.100, 1.0, 10.0, 100.0), '2': in_set(0.100, 1.0, 10.0)}),
    )

    voltage_range_auto_enabled = bool_control(
        BoolFormat.OneZero,
        """Control the auto voltage ranging option (bool).""",
        ':SENS:VOLT:CHAN{ch}:RANG:AUTO?',
        ':SENS:VOLT:CHAN{ch}:RANG:AUTO %s',
    )

    voltage_offset = basic_control(
        float,
        """Control the relative offset for measuring voltage.
        Displayed value = actual value - offset value.
        Valid ranges are -120 V to +120 V for Ch. 1, and -12 V to +12 V for Ch. 2.""",
        ':SENS:VOLT:CHAN{ch}:REF?',
        ':SENS:VOLT:CHAN{ch}:REF %g',
        validate=for_channel({'1': in_range_inc(-120.0, 120.0), '2': in_range_inc(-12.0, 12.0)}),
    )

    temperature_offset = basic_control(
        float,
        """Control the relative offset for measuring temperature.
        Displayed value = actual value - offset value.
        Valid values are -273 C to 1800 C.""",
        ':SENS:TEMP:CHAN{ch}:REF?',
        ':SENS:TEMP:CHAN{ch}:REF %g',
        validate=in_range_inc(-273.0, 1800.0),
    )

    voltage_offset_enabled = bool_control(
        BoolFormat.OneZero,
        """Control whether voltage is measured as a relative or absolute value (bool).
        Enabled by default for Ch. 2 voltage, which is measured relative to Ch. 1
        voltage.""",
        ':SENS:VOLT:CHAN{ch}:REF:STAT?',
        ':SENS:VOLT:CHAN{ch}:REF:STAT %s',
    )

    temperature_offset_enabled = bool_control(
        BoolFormat.OneZero,
        """Control whether temperature is measured as a relative or absolute value (bool).
        Disabled by default.""",
        ':SENS:TEMP:CHAN{ch}:REF:STAT?',
        ':SENS:TEMP:CHAN{ch}:REF:STAT %s',
    )


class Keithley2182(KeithleyMixin, KeithleyBufferMixin, SCPIMixin, Instrument):
    active_channel = basic_control(
        int,
        """Control which channel is active for measurement.""",
        ':SENS:CHAN?',
        ':SENS:CHAN %d',
        validate=in_set(0, 1, 2),
    )

    channel_1 = Keithley2182Channel.make('1')
    channel_2 = Keithley2182Channel.make('2')

    function = basic_control(
        KeithleyMixin.ChannelFunction,
        """Control the measurement mode of the active channel.""",
        ':SENS:FUNC?',
        ':SENS:FUNC %s',
        set_format=lambda value: value.value,
        validate=in_set(KeithleyMixin.ChannelFunction.Voltage, KeithleyMixin.ChannelFunction.Temperature),
    )
