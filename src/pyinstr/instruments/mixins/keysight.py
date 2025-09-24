"""
This file is part of PyINSTR.

:copyright: 2025 by Marco Schott.
:license: MIT, see LICENSE for more details.
"""

from enum import IntFlag, StrEnum

from pyinstr import BoolFormat, bool_control, enum_control, flag_control
from pyinstr.instruments.channels import KeysightControlChannel


class KeysightSupplyMixin:
    class PriorityMode(StrEnum):
        Current = 'CURR'
        Voltage = 'VOLT'

    class OperationStatus(IntFlag):
        ConstantVoltage = 1
        ConstantCurrent = 2
        OutputOff = 4
        MeasurementWait = 8
        TransientWait = 16
        MeasurementActive = 32
        TransientActive = 64
        User1 = 128
        User2 = 256

    class QuestionableStatus(IntFlag):
        VoltageProtection = 1
        CurrentProtection = 2
        PowerFail = 4
        PositivePowerLimit = 8
        TemperatureProtection = 16
        NegativePowerLimit = 32
        NegativeOverVoltage = 64
        PositiveLimit = 128
        NegativeLimit = 256
        Inhibit = 512
        Unregulated = 1024
        TimerProtection = 2048
        DynamicProtection = 4096
        SenseFault = 8192

    current = KeysightControlChannel.make('CURR')
    voltage = KeysightControlChannel.make('VOLT')

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
