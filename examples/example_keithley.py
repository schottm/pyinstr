from pyinstr.adapters import NullAdapter
from pyinstr.instruments import Keithley2182

inst = Keithley2182(NullAdapter())
print('instrument: ' + inst.identity)
