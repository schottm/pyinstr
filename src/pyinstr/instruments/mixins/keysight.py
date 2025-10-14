"""
This file is part of PyINSTR.

:copyright: 2025 by Marco Schott.
:license: MIT, see LICENSE for more details.
"""

from enum import IntFlag, StrEnum
from typing import ClassVar

from pyinstr import BoolFormat, MessageProtocol, bool_control, enum_control, flag_control
from pyinstr.adapters import VISAAdapter
from pyinstr.instruments.channels import KeysightControlChannel, KeysightListChannel, KeysightPinChannel


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
    list = KeysightListChannel.make('')

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
