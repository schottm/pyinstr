import time

from pyinstr.adapters import VISAAdapter
from pyinstr.instruments import Keithley2182

inst = Keithley2182(VISAAdapter.make_gpib(17))
print('instrument: ' + inst.identity)
inst.reset()
inst.active_channel = 1
inst.function = Keithley2182.ChannelFunction.Voltage
inst.display_enabled = True
inst.voltage_digits = 7
inst.voltage_nplc = 5.0
inst.trigger_source = Keithley2182.TriggerSource.Immediate
inst.initiate_continuous_enabled = True

for _ in range(10):
    time.sleep(0.5)
    print(inst.fetch)
