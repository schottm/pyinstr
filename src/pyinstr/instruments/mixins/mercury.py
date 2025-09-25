"""
This file is part of PyINSTR.

:copyright: 2025 by Marco Schott.
:license: MIT, see LICENSE for more details.
"""

from datetime import date, datetime, time
from typing import ClassVar

from pyinstr import basic_control, noop
from pyinstr.adapters import VISAAdapter


class MercuryMixin:
    adapter_options: ClassVar = {
        VISAAdapter: {
            'read_termination': '\n',
            'write_termination': '\n',
        }
    }

    catalogue = basic_control(
        str,
        """Get the connected measurement units.""",
        'READ:SYS:CAT?',
    )

    date = basic_control(
        date,
        """Get/set the date of the instrument.""",
        'READ:SYS:DATE?',
        'SET:SYS:DATE:%s',
        get_format=lambda v: datetime.strptime(v, '%Y:%m:%d').date(),
        set_format=lambda v: date.strftime(v, '%Y:%m:%d'),
        response=noop,
    )

    time = basic_control(
        time,
        """Get/set the date of the instrument.""",
        'READ:SYS:TIME?',
        'SET:SYS:TIME:%s',
        get_format=lambda v: datetime.strptime(v, '%H:%M:%S').time(),
        set_format=lambda v: time.strftime(v, '%H:%M:%S'),
        response=noop,
    )
