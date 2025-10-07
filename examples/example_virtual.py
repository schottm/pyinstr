"""
This file is part of PyINSTR.

:copyright: 2025 by Marco Schott.
:license: MIT, see LICENSE for more details.
"""

from example_instrument import ExampleInstrument

from pyinstr import inject_real, inject_virtual, make_virtual
from pyinstr.adapters import NullAdapter

# create a new virtual instrument instance, providing default values for some properties.
virt_inst = make_virtual(ExampleInstrument, defaults={'identity': 'virt_instrument'})
print(virt_inst.identity)
virt_inst.identity = 'new_identity'
print(virt_inst.identity)

# or change a instrument instance to a virtual instrument using inject_virtual. (e.g. if the instrument disconnected)
inst = ExampleInstrument(NullAdapter())
print(inst.test.value)
inject_virtual(inst, defaults={'identity': 'injected_instrument'})
print(inst.identity)

# you can promote a virtual instrument to a real instrument using the inject_real method.
inject_real(virt_inst, NullAdapter())
print(virt_inst.identity)
