from pyinstr import BoolFormat, Channel, Instrument, MessageProtocol, basic_control, bool_control
from pyinstr.instruments.mixins import KeithleyBufferMixin, KeithleyMixin, SCPIMixin
from pyinstr.validator import for_channel, in_range_inc


class Keithley2700Channel(Channel[MessageProtocol]):
    voltage_range_auto_enabled = bool_control(
        BoolFormat.OneZero,
        """Controls the auto range.""",
        ':SENS:VOLT:{ch}:RANG:AUTO?',
        ':SENS:VOLT:{ch}:RANG:AUTO %s',
    )

    voltage_range = basic_control(
        float,
        """Select voltage range.""",
        ':SENS:VOLT:{ch}:RANG?',
        ':SENS:VOLT:{ch}:RANG %g',
        validate=for_channel({'DC': in_range_inc(0.0, 1000.0), 'AC': in_range_inc(0.0, 757.5)}),
    )

    digits = basic_control(
        int,
        """Controls the precission.""",
        ':SENS:VOLT:{ch}:DIG?',
        ':SENS:VOLT:{ch}:DIG %d',
        validate=in_range_inc(4, 7),
    )


class Keithley2700(KeithleyMixin, KeithleyBufferMixin, SCPIMixin, Instrument):
    dc = Keithley2700Channel.make('DC')
    ac = Keithley2700Channel.make('AC')

    closed_channel = basic_control(
        int,
        """Parameter that controls one closed channel.
        The mentioned channel is closed, other channels will be opened.""",
        ':ROUT:CLOS?',
        ':ROUT:CLOS (@%d)',
        get_format=lambda v: -1 if v == '' else int(v.strip(' ()@,')),
    )
