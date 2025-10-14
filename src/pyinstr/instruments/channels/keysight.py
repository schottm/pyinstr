"""
This file is part of PyINSTR.

:copyright: 2025 by Marco Schott.
:license: MIT, see LICENSE for more details.
"""

from enum import StrEnum

from pyinstr import BoolFormat, Channel, MessageProtocol, basic_control, bool_control, enum_control, list_control


class KeysightPinChannel(Channel[MessageProtocol]):
    class Function(StrEnum):
        DigitalIO = 'DIO'
        DigitalInput = 'DINP'
        Fault = 'FAUL'
        Inhibit = 'INH'
        OnCouple = 'ONC'
        OffCouple = 'OFFC'
        TriggerInput = 'TINP'
        TriggerOutput = 'TOUT'

    class Polarity(StrEnum):
        Positive = 'POS'
        Negative = 'NEG'

    function = enum_control(
        Function,
        """Sets the pin function. The functions are saved in non-volatile memory.""",
        'DIG:PIN{ch}:FUNC?',
        'DIG:PIN{ch}:FUNC %s',
    )

    polarity = enum_control(
        Polarity,
        """Sets the pin polarity. POSitive means a logical true signal is a voltage high at the pin.""",
        'DIG:PIN{ch}:POL?',
        'DIG:PIN{ch}:POL %s',
    )


class KeysightListChannel(Channel[MessageProtocol]):
    class Step(StrEnum):
        Auto = 'AUTO'
        Once = 'ONCE'

    count = basic_control(
        int,
        """Get/set the number of list entires.""",
        'LIST:COUN?',
        'LIST:COUN %d',
    )

    dwell = list_control(
        float,
        """Get/set the dwell times for each list entry.""",
        'LIST:DWEL?',
        'LIST:DWEL %s',
    )

    step = enum_control(
        Step,
        """Select either Dwell paced or Trigger paced.""",
        'LIST:STEP?',
        'LIST:STEP %s',
    )

    trigger_begin_output = list_control(
        int,
        'Get/set the steps when trigger is send at the beginning.',
        'LIST:TOUT:BOST?',
        'LIST:TOUT:BOST %s',
    )

    trigger_end_output = list_control(
        int,
        'Get/set the steps when trigger is send at the end.',
        'LIST:TOUT:EOST?',
        'LIST:TOUT:EOST %s',
    )


class KeysightControlChannel(Channel[MessageProtocol]):
    value = basic_control(
        float,
        """Get/set the target voltage/current level.""",
        '{ch}?',
        '{ch} %g',
    )

    list_values = list_control(
        float,
        """Get/set the voltage/current values.""",
        'LIST:{ch}?',
        'LIST:{ch} %s',
    )

    limit = basic_control(
        float,
        """Get/set the voltage/current limit, when in current/voltage mode.""",
        '{ch}:LIM?',
        '{ch}:LIM %g',
    )

    triggered_level = basic_control(
        float,
        """Get/set the target triggered voltage/current level.""",
        '{ch}:TRIG?',
        '{ch}:TRIG %g',
    )

    class Mode(StrEnum):
        Fixed = 'FIX'
        Step = 'STEP'
        List = 'LIST'
        Waveform = 'ARB'

    mode = enum_control(
        Mode,
        """Get/set the mode which is executed when the transient system is triggered.""",
        '{ch}:MODE?',
        '{ch}:MODE %s',
    )

    slew = basic_control(
        float,
        """Get/set the voltage/current slew rate in (V|A)/s.""",
        '{ch}:SLEW?',
        '{ch}:SLEW %g',
    )

    maximum_slew = bool_control(
        BoolFormat.OneZero,
        """Get/set the voltage/current slew rate to the maximum value.""",
        '{ch}:SLEW:MAX?',
        '{ch}:SLEW:MAX %s',
    )
