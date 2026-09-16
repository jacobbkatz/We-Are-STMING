#include "Arduino.h"
#include <SPI.h>
#include "EfficientStepper.hpp"

/**************************************************************************/
/*
    Constructor
*/
/**************************************************************************/

EfficientStepper::EfficientStepper(int number_of_steps, int motor_pin_1, int motor_pin_2,
                                   int motor_pin_3, int motor_pin_4) : _stepper_motor(Stepper(number_of_steps, motor_pin_1, motor_pin_2, motor_pin_3, motor_pin_4))
{
    _number_of_steps = number_of_steps;
    _stepper_motor_pins[0] = motor_pin_1;
    _stepper_motor_pins[1] = motor_pin_2;
    _stepper_motor_pins[2] = motor_pin_3;
    _stepper_motor_pins[3] = motor_pin_4;
    _stepper_motor_enabled = true;
}

void EfficientStepper::_save_status()
{
    if (_stepper_motor_enabled)
    // If the motor is already disabled, then we should not try to read the current pins;
    {
        for (int i = 0; i < 4; ++i)
        {
            _stepper_motor_status[i] = digitalRead(_stepper_motor_pins[i]);
        }
    }
}

void EfficientStepper::enable()
{
    for (int i = 0; i < 4; ++i)
    {
        digitalWrite(_stepper_motor_pins[i], _stepper_motor_status[i]);
    }

    _stepper_motor_enabled = true;
}

void EfficientStepper::disable()
{
    _save_status();
    for (int i = 0; i < 4; ++i)
    {
        digitalWrite(_stepper_motor_pins[i], LOW);
    }
    _stepper_motor_enabled = false;
}

void EfficientStepper::step(int steps)
{
    // FIX 2026-09-16, STATUS.md fault 3. This used to enable the coils and never
    // switch them off again: disable() was called only from approach(), on
    // success. After any MTMV the motor sat powered and heated the scan head,
    // which Berard warns makes the scanner drift within minutes. The 28BYJ-48 is
    // geared and holds position unpowered, so the coils are now switched off
    // after every move. disable() saves the coil pattern and enable() restores
    // it, so the next move carries on from the same phase.
    //
    // Uploaded and bench-tested 2026-09-16: the driver LEDs go dark after a move,
    // where the old firmware left two lit.
    if (steps == 0)
    {
        // Nothing to move. Do not pulse the coils on; just make sure they are off.
        if (_stepper_motor_enabled)
        {
            disable();
        }
        return;
    }
    if (!_stepper_motor_enabled)
    {
        enable();
    }
    _stepper_motor.step(steps);
    _total_steps = _total_steps + steps;

    // Stepper::step() returns the moment it has energised the LAST step's coil
    // pattern, before the rotor has had time to move there. Cutting the coils
    // at once could lose that step, so wait one step period first: at the
    // firmware's setSpeed(2) and 2048 steps per revolution that is about 15 ms.
    unsigned long settle_ms = 30; // fallback if setSpeed() was never called
    if (_speed_rpm > 0 && _number_of_steps > 0)
    {
        unsigned long step_period_us = 60UL * 1000UL * 1000UL / _number_of_steps / _speed_rpm;
        settle_ms = (step_period_us + 999UL) / 1000UL + 5UL;
    }
    delay(settle_ms);
    disable();
}

void EfficientStepper::setSpeed(long speed)
{
    _speed_rpm = speed;
    _stepper_motor.setSpeed(speed);
}

int EfficientStepper::get_total_steps()
{
    return _total_steps;
}

void EfficientStepper::reset()
{
    _total_steps = 0;
}