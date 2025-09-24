"""
This file is part of PyINSTR.

:copyright: 2025 by Marco Schott.
:license: MIT, see LICENSE for more details.
"""

from enum import StrEnum

from pyinstr import BoolFormat, Channel, MessageProtocol, basic_control, bool_control, enum_control


class KeysightControlChannel(Channel[MessageProtocol]):
    value = basic_control(
        float,
        """Get/set the target voltage/current level.""",
        '{ch}?',
        '{ch} %g',
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
