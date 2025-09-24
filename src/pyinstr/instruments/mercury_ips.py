"""
This file is part of PyINSTR.

:copyright: 2025 by Marco Schott.
:license: MIT, see LICENSE for more details.
"""

from typing import ClassVar

from pyinstr import Instrument
from pyinstr.adapters import VISAAdapter
from pyinstr.instruments.channels import LevelSensor, MagnetControl, TemperatureSensor
from pyinstr.instruments.mixins import MercuryMixin, SCPIMixin


class MercuryiPS(SCPIMixin, MercuryMixin, Instrument):
    adapter_options: ClassVar = {
        VISAAdapter: {
            'read_termination': '\n',
            'write_termination': '\n',
        }
    }

    temperature_sensors = TemperatureSensor.make('MB1.T1')

    level_sensors = LevelSensor.make_dynamic()

    magnet_controls = MagnetControl.make_dynamic()
