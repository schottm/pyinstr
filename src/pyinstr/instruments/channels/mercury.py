"""
This file is part of PyINSTR.

:copyright: 2025 by Marco Schott.
:license: MIT, see LICENSE for more details.
"""

from collections.abc import Callable
from enum import StrEnum

from pyinstr import BoolFormat, Channel, MessageProtocol, basic_control, bool_control, enum_control, ignore
from pyinstr.validator import in_range, in_range_inc


def _pre_format_quantity(quantity: str) -> Callable[[MessageProtocol, str], str]:
    def wrapper(_: MessageProtocol, value: str) -> str:
        return value.split(':')[-1].replace(quantity, '')

    return wrapper


def _pre_format(_: MessageProtocol, value: str) -> str:
    return value.split(':')[-1]


class TemperatureSensor(Channel[MessageProtocol]):
    temperature = basic_control(
        float,
        """Get the measured temperature, in Kelvin.""",
        'READ:DEV:{ch}:TEMP:SIG:TEMP',
        None,
        pre_format=_pre_format_quantity('K'),
    )

    voltage = basic_control(
        float,
        """Get the sensor voltage, in Volts.""",
        'READ:DEV:{ch}:TEMP:SIG:VOLT',
        None,
        pre_format=_pre_format_quantity('V'),
    )


class TemperatureLoopControl(TemperatureSensor):
    pid_enabled = bool_control(
        BoolFormat.OnOff,
        """Control whether the control-loop heater is controlled by
        the PID loop (``True``) or the manual heater percentage (``False``).""",
        'READ:DEV:{ch}:TEMP:LOOP:ENAB',
        'SET:DEV:{ch}:TEMP:LOOP:ENAB:%s',
        pre_format=_pre_format,
        response=ignore,
    )

    proportional = basic_control(
        float,
        """Control the proportional term, P, of the control loop.""",
        'READ:DEV:{ch}:TEMP:LOOP:P',
        'SET:DEV:{ch}:TEMP:LOOP:P:%g',
        pre_format=_pre_format,
        response=ignore,
    )

    integral = basic_control(
        float,
        """Control the integral term, I, of the control loop.""",
        'READ:DEV:{ch}:TEMP:LOOP:I',
        'SET:DEV:{ch}:TEMP:LOOP:I:%g',
        pre_format=_pre_format,
        response=ignore,
    )

    derivative = basic_control(
        float,
        """Control the derivative term, D, of the control loop.""",
        'READ:DEV:{ch}:TEMP:LOOP:D',
        'SET:DEV:{ch}:TEMP:LOOP:D:%g',
        pre_format=_pre_format,
        response=ignore,
    )

    temperature_setpoint = basic_control(
        float,
        """Control the control loop temperature setpoint, in Kelvin (in the range
        0 to 2000).""",
        'READ:DEV:{ch}:TEMP:LOOP:TSET',
        'SET:DEV:{ch}:TEMP:LOOP:TSET:%g',
        pre_format=_pre_format_quantity('K'),
        validate=in_range(0.0, 2000.0),
        response=ignore,
    )

    heater = basic_control(
        float,
        """Control the heater when output configured to manual mode
        (in the range 0 to 1).""",
        'READ:DEV:{ch}:TEMP:LOOP:HSET',
        'SET:DEV:{ch}:TEMP:LOOP:HSET:%g',
        get_format=lambda x: float(x) * 1e-2,
        set_format=lambda x: x * 1e2,
        pre_format=_pre_format,
        validate=in_range_inc(0.0, 1.0),
        response=ignore,
    )

    ramp_rate = basic_control(
        float,
        """Control the control loop ramp rate, in K/min, if enabled (in the
        range 0 to 100000).""",
        'READ:DEV:{ch}:TEMP:LOOP:RSET',
        'SET:DEV:{ch}:TEMP:LOOP:RSET:%g',
        pre_format=_pre_format_quantity('K/m'),
        validate=in_range(0.0, 100000.0),
        response=ignore,
    )

    ramp_enabled = bool_control(
        BoolFormat.OnOff,
        """Control whether the temperature ramping function is enabled (``True``) or
        disabled (``False``).""",
        'READ:DEV:{ch}:TEMP:LOOP:RENA',
        'SET:DEV:{ch}:TEMP:LOOP:RENA:%s',
        pre_format=_pre_format,
        response=ignore,
    )


class HeaterControl(Channel[MessageProtocol]):
    voltage = basic_control(
        float,
        """Get the heater excitation voltage, in Volts.""",
        'READ:DEV:{ch}:HTR:SIG:VOLT',
        None,
        pre_format=_pre_format_quantity('V'),
    )

    current = basic_control(
        float,
        """Get the heater excitation current, in Amps.""",
        'READ:DEV:{ch}:HTR:SIG:CURR',
        None,
        pre_format=_pre_format_quantity('A'),
    )

    power = basic_control(
        float,
        """Get the heater power dissipation, in Watts.""",
        'READ:DEV:{ch}:HTR:SIG:POWR',
        None,
        pre_format=_pre_format_quantity('W'),
    )

    voltage_limit = basic_control(
        float,
        """Control the voltage limit of the heater output, in Volts (float strictly
        from 0 to 40).""",
        'READ:DEV:{ch}:HTR:VLIM',
        'SET:DEV:{ch}:HTR:VLIM:%g',
        pre_format=_pre_format,
        validate=in_range_inc(0.0, 40.0),
        response=ignore,
    )

    resistance = basic_control(
        float,
        """Control the programmed heater resistance, in Ohms (float strictly
        in the range of 10 to 2000).""",
        'READ:DEV:{ch}:HTR:RES',
        'SET:DEV:{ch}:HTR:RES:%g',
        pre_format=_pre_format,
        validate=in_range_inc(10.0, 2000.0),
        response=ignore,
    )

    max_power = basic_control(
        float,
        """Get the provisional maximum power of the heater, in Watts.""",
        'READ:DEV:{ch}:HTR:PMAX',
        None,
        pre_format=_pre_format,
    )


class LevelSensor(Channel[MessageProtocol]):
    he_level = basic_control(
        float,
        """Get the measured liquid helium fill level (0 to 1)""",
        'READ:DEV:{ch}:LVL:SIG:HEL:LEV',
        None,
        get_format=lambda v: float(v) * 1e-2,
        pre_format=_pre_format_quantity('%'),
    )

    n2_level = basic_control(
        float,
        """Get the measured liquid nitrogen fill level (0 to 1)""",
        'READ:DEV:{ch}:LVL:SIG:NIT:LEV',
        None,
        get_format=lambda v: float(v) * 1e-2,
        pre_format=_pre_format_quantity('%'),
    )


class MagnetControl(Channel[MessageProtocol]):
    class Action(StrEnum):
        Hold = 'HOLD'
        RampToZero = 'RTOZ'
        RampToSet = 'RTOS'
        ClampOutput = 'CLMP'
        Unknown = 'N/A'

    field = basic_control(
        float,
        """Get the most recent field reading, in Tesla.""",
        'READ:DEV:{ch}:PSU:SIG:FLD',
        None,
        pre_format=_pre_format_quantity('T'),
    )

    persist_field = basic_control(
        float,
        """Get the most recent persist field reading, in Tesla.""",
        'READ:DEV:{ch}:PSU:SIG:PFLD',
        None,
        pre_format=_pre_format_quantity('T'),
    )

    # TODO : add range validation
    field_setpoint = basic_control(
        float,
        """Control the target magnetic field, in Tesla (float strictly in range -CLIM/ATOB and CLIM/ATOB)""",
        'READ:DEV:{ch}:PSU:SIG:FSET',
        'SET:DEV:{ch}:PSU:SIG:FSET:%g',
        pre_format=_pre_format_quantity('T'),
        response=ignore,
    )

    field_rate_setpoint = basic_control(
        float,
        """Control the target magnetic field rate, in Tesla/min (float strictly in range 0.0 to 50)""",
        'READ:DEV:{ch}:PSU:SIG:RFST',
        'SET:DEV:{ch}:PSU:SIG:RFST:%g',
        pre_format=_pre_format_quantity('T/m'),
        validate=in_range_inc(0.0, 50.0),
        response=ignore,
    )

    heater_enabled = bool_control(
        BoolFormat.OnOff,
        """Get/set the heater status.""",
        'READ:DEV:{ch}:PSU:SIG:SWHT',
        'SET:DEV:{ch}:PSU:SIG:SWHT:%s',
        pre_format=_pre_format,
        response=ignore,
    )

    action = enum_control(
        Action,
        """Get/set the PSU action status.""",
        'READ:DEV:{ch}:PSU:SIG:ACTN',
        'SET:DEV:{ch}:PSU:SIG:ACTN:%s',
        pre_format=_pre_format,
        response=ignore,
    )


class FlowControl(Channel[MessageProtocol]):
    flow = basic_control(
        float,
        """Set the gas flow manually.""",
        'READ:DEV:{ch}:AUX:SIG:PERC',
        'SET:DEV:{ch}:AUX:LOOP:FSET:%g',
        get_format=lambda v: float(v) * 1e-2,
        set_format=lambda v: v * 1e2,
        pre_format=_pre_format_quantity('%'),
        validate=in_range_inc(0.0, 1.0),
        response=ignore,
    )
