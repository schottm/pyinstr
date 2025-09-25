"""
This file is part of PyINSTR.

:copyright: 2025 by Marco Schott.
:license: MIT, see LICENSE for more details.
"""

from pyinstr import Instrument
from pyinstr.instruments.channels import LevelSensor, MagnetControl, TemperatureSensor
from pyinstr.instruments.mixins import MercuryMixin, SCPIMixin


class MercuryiPS(SCPIMixin, MercuryMixin, Instrument):
    temperature_sensor = TemperatureSensor.make('MB1.T1')

    magnet_controls = MagnetControl.make_dynamic()

    level_sensors = LevelSensor.make_dynamic()
