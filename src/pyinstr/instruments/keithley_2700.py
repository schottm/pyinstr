from pyinstr import BoolFormat, Channel, Instrument, MessageProtocol, basic_control, bool_control
from pyinstr.instruments.mixins import KeithleyMixin, SCPIMixin
from pyinstr.validator import in_range_inc


class Keithley2700Channel(Channel[MessageProtocol]):
    auto_range_enabled = bool_control(
        BoolFormat.OneZero,
        """Controls the auto range.""",
        ':SENS:VOLT:{ch}:RANG:AUTO?',
        ':SENS:VOLT:{ch}:RANG:AUTO %s',
    )

    digits = basic_control(
        int,
        """Controls the precission.""",
        ':SENS:VOLT:{ch}:DIG?',
        ':SENS:VOLT:{ch}:DIG %d',
        validate=in_range_inc(4, 7),
    )


class Keithley2700(KeithleyMixin, SCPIMixin, Instrument):
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
