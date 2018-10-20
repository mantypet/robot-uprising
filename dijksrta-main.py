#!/usr/bin/env python3
from labyrinth.labyrinth_solver import *
from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank, MoveSteering
from ev3dev2.motor import SpeedDPS, SpeedRPM, SpeedRPS, SpeedDPM
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor
from ev3dev2.led import Leds
from ev3dev2.display import Display
from ev3dev2.button import Button
from ev3dev2.sound import Sound
from tank.custom_tank import CustomMoveTank

# class DijkstraMain():

def drive(currow, curcol, prevrow, prevcol, index):
    global heading
    if prevrow - currow < 0:  # want to move south
        if heading == 3:  # west
            tank.turn(-90)  # kaanna 90 astetta vasemmalle
            heading = (heading - 1) % 4
        elif heading == 1:  # east
            tank.turn(90)  # kaanna 90 astetta oikealle
            heading = (heading + 1) % 4
        # liiku eteenpain
        tank.move_cm(30)
    elif prevrow - currow > 0:  # want to move north
        if heading == 3:  # west
            tank.turn(90)  # kaanna 90 astetta oikealle
            heading = (heading + 1) % 4
        elif heading == 1:  # east
            tank.turn(-90)  # kaanna 90 astetta vasemmalle
            heading = (heading - 1) % 4
        # liiku eteenpain
        tank.move_cm(30)
    elif prevcol - curcol < 0:  # want to move west
        if heading == 0:  # north
            tank.turn(-90)  # kaanna 90 astetta vasemmalle
            heading = (heading - 1) % 4
        elif heading == 2:  # south
            tank.turn(90)  # kaanna oikealle
            heading = (heading + 1) % 4
        # liiku eteenpain
        tank.move_cm(30)
    elif prevcol - curcol > 0:  # right / east
        if heading == 0:  # north
            tank.turn(90)  # kaanna 90 astetta oikealle
            heading = (heading + 1) % 4
        elif heading == 2:  # south
            tank.turn(90)  # kaanna vasemmalle
            heading = (heading - 1) % 4
        # liiku eteenpain
        tank.move_cm(30)

start = 34
goal = 21
dij = Dijkstra(start, goal)
coordinates = dij.dij()
prevrow = coordinates[0][0]
prevcol = coordinates[0][1]

currow = coordinates[1][0]
curcol = coordinates[1][0]

tank = CustomMoveTank(OUTPUT_B, OUTPUT_C)

heading = 1  # 0 = north, 1 = east, 2 = south, 3 = west
index = 2

while 6*currow+curcol != goal:
    drive(currow, curcol, prevrow, prevcol, index)
    prevrow = currow
    prevcol = currow
    currow = coordinates[index][0]
    curcol = coordinates[index][1]
    index += 1


# Second goal
start = 21
goal = 5
dij = Dijkstra(start, goal)
coordinates = dij.dij()
prevrow = coordinates[0][0]
prevcol = coordinates[0][1]

currow = coordinates[1][0]
curcol = coordinates[1][0]

while 6*currow+curcol != goal:
    drive(currow, curcol, prevrow, prevcol, index)
    prevrow = currow
    prevcol = currow
    currow = coordinates[index][0]
    curcol = coordinates[index][1]
    index += 1
