#!/usr/bin/env python3

# line_follower.py

# Import the EV3-robot library
from time   import sleep
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
motors = [LargeMotor(address) for address in (OUTPUT_B, OUTPUT_C)]

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
    for m in motors:
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
    #if ts.is_pressed
    rand = random.randint(0,9)
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

    sound.speak(text,volume=1000)

start()

speed = - 360/4 
dt = 500       # milliseconds
stop_action = "coast"

# PID tuning
Kp = 1  # proportional gain
Ki = 0  # integral gain
Kd = 0  # derivative gain

integral = 0
previous_error = 0

target_value = color_sensor.value()

while not btn.any():
    #insult_random()

    # deal with obstacles
    distance = ir.proximity # convert mm to cm
    if distance <= 5:  # sweep away the obstacle
        backup()

    sound.speak('target: %d value: %d' % (target_value,color_sensor.value()))
    print(color_sensor.color)

    # Calculate steering using PID algorithm
    error = target_value - color_sensor.value()
    integral += (error * dt)
    derivative = (error - previous_error) / dt

    u = (Kp * error) + (Ki * integral) + (Kd * derivative)

    # limit u to safe values: [-1000, 1000] deg/sec
    if speed + abs(u) > 1000:
        if u >= 0:
            u = 1000 - speed
        else:
            u = speed - 1000

    # run motors
    if u >= 0:
        motors[0].run_timed(time_sp=dt, speed_sp=speed - u, stop_action=stop_action)
        motors[1].run_timed(time_sp=dt, speed_sp=speed + u, stop_action=stop_action)
        #sleep(dt / 1000)
    else:
        motors[0].run_timed(time_sp=dt, speed_sp=speed + u, stop_action=stop_action)
        motors[1].run_timed(time_sp=dt, speed_sp=speed - u, stop_action=stop_action)
        #sleep(dt / 1000)

    previous_error = error
