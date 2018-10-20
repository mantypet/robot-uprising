#!/usr/bin/env python3
__author__ = 'Anton Vanhoucke'

# This is a linux-specific module.
# It is required by the Button class, but failure to import it may be
# safely ignored if one just needs to run API tests on Windows.
import evdev

from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent, MoveTank, MoveSteering
from ev3dev2.sound import Sound

import threading
import math

## Some helpers ##
def scale(val, src, dst):
    """
    Scale the given value from the scale of src to the scale of dst.

    val: float or int
    src: tuple
    dst: tuple

    example: print(scale(99, (0.0, 99.0), (-1.0, +1.0)))
    """
    return (float(val - src[0]) / (src[1] - src[0])) * (dst[1] - dst[0]) + dst[0]

def scale_stick(value):
    return scale(value,(0,255),(-100,100))

## Initializing ##
sound = Sound()

sound.beep()
print("Finding ps3 controller...")
devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
for device in devices:
    if device.name == 'PLAYSTATION(R)3 Controller':
        ps3dev = device.fn

gamepad = evdev.InputDevice(ps3dev)

sound.speak("Ready")

speedL = 0
speedR = 0
close_jaw = True
running = True

class MotorThread(threading.Thread):
    def __init__(self):
        self.tank = MoveTank(OUTPUT_B, OUTPUT_C)
        self.claw = LargeMotor(OUTPUT_D)
        threading.Thread.__init__(self)

    def run(self):
        print("Engine running!")
        while running:
            if speedL != 0 or speedR != 0:
                self.tank.on(-speedL, -speedR)
            else:
                self.tank.off()
            if close_jaw and not self.claw.is_overloaded:
                self.claw.on(30)
            elif not close_jaw and not self.claw.is_overloaded:
                self.claw.on(-30)
            else:
                self.claw.off()
            

        self.tank.off()

motor_thread = MotorThread()
motor_thread.setDaemon(True)
motor_thread.start()


for event in gamepad.read_loop():   #this loops infinitely
    if event.type == 2 or event.type == 1 or event.type == 0:
        if event.value != 0:
            print("%s %s %s" % (event.type, event.code, event.value))
    if event.type == 3:             #A stick is moved
        # 5: R2
        # 2: L2
        #0: L-stick X-axis
        #1: L-stick Y-axis
        #3: R-stick X-axis
        #4: R-stick Y-axis

        #304: X-button
        #305: O-button
        #307: Triangle
        #308: square
        #310: L1
        #311: R1
        #314: Select
        #315: start

        if event.code == 1:         #Y axis on right stick
            speedL = scale_stick(event.value)
        if event.code == 4:
            speedR = scale_stick(event.value)
    if event.type == 1 and event.code == 304 and event.value == 1:
        close_jaw = True
    if event.type == 1 and event.code == 305 and event.value == 1:
        close_jaw = False
