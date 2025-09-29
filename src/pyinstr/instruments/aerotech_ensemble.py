"""
This file is part of PyINSTR.

:copyright: 2025 by Marco Schott.
:license: MIT, see LICENSE for more details.
"""

import logging
from enum import IntFlag, StrEnum
from typing import ClassVar

from pyinstr import (
    Channel,
    Instrument,
    MessageProtocol,
    basic_control,
    enum_control,
    flag_control,
    ignore,
    optional_control,
)
from pyinstr.adapters import VISAAdapter

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


def _check_fault(status: str) -> None:
    if status == '!':
        raise ValueError('Wrong command format')
    elif status == '#':
        log.warning('Axis faults received.')


class AxisControl(Channel[MessageProtocol]):
    class AxisFault(IntFlag):
        PositionError = 0x1
        OverCurrent = 0x2
        CwEOTLimit = 0x4
        CcwEOTLimit = 0x8
        CwSoftLimit = 0x10
        CcwSoftLimit = 0x20
        AmplifierFault = 0x40
        PositionFbk = 0x80
        VelocityFbk = 0x100
        HallFault = 0x200
        MaxVelocity = 0x400
        EstopFault = 0x800
        VelocityError = 0x1000
        ExternalFault = 0x8000
        MotorTemp = 0x20000
        AmplifierTemp = 0x40000
        EncoderFault = 0x80000
        CommLost = 0x100000
        FbkScalingFault = 0x800000
        MrkSearchFault = 0x1000000
        VoltageClamp = 0x8000000
        PowerSupply = 0x10000000
        Internal = 0x20000000

    class AxisStatus(IntFlag):
        Enabled = 0x1
        Homed = 0x2
        InPosition = 0x4
        MoveActive = 0x8
        AccelPhase = 0x10
        DecelPhase = 0x20
        PositionCapture = 0x40
        CurrentClamp = 0x80
        BrakeOutput = 0x100
        MotionIsCw = 0x200
        MasterSlaveControl = 0x400
        CalActive = 0x800
        CalEnabled = 0x1000
        JoystickControl = 0x2000
        Homing = 0x4000
        MasterSuppress = 0x8000
        GauntryActive = 0x10000
        GauntryMaster = 0x20000
        AutofocusActive = 0x40000
        CommandFilterDone = 0x80000
        InPosition2 = 0x100000
        ServoControl = 0x200000
        CwEOTLimit = 0x400000
        CcwEOTLimit = 0x800000
        HomeLimit = 0x1000000
        MarkerInput = 0x2000000
        HallAInput = 0x4000000
        HallBInput = 0x8000000
        HallCInput = 0x10000000
        SineEncoderError = 0x20000000
        CosineEncoderError = 0x40000000
        ESTOPInput = 0x80000000

    def _pre_format(self, message: str) -> str:
        status_char = message[0]
        _check_fault(status_char)
        return message[1:]

    status = flag_control(
        AxisStatus,
        """Returns the current status of the axis.""",
        'AXISSTATUS({ch})',
        None,
        pre_format=_pre_format,
    )

    faults = flag_control(
        AxisFault,
        """Returns the current fault of the axis.""",
        'AXISFAULT({ch})',
        None,
        pre_format=_pre_format,
    )

    enabled = basic_control(
        bool,
        """Enables/disables the axis.""",
        'AXISSTATUS({ch})',
        '%s {ch}',
        get_format=lambda x: (int(x) & (1 << AxisControl.AxisStatus.Enabled.value)) != 0,
        set_format=lambda x: 'ENABLE' if x else 'DISABLE',
        pre_format=_pre_format,
        response=ignore,
    )

    position = basic_control(
        float,
        """Returns the current position of the axis.""",
        'PFBK({ch})',
        None,
        pre_format=_pre_format,
    )

    target_position = basic_control(
        float,
        """Returns the current target position of the axis.""",
        'PCMD({ch})',
        None,
        pre_format=_pre_format,
    )

    program_offset = optional_control(
        float,
        """Sets the coordinate system of the current position to the specified value.""",
        None,
        'POSOFFSET %s',
        set_format=lambda x: 'CLEAR {ch}' if x is None else 'SET {ch}, ' + f'{x:g}',
        pre_format=_pre_format,
        response=ignore,
    )

    program_postition = basic_control(
        float,
        """Returns the current position using the specified offset of the axis.""",
        'PFBKPROG({ch})',
        pre_format=_pre_format,
    )

    program_target_postition = basic_control(
        float,
        """Returns the current target position using the specified offset of the axis.""",
        'PCMDPROG({ch})',
        pre_format=_pre_format,
    )

    def move_abs(self, position: float, rate: float | None = None) -> None:
        command = ('MOVEABS {ch} ' + str(position)) + ('' if rate is None else (' {ch}F ' + str(rate)))
        status_char = self.query(command)
        _check_fault(status_char)

    def move_inc(self, delta: float, rate: float | None = None) -> None:
        command = ('MOVEINC {ch} ' + str(delta)) + ('' if rate is None else (' {ch}F ' + str(rate)))
        status_char = self.query(command)
        _check_fault(status_char)

    def reset_faults(self) -> None:
        status_char = self.query('FAULTACK({ch})')
        _check_fault(status_char)


class AerotechEnsemble(Instrument):
    adapter_options: ClassVar = {
        VISAAdapter: {
            'read_termination': '\n',
            'write_termination': '\n',
        }
    }

    class WaitMode(StrEnum):
        NoWait = 'NOWAIT'
        MoveDone = 'MOVEDONE'
        InPos = 'INPOS'

    def _pre_format(self, message: str) -> str:
        status_char = message[0]
        _check_fault(status_char)
        return message[1:]

    version = basic_control(
        str,
        """Get version of the device""",
        'VERSION',
        None,
        pre_format=_pre_format,
    )

    mode = enum_control(
        WaitMode,
        """Sets the wait mode for movment commands.""",
        None,
        'WAIT MODE %s',
        pre_format=_pre_format,
        response=ignore,
    )

    axes = AxisControl.make_dynamic()
