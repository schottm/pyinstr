"""
This file is part of PyINSTR.

:copyright: 2025 by Marco Schott.
:license: MIT, see LICENSE for more details.
"""

import time

from pyinstr.adapters import VISAAdapter
from pyinstr.instruments import Keithley2182

# connect to a Keithley2182 using a gpib connection with address 17 (GPIB::17)
inst = Keithley2182(VISAAdapter.make_gpib(17))
print(inst.identity)

# configure the measurement
inst.reset()
inst.active_channel = 1
inst.function = Keithley2182.ChannelFunction.Voltage
inst.display_enabled = True
inst.voltage_digits = 7
inst.voltage_nplc = 5.0
inst.trigger_source = Keithley2182.TriggerSource.Immediate

# sample countinuous and just fetch the last measurement
inst.initiate_continuous_enabled = True
for _ in range(10):
    time.sleep(0.5)
    print(inst.fetch)

# or manually initiate a read (this will block until measurement is complete)
inst.initiate_continuous_enabled = False
for _ in range(10):
    time.sleep(0.5)
    print(inst.read)
