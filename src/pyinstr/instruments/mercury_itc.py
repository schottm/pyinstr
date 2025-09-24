"""
This file is part of PyINSTR.

:copyright: 2025 by Marco Schott.
:license: MIT, see LICENSE for more details.
"""

from typing import ClassVar

from pyinstr import Instrument
from pyinstr.adapters import VISAAdapter
from pyinstr.instruments.channels import FlowControl, HeaterControl, TemperatureLoopControl
from pyinstr.instruments.mixins import MercuryMixin, SCPIMixin


class MercuryiTC(SCPIMixin, MercuryMixin, Instrument):
    adapter_options: ClassVar = {
        VISAAdapter: {
            'read_termination': '\n',
            'write_termination': '\n',
        }
    }

    temperature_controls = TemperatureLoopControl.make_dynamic()

    heater_controls = HeaterControl.make_dynamic()

    flow_controls = FlowControl.make_dynamic()
