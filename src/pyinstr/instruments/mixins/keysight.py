"""
This file is part of PyINSTR.

:copyright: 2025 by Marco Schott.
:license: MIT, see LICENSE for more details.
"""

from enum import IntFlag, StrEnum
from typing import ClassVar

from pyinstr import BoolFormat, MessageProtocol, basic_control, bool_control, enum_control, flag_control, list_control
from pyinstr.adapters import VISAAdapter
from pyinstr.instruments.channels import KeysightControlChannel, KeysightPinChannel


class KeysightListMixin:
    class ListStep(StrEnum):
        Auto = 'AUTO'
        Once = 'ONCE'

    list_count = basic_control(
        int,
        """Get/set the number of list entires.""",
        'LIST:COUN?',
        'LIST:COUN %d',
    )

    list_dwell = list_control(
        float,
        """Get/set the dwell times for each list entry.""",
        'LIST:DWEL?',
        'LIST:DWEL %s',
    )

    list_step = enum_control(
        ListStep,
        """Select either Dwell paced or Trigger paced.""",
        'LIST:STEP?',
        'LIST:STEP %s',
    )

    list_trigger_begin_output = list_control(
        int,
        'Get/set the steps when trigger is send at the beginning.',
        'LIST:TOUT:BOST?',
        'LIST:TOUT:BOST %s',
    )

    list_trigger_end_output = list_control(
        int,
        'Get/set the steps when trigger is send at the end.',
        'LIST:TOUT:EOST?',
        'LIST:TOUT:EOST %s',
    )



class KeysightSupplyMixin:
    adapter_options: ClassVar = {
        VISAAdapter: {
            'read_termination': '\n',
            'write_termination': '\n',
        }
    }

    class PriorityMode(StrEnum):
        Current = 'CURR'
        Voltage = 'VOLT'

    class OperationStatus(IntFlag):
        ConstantVoltage = 0x1
        ConstantCurrent = 0x2
        OutputOff = 0x4
        MeasurementWait = 0x8
        TransientWait = 0x10
        MeasurementActive = 0x20
        TransientActive = 0x40
        User1 = 0x80
        User2 = 0x100

    class QuestionableStatus(IntFlag):
        VoltageProtection = 0x1
        CurrentProtection = 0x2
        PowerFail = 0x4
        PositivePowerLimit = 0x8
        TemperatureProtection = 0x10
        NegativePowerLimit = 0x20
        NegativeOverVoltage = 0x40
        PositiveLimit = 0x80
        NegativeLimit = 0x100
        Inhibit = 0x200
        Unregulated = 0x400
        TimerProtection = 0x800
        DynamicProtection = 0x1000
        SenseFault = 0x2000

    current = KeysightControlChannel.make('CURR')
    voltage = KeysightControlChannel.make('VOLT')
    pins = KeysightPinChannel.make_multiple(*range(1, 8))

    function = enum_control(
        PriorityMode,
        """Get/set the priority mode.""",
        'FUNC?',
        'FUNC %s',
    )

    output_enabled = bool_control(
        BoolFormat.OneZero,
        """Enable/disable the output of the device.""",
        'OUTP?',
        'OUTP %s',
    )

    operation_status = flag_control(
        OperationStatus,
        """Returns the operation status.""",
        'STAT:OPER:COND?',
        None,
    )

    questionable_status = flag_control(
        QuestionableStatus,
        """Returns the questionable status.""",
        'STAT:QUES1:COND?',
        None,
    )

    step_output_enabled = bool_control(
        BoolFormat.OneZero,
        """Specifies whether a trigger out is generated when a transient step occurs.""",
        'STEP:TOUT?',
        'STEP:TOUT %s',
    )

    def inititate_transient(self: MessageProtocol) -> None:
        self.send('INIT:IMM:TRAN')

    def trigger_transient(self: MessageProtocol) -> None:
        self.send('TRIG:TRAN:IMM')
