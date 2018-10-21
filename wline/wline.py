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
ridColor = 20 # maalarinteippi
#ridColor = 40 # valkoinen paperi


# Nopeus
speed = 25

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

    while (intensity > ridColor):  # viivalla
        intensity = colorS.reflected_light_intensity
        tank_pair.on(50, 50)  # Eteenpäin
        counter_max = 5 # alustetaan viivanhaun sektorin leveys
    
    
    if (intensity <= ridColor): #Ei viivalla -> alusta viivanhakumuuttujat
        speed = -speed
    
    counter_max = 0
    i = 0
    while (intensity <= ridColor and i < counter_max): # Ei viivalla -> 
        intensity = colorS.reflected_light_intensity
        tank_pair.on(speed, -speed) # vasemman ja oikean nopeudet, kääntyy vasemmalle
        i += 1

    counter_max += counter_max
        