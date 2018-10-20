#!/usr/bin/env python3

# line_follower.py

# Import the EV3-robot library
from time   import sleep
from random import choice, randint

from ev3dev2.motor import OUTPUT_B, OUTPUT_A, LargeMotor, MediumMotor
from ev3dev2.sensor.lego import InfraredSensor, TouchSensor
from ev3dev2.button import Button
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
from ev3dev2.sensor.lego import ColorSensor

print('Robot Starting')

class LineFollower:
    # Constructor
    def __init__(self):
        self.btn = Button()

    # Main method
    def run(self):

        # sensors
        cs = ColorSensor()   # measures light intensity
        ir = InfraredSensor()

        cs.mode = 'COL-REFLECT'  # measure light intensity

        # motors
        lm = LargeMotor('outC');  assert lm.connected  # left motor
        rm = LargeMotor('outB');  assert rm.connected  # right motor
        mm = MediumMotor('outA'); assert mm.connected  # medium motor

        speed = 360/4  # deg/sec, [-1000, 1000]
        dt = 500       # milliseconds
        stop_action = "coast"

        # PID tuning
        Kp = 1  # proportional gain
        Ki = 0  # integral gain
        Kd = 0  # derivative gain

        integral = 0
        previous_error = 0

        # initial measurment
        target_value = cs.value()

        # Start the main loop
        while not self.btn.any():

            # deal with obstacles
            distance = ir.proximity() # convert mm to cm

            if distance <= 5:  # sweep away the obstacle
                mm.run_timed(time_sp=600, speed_sp=+150, stop_action="hold").wait()
                mm.run_timed(time_sp=600, speed_sp=-150, stop_action="hold").wait()

            # Calculate steering using PID algorithm
            error = target_value - cs.value()
            integral += (error * dt)
            derivative = (error - previous_error) / dt

            # u zero:     on target,  drive forward
            # u positive: too bright, turn right
            # u negative: too dark,   turn left

            u = (Kp * error) + (Ki * integral) + (Kd * derivative)

            # limit u to safe values: [-1000, 1000] deg/sec
            if speed + abs(u) > 1000:
                if u >= 0:
                    u = 1000 - speed
                else:
                    u = speed - 1000

            # run motors
            if u >= 0:
                lm.run_timed(time_sp=dt, speed_sp=speed + u, stop_action=stop_action)
                rm.run_timed(time_sp=dt, speed_sp=speed - u, stop_action=stop_action)
                sleep(dt / 1000)
            else:
                lm.run_timed(time_sp=dt, speed_sp=speed - u, stop_action=stop_action)
                rm.run_timed(time_sp=dt, speed_sp=speed + u, stop_action=stop_action)
                sleep(dt / 1000)

            previous_error = error

            # Check if buttons pressed (for pause or stop)
            if not self.btn.down:  # Stop
                print("Exit program... ")
                break
            elif not self.btn.left:  # Pause
                print("[Pause]")
                self.pause()

    # 'Pause' method
    def pause(self, pct=0.0, adj=0.01):
        while self.btn.right or self.btn.left:  # ...wait 'right' button to unpause
            Leds.set_color(Leds.LEFT, Leds.AMBER, pct)
            Leds.set_color(Leds.RIGHT, Leds.AMBER, pct)
            if (pct + adj) < 0.0 or (pct + adj) > 1.0:
                adj = adj * -1.0
            pct = pct + adj

        print("[Continue]")
        Leds.set_color(Leds.LEFT, Leds.GREEN)
        Leds.set_color(Leds.RIGHT, Leds.GREEN)


# Main function
robot = LineFollower()
robot.run()