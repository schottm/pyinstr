"""
This file is part of PyINSTR.

:copyright: 2025 by Marco Schott.
:license: MIT, see LICENSE for more details.
"""

from pyinstr import Instrument
from pyinstr.instruments.channels import FlowControl, HeaterControl, TemperatureLoopControl
from pyinstr.instruments.mixins import MercuryMixin, SCPIMixin


class MercuryiTC(SCPIMixin, MercuryMixin, Instrument):
    temperature_controls = TemperatureLoopControl.make_dynamic()

    heater_controls = HeaterControl.make_dynamic()

    flow_controls = FlowControl.make_dynamic()
