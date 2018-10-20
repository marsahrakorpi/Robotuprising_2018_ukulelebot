#!/usr/bin/env python3

import logging
import sys
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, MediumMotor, MoveTank
from time import sleep

# ============
# Tank classes
# ============
class UkuleleControlledTank(MoveTank):

    def __init__(self, left_motor_port, right_motor_port, polarity='inversed', speed=400, channel=1):
        MoveTank.__init__(self, left_motor_port, right_motor_port)
        self.set_polarity(polarity)

        left_motor = self.motors[left_motor_port]
        right_motor = self.motors[right_motor_port]
        self.speed_sp = speed

        # 
        self.remote = InfraredSensor()
        self.remote.on_channel1_top_left = self.make_move(left_motor, self.speed_sp)
        self.remote.on_channel1_bottom_left = self.make_move(left_motor, self.speed_sp* -1)
        self.remote.on_channel1_top_right = self.make_move(right_motor, self.speed_sp)
        self.remote.on_channel1_bottom_right = self.make_move(right_motor, self.speed_sp * -1)
        self.channel = channel

    def make_move(self, motor, dc_sp):
        def move(state):
            if state:
                motor.run_forever(speed_sp=dc_sp)
            else:
                motor.stop()
        return move

    def main(self):

        try:
            while True:
                self.remote.process()
                sleep(0.01)

        # Exit cleanly so that all motors are stopped
        except (KeyboardInterrupt, Exception) as e:
            log.exception(e)
            self.stop()


class EV3D4WebControlled(UkuleleControlledTank):

    def __init__(self, medium_motor=OUTPUT_C, left_motor=OUTPUT_A, right_motor=OUTPUT_B):
        UkuleleControlledTank.__init__(self, left_motor, right_motor)
        ''' self.medium_motor = MediumMotor(medium_motor)

        if not self.medium_motor.connected:
            log.error("%s is not connected" % self.medium_motor)
            sys.exit(1)

        self.medium_motor.reset() '''


if __name__ == '__main__':

    # Change level to logging.INFO to make less chatty
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s %(levelname)5s %(filename)s:%(lineno)5s - %(funcName)25s(): %(message)s")
    log = logging.getLogger(__name__)

    # Color the errors and warnings in red
    logging.addLevelName(logging.ERROR, "\033[91m  %s\033[0m" % logging.getLevelName(logging.ERROR))
    logging.addLevelName(logging.WARNING, "\033[91m%s\033[0m" % logging.getLevelName(logging.WARNING))

    log.info("Starting EV3D4")
    ev3d4 = EV3D4WebControlled()
    ev3d4.main()  # start the web server
    log.info("Exiting EV3D4")
