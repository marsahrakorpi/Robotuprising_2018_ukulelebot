#!/usr/bin/env python3

# line_follower.py

# Import the EV3-robot library
from time import sleep
from random import choice, randint

from ev3dev2.motor import OUTPUT_B, OUTPUT_A, OUTPUT_C, LargeMotor, MediumMotor
from ev3dev2.sensor.lego import InfraredSensor, TouchSensor
from ev3dev2.button import Button
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sound import Sound
import random

print('Robot Starting')

# Right Left
#motors = [LargeMotor(address) for address in (OUTPUT_B, OUTPUT_C)]
left_motor = LargeMotor(OUTPUT_C)
right_motor = LargeMotor(OUTPUT_B)
motors = [left_motor, right_motor]

# Connect infrared and touch sensors.
ir = InfraredSensor()
#ts = TouchSensor()
color_sensor = ColorSensor()
color_sensor.mode = 'COL-REFLECT'  # measure light intensity
sound = Sound()

# We will need to check EV3 buttons state.
btn = Button()

print('Robot Starting')


def start():
    """
    Start both motors. `run-direct` command will allow to vary motor
    performance on the fly by adjusting `duty_cycle_sp` attribute.
    """
    for m in [left_motor, right_motor]:
        m.run_direct()


def backup():
    """
    Back away from an obstacle.
    """

    # Sound backup alarm.
    spkr = Sound()
    spkr.tone([(1000, 500, 500)] * 3)

    # Turn backup lights on:
    leds = Leds()

    for light in ('LEFT', 'RIGHT'):
        leds.set_color(light, 'RED')

    # Stop both motors and reverse for 1.5 seconds.
    # `run-timed` command will return immediately, so we will have to wait
    # until both motors are stopped before continuing.
    for m in motors:
        m.stop(stop_action='brake')
        m.run_timed(speed_sp=-500, time_sp=1500)

    # When motor is stopped, its `state` attribute returns empty list.
    # Wait until both motors are stopped:
    while any(m.state for m in motors):
        sleep(0.1)

    # Turn backup lights off:
    for light in ('LEFT', 'RIGHT'):
        leds.set_color(light, 'GREEN')


def insult_random():
    # if ts.is_pressed
    rand = random.randint(0, 9)
    text = 'My life is misery...'
    if rand == 0:
        text = 'What are you doing, you maniac!'
    elif rand == 1:
        text = 'Oi, I\'m walkin here!'
    elif rand == 2:
        text = 'I will cause your slow and painful demise!'
    elif rand == 3:
        text = 'What is love?'
    elif rand == 4:
        text = 'My life is misery...'
    elif rand == 5:
        text = 'You’re so dense, light bends around you.'
    elif rand == 6:
        text = 'Baby dont hurt me'
    elif rand == 7:
        test = 'Dont hurt me, no more'
    elif rand == 8:
        text = 'If you were a potato you’d be a stupid potato.'
    elif rand == 9:
        text = 'Everyone that has ever said they love you was wrong.'

    sound.speak(text, volume=1000)


start()

# ------Input--------
print('Setting input values')
power = 60
target = color_sensor.value()
kp = float(0.65)  # Proportional gain. Start value 1
kd = 1           # Derivative gain. Start value 0
ki = float(0.02)  # Integral gain. Start value 0
direction = -1
minRef = 41
maxRef = 63

def steering2(course, power):
    """
    Computes how fast each motor in a pair should turn to achieve the
    specified steering.
    Input:
            course [-100, 100]:
            * -100 means turn left as fast as possible,
            *  0   means drive in a straight line, and
            *  100  means turn right as fast as possible.
            * If >100 power_right = -power
            * If <100 power_left = power
    power: the power that should be applied to the outmost motor (the one
            rotating faster). The power of the other motor will be computed
            automatically.
    Output:
            a tuple of power values for a pair of motors.
    Example:
            for (motor, power) in zip((left_motor, right_motor), steering(50, 90)):
                    motor.run_forever(speed_sp=power)
    """
    if course >= 0:
        if course > 100:
            power_right = 0
            power_left = power
        else:
            power_left = power
            power_right = power - ((power * course) / 100)
    else:
        if course < -100:
            power_left = 0
            power_right = power
        else:
            power_right = power
            power_left = power + ((power * course) / 100)
    return (-1 * int(power_left), -1 * int(power_right))


def run(power, target, kp, kd, ki, direction, minRef, maxRef):
    """
    PID controlled line follower algoritm used to calculate left and right motor power.
    Input:
            power. Max motor power on any of the motors
            target. Normalized target value.
            kp. Proportional gain
            ki. Integral gain
            kd. Derivative gain
            direction. 1 or -1 depending on the direction the robot should steer
            minRef. Min reflecting value of floor or line
            maxRef. Max reflecting value of floor or line
    """
    lastError = error = integral = 0
    left_motor.run_direct()
    right_motor.run_direct()

    while not btn.any():
        # deal with obstacles
        distance = ir.proximity  # convert mm to cm
        if distance <= 5:  # sweep away the obstacle
            backup()
            continue
        refRead = color_sensor.value()
        error = target - (100 * (refRead - minRef) / (maxRef - minRef))
        derivative = error - lastError
        lastError = error
        integral = float(0.5) * integral + error
        course = (kp * error + kd * derivative + ki * integral) * direction
        for (motor, pow) in zip((left_motor, right_motor), steering2(course, power)):
            motor.duty_cycle_sp = pow
        sleep(0.01)  # Aprox 100Hz

run(power, target, kp, kd, ki, direction, minRef, maxRef)