#!/usr/bin/env python3

# This program was written for the L turn quick challenge at the start.
# It turns left ALWAYS when black color is not under the color sensor

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, MoveTank
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.button import Button
from ev3dev2.sound import Sound

from time import sleep

button = Button()
colorS = ColorSensor(INPUT_4)
sound = Sound()

tank_pair = MoveTank(OUTPUT_B, OUTPUT_C)

tank_pair.off()

sound.beep()

while True:
    intensity = colorS.reflected_light_intensity

    if (intensity < 50):
        tank_pair.on(-50, -50)  # vasemman ja oikean nopeudet
    else:
        tank_pair.on(-50, 50)  # vasemman ja oikean nopeudet
