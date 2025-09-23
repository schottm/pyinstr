"""
This file is part of PyINSTR.

:copyright: 2025 by Marco Schott.
:license: MIT, see LICENSE for more details.
"""

from pyinstr import Instrument
from pyinstr.mixins import KeithleyMixin, SCPIMixin


class Keithley2182(SCPIMixin, KeithleyMixin, Instrument):
    pass
