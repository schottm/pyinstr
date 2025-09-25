from pyinstr import Channel, Instrument, MessageProtocol, basic_control, make_virtual
from pyinstr.adapters import NullAdapter
from pyinstr.instruments import Keithley2182


class ExampleChannel(Channel[MessageProtocol]):
    value = basic_control(str, 'Example get/set id', '*IDN?', '*IDN %s')


class ExampleInstrument(Instrument):
    test = ExampleChannel.make('test')

    test_multiple = ExampleChannel.make_multiple('channel1', 'channel2')

    test_dynamic = ExampleChannel.make_dynamic()


inst = ExampleInstrument(NullAdapter())
print(inst.test.value)

virt = make_virtual(ExampleInstrument, defaults={'test_multiple': {'value': 'hello'}})
print(virt.test_multiple['channel1'].value)
print(inst.test.value)

keithley_virt = make_virtual(Keithley2182)
keithley_virt.clear_status()
print(keithley_virt.trigger_source)
keithley_virt.trigger_source = Keithley2182.TriggerSource.External
print(keithley_virt.trigger_source)
