#!/usr/bin/env python3
__author__ = 'Anton Vanhoucke'

# This is a linux-specific module.
# It is required by the Button class, but failure to import it may be
# safely ignored if one just needs to run API tests on Windows.
import evdev

from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent, MoveTank, MoveSteering
from ev3dev2.sound import Sound
from time import sleep
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor
from ev3dev2.led import Leds
from ev3dev2.display import Display
from ev3dev2.button import Button

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
    return scale(value, (0, 255), (-100, 100))


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
closed = False
running = True

follow_line = False


class MotorThread(threading.Thread):
    def __init__(self):
        self.tank = MoveTank(OUTPUT_B, OUTPUT_C)
        threading.Thread.__init__(self)

    def run(self):
        while running:
            if follow_line:
                continue
            if speedL != 0 or speedR != 0:
                self.tank.on(-speedL, -speedR)
            else:
                self.tank.off()

        self.tank.off()


class ClawThread(threading.Thread):
    def __init__(self):
        self.claw = LargeMotor(OUTPUT_D)
        threading.Thread.__init__(self)

    def run(self):
        closed = False

        while running:
            if close_jaw and not self.claw.is_overloaded and not closed:
                closed = True
                self.claw.on_for_degrees(30, 5 * 360)
            elif not close_jaw and not self.claw.is_overloaded and closed:
                closed = False
                self.claw.on_for_degrees(-30, 2*360)
            else:
                self.claw.off()

        self.claw.off()


class LineFollowThread(threading.Thread):
    def __init__(self):
        self.claw = LargeMotor(OUTPUT_D)
        threading.Thread.__init__(self)

    def run(self):
        # valkoinen mitattu 70, harmaa mitattu 12, keskiarvo ^40

        # taustavari
        # ridColor = 20 # maalarinteippi
        ridColor = 40  # valkoinen paperi

        # Nopeus
        speed = 25
        counter_max = 5

        button = Button()
        colorS = ColorSensor(INPUT_3)
        sound = Sound()

        # ajaa eteenpain
        tank_pair = MoveTank(OUTPUT_B, OUTPUT_C)
        # kaantyy 2 sekunttia

        tank_pair.off()

        sound.beep()

        # Suoritussilmukka
        while True:
            intensity = colorS.reflected_light_intensity

            while (intensity > ridColor and follow_line):  # viivalla
                intensity = colorS.reflected_light_intensity
                tank_pair.on(50, 50)  # Eteenpäin
                counter_max = 5  # alustetaan viivanhaun sektorin leveys

            if (intensity <= ridColor and follow_line):  # Ei viivalla -> alusta viivanhakumuuttujat
                speed = -speed

            i = 0
            while (intensity <= ridColor and i < counter_max and follow_line):  # Ei viivalla ->
                intensity = colorS.reflected_light_intensity
                # vasemman ja oikean nopeudet, kääntyy vasemmalle
                tank_pair.on(speed, -speed)
                i += 1

            if follow_line:
                counter_max += counter_max


motor_thread = MotorThread()
motor_thread.setDaemon(True)
motor_thread.start()
claw_thread = ClawThread()
claw_thread.setDaemon(True)
claw_thread.start()
line_thread = LineFollowThread()
line_thread.setDaemon(True)
line_thread.start()

duck = MediumMotor(OUTPUT_A)
duck.on(20)

for event in gamepad.read_loop():  # this loops infinitely
    if event.type == 2 or event.type == 1 or event.type == 0:
        if event.value != 0:
            print("%s %s %s" % (event.type, event.code, event.value))
    if event.type == 3:  # A stick is moved
        # 5: R2
        # 2: L2
        # 0: L-stick X-axis
        # 1: L-stick Y-axis
        # 3: R-stick X-axis
        # 4: R-stick Y-axis

        # 304: X-button
        # 305: O-button
        # 307: Triangle
        # 308: square
        # 310: L1
        # 311: R1
        # 314: Select
        # 315: start

        if event.code == 1:  # Y axis on right stick
            speedL = scale_stick(event.value)
        if event.code == 4:
            speedR = scale_stick(event.value)
    if event.type == 1 and event.code == 304 and event.value == 1:
        close_jaw = True
    if event.type == 1 and event.code == 305 and event.value == 1:
        close_jaw = False
    if event.type == 1 and event.code == 307 and event.value == 1:
        follow_line = True
    if event.type == 1 and event.code == 308 and event.value == 1:
        follow_line = False
