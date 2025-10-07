"""
This file is part of PyINSTR.

:copyright: 2025 by Marco Schott.
:license: MIT, see LICENSE for more details.
"""

from pyinstr import Channel, Instrument, MessageProtocol, basic_control
from pyinstr.adapters import NullAdapter
from pyinstr.instruments.mixins import SCPIMixin


class ExampleChannel(Channel[MessageProtocol]):
    """
    Channels can be used to represent instrument channels and subsystems which share similar commands.
    You can adjust the generic type to access methods of the parent instrument with self._parent:
    (class ExampleChannel(Channel['ExampleInstrument'])).
    By doing so, the channel can only be added to an instrument of the specified type.
    """

    value = basic_control(
        str,
        'Example control ',
        'GET:COMMAND:FOR:{ch}:VALUE?',
        'SET:COMMAND:FOR:{ch}:VALUE %s',
    )
    """
    The placeholder (default: {ch}, can be changed by overwriting the constructor) gets replaced with the channel id.
    """


class ExampleInstrument(SCPIMixin, Instrument):
    """
    Create a new instrument by inherting from the instrument base class.
    If your instrument supports the SCPI specifiction you can add the SCPIMixin to expose those commands.
    """

    test = ExampleChannel.make('test')
    """
    Using 'Channel.make' you can add instances of a channel to your instrument.
    """

    test_multiple = ExampleChannel.make_multiple('channel1', 'channel2')
    """
    Using 'Channel.make_multiple' you can add a predefined set of channels of the same type to your instrument.
    You can access individual channels using 'test_multiple[<channel_id>]'.
    If your channel does not match the name of a predefined channel, this will result in an error.
    """

    test_dynamic = ExampleChannel.make_dynamic()
    """
    Using 'Channel.make_dynamic' channels will get created dynamically on first access.
    This is usefull, if your instrument has a modular build with (e.g. expansion cards), thus channels differ
    depending on the configuration.
    You can access channels using 'test_dynamic[<channel_id>]', creating a new channel on the first access.
    """

    value = basic_control(
        str,
        'Example control',
        'GET:COMMAND:FOR:VALUE?',
        'SET:COMMAND:FOR:VALUE %s',
    )
    """
    This is a minimal channel control to get/set a specified value on the instrument.
    """


if __name__ == '__main__':
    inst = ExampleInstrument(NullAdapter())
    print(inst.value)
    print(inst.test.value)
    print(inst.identity)  # provided by the SCPIMixin
