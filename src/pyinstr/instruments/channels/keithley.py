"""
This file is part of PyINSTR.

:copyright: 2025 by Marco Schott.
:license: MIT, see LICENSE for more details.
"""

from enum import StrEnum

from pyinstr import Channel, MessageProtocol, basic_control, enum_control, list_control


class KeithleyBufferChannel(Channel[MessageProtocol]):
    class BufferSource(StrEnum):
        Sense = 'SENS'
        Calculate = 'CALC'
        Nothing = 'NONE'

    class BufferMode(StrEnum):
        Never = 'NEV'
        Next = 'NEXT'

    free = basic_control(
        int,
        """Query bytes available and bytes in use.""",
        ':TRAC:FREE?',
    )

    points = basic_control(
        int,
        """Specify number of readings to store (2 to 1024).""",
        ':TRAC:POIN?',
        ':TRAC:POIN %d',
    )

    feed = enum_control(
        BufferSource,
        """Select source of readings.""",
        ':TRAC:FEED?',
        ':TRAC:FEED %s',
    )

    control = enum_control(
        BufferMode,
        """Select buffer control mode.""",
        ':TRAC:FEED:CONT?',
        ':TRAC:FEED:CONT %s',
    )

    data = list_control(
        float,
        """Get the buffer data.""",
        ':TRAC:DATA?',
    )

    def clear(self) -> None:
        self.send(':TRAC:CLE')
