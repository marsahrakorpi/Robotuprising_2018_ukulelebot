#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds

from ev3dev2.sound import Sound
import random
# TODO: Add code here
print("hello world")
sound = Sound()
#sound.speak('Welcome to the E V 3 dev project!')

ts=TouchSensor()
def insult_random():
    #if ts.is_pressed
    rand = random.randint(0,3)
    
    if rand == 0:
      sound.speak('What are you doing, you maniac!')
    elif rand == 1:
      sound.speak('Oi, I\'m walkin here!')
    elif rand == 2:
      sound.speak('I will cause your slow and painful demise!')
    elif rand == 3:
      sound.speak('What is love?')
    else:
      sound.speak('My life is misery...')

#can call sinults with
#  if ts.is_pressed:
#    insult_random()


# drive in a turn for 5 rotations of the outer motor
# the first two parameters can be unit classes or percentages.
#tank_drive.on_for_rotations(SpeedPercent(50), SpeedPercent(75), 10)

# drive in a different turn for 3 seconds
#tank_drive.on_for_seconds(SpeedPercent(60), SpeedPercent(30), 3)

def drive_forward(time=10, speed=50, direction=0):
  tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)
  left_speed = max(min(speed * (1 - direction),100),-100)
  right_speed = max(min(speed * (1 + direction),100),-100)

  tank_drive.on_for_rotations(SpeedPercent(left_speed), SpeedPercent(right_speed), time)

def right_turn():
  drive_forward(1.35,50,2)

def left_turn():
  drive_forward(1.35,50,-2)

drive_forward(20,100,0)
right_turn()
drive_forward(5,100,0)

drive_forward(5,-100,0)
left_turn()
drive_forward(20,-100,0)


#drive_forward(50,100,0)
#drive_forward(10,-50,0)
#drive_forward(1,50,2)
#drive_forward(10,100,0)
#drive_forward(1000,50,-2)
#drive_forward(10,100,0)

