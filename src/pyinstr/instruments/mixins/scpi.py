"""
This file is part of PyINSTR.

:copyright: 2025 by Marco Schott.
:license: MIT, see LICENSE for more details.
"""

from pyinstr import MessageProtocol, basic_control


class SCPIMixin:
    def clear_status(self: MessageProtocol) -> None:
        self.send('*CLS')

    event_enable = basic_control(
        int,
        """Gets/sets bits in the standard event status enable register.""",
        '*ESE?',
        '*ESE %d',
    )

    event_status = basic_control(
        int,
        """Reads and clears event status enable register.""",
        '*ESR?',
        None,
    )

    identity = basic_control(
        str,
        """Returns the identity of the instrument.""",
        '*IDN?',
        None,
    )

    complete = basic_control(
        bool,
        """Returns true when all pending overlapped operations have been completed.""",
        '*OPC?',
        '%s',
        get_format=lambda value: value == '1',
        set_format=lambda value: '*OPC' if value else '',
    )

    def reset(self: MessageProtocol) -> None:
        """Executes a device reset and cancels any pending *OPC command or query."""
        self.send('*RST')

    service_enable = basic_control(
        int,
        """Gets/sets bits in the service request enable register.""",
        '*ESE?',
        '*ESE %d',
    )

    status = basic_control(
        int,
        """Read the status byte.""",
        '*STB?',
    )

    test = basic_control(
        int,
        """Issues the self test query.""",
        '*TST?',
        None,
    )

    def wait(self: MessageProtocol) -> None:
        """Inserts a waiting barrier between commands on the device."""
        self.send('*WAI')
