"""
This file is part of PyINSTR.

:copyright: 2025 by Marco Schott.
:license: MIT, see LICENSE for more details.
"""

from typing import ClassVar

from pyvisa.constants import ControlFlow, Parity, StopBits

from pyinstr import BoolFormat, Instrument, basic_control, bool_control, noop
from pyinstr.adapters import VISAAdapter
from pyinstr.validator import in_range, in_range_inc


class Lakeshore121(Instrument):
    adapter_options: ClassVar = {
        VISAAdapter: {
            'baud_rate': 57600,
            'data_bits': 7,
            'stop_bits': StopBits.one,
            'parity': Parity.odd,
            'flow_control': ControlFlow.none,
            'timeout': 2000,
            'read_termination': '\n',
            'write_termination': '\n',
        }
    }

    identity = basic_control(
        str,
        """Returns the identity of the instrument.""",
        '*IDN?',
    )

    contrast = basic_control(
        int,
        """Gets/sets the display contrast of the front panel seven-segment display.""",
        'BRIGT?',
        'BRIGT %02d; COMP?',
        validate=in_range(0, 16),
        response=noop,
    )

    enabled = bool_control(
        BoolFormat.OneZero,
        """Set/get enabled status of instrument.""",
        'IENBL?',
        'IENBL %d; COMP?',
        response=noop,
    )

    current = basic_control(
        float,
        """Sets the current Range of the instrument.""",
        'SETI?',
        'RANGE 13; SETI %f; COMP?',
        validate=in_range_inc(100e-9, 100e-3),
        response=noop,
    )

    def factory_defaults(self) -> None:
        """Resets the instruments to factory default and resets the instrument."""
        self.query('DFLT 99; COMP?')

    def reset(self) -> None:
        """Reset the instrument."""
        self.query('*RST; COMP?')
