#!/usr/bin/env python3
from time import sleep
from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank, MoveSteering
from ev3dev2.motor import SpeedDPS, SpeedRPM, SpeedRPS, SpeedDPM
# degrees per second, rotations per minute, rotations per second, degrees per minute
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor
from ev3dev2.led import Leds
from ev3dev2.display import Display
from ev3dev2.button import Button
from ev3dev2.sound import Sound

# valkoinen mitattu 70, harmaa mitattu 12, keskiarvo ^40

# taustavari
ridColor = 40


button = Button()
colorS = ColorSensor(INPUT_3)
sound = Sound()

# ajaa eteenpain
tank_pair = MoveTank(OUTPUT_B, OUTPUT_C)
# kaantyy 2 sekunttia

tank_pair.off()

sound.beep()

while True:
    intensity = colorS.reflected_light_intensity

    if (intensity > ridColor):  # viivalla
        tank_pair.on(50, 50)  # vasemman ja oikean nopeudet, ajaa eteenpäin

    else:
        tank_pair.on_for_seconds(-25, 25, 2, brake = True, block = False) # vasemman ja oikean nopeudet, kääntyy vasemmalle
        tank_pair.on_for_seconds(25, -25, 2, brake = True, block = False)  # vasemman ja oikean nopeudet, kääntyy oikealle
