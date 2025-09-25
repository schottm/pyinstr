"""
This file is part of PyINSTR.

:copyright: 2025 by Marco Schott.
:license: MIT, see LICENSE for more details.
"""

from pyinstr import Instrument
from pyinstr.instruments.mixins import KeysightSupplyMixin, SCPIMixin


class KeysightN69XX(KeysightSupplyMixin, SCPIMixin, Instrument):
    pass
