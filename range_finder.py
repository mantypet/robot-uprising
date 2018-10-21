#!/usr/bin/env python3

# This program uses an algorithm that was written for solving metal rod
# forest. It was abandoned as the robot was too big to rotate in the forest.
# Possible fix for this was to make the infrared sensor rotate instead.
# Unfortunately due to time constraints the code was not modified.

from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank, MoveSteering
from ev3dev2.motor import SpeedDPS, SpeedRPM, SpeedRPS, SpeedDPM
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor
from ev3dev2.led import Leds
from ev3dev2.display import Display
from ev3dev2.button import Button
from ev3dev2.sound import Sound

from time import sleep
from tank.custom_tank import CustomMoveTank

from utils.rangemapper import RangeMapper, Reading

sound = Sound()
button = Button()
mapper = RangeMapper()

tank = CustomMoveTank(OUTPUT_B, OUTPUT_C)

sound.beep()

while not button.enter:
    sleep(1)

while not button.backspace:
    gap_heading = mapper.findGap()
    tank.turn(gap_heading.degree)
    tank.move_cm(gap_heading.dist)
