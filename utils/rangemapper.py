
# This algorithm was written for solving metal rod
# forest. It was abandoned as the robot was too big to rotate in the forest.
# Possible fix for this was to make the infrared sensor rotate instead.
# Unfortunately due to time constraints the code was not modified.

from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent, MoveTank, MoveSteering
from ev3dev2.motor import SpeedDPS, SpeedRPM, SpeedRPS, SpeedDPM
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor
from ev3dev2.led import Leds
from ev3dev2.display import Display
from ev3dev2.button import Button
from ev3dev2.sound import Sound

from tank.custom_tank import CustomMoveTank

from time import sleep
import math


class Reading:

    def __init__(self, degree, dist):
        self.degree = degree
        self.dist = dist


class RangeMapper:

    # sensor location determines turn radius of the sensor location in cm
    # thresehold determines how large space is required for a heading to be allowed
    def __init__(self, sensor_turn_radius=14, space_threshold=22):
        self.sensor_turn_radius = sensor_turn_radius

    def measure(self):
        infra = InfraredSensor(INPUT_2)

        tank = CustomMoveTank(OUTPUT_B, OUTPUT_C)

        readings = []

        # Mittaa etäisyys kaikissa suunnissa
        tank.turn(-90)
        for i in range(0, 34):
            dist = infra.proximity
            readings.append(Reading(i * 5, self.sensor_turn_radius + dist))
            tank.turn(5)
            sleep(0.1)

        # Return to original position
        tank.turn(-90)

        return readings

    def findGap(self):
        readings = self.measure()

        largest_gap_reading = None
        largest_gap = 0.0

        last_close = readings[0]
        for i in range(1, len(readings)):
            reading = readings[i]
            degree1 = last_close.degree
            degree2 = reading.degree
            alpha = degree2 - degree1

            p1 = last_close.dist
            p2 = reading.dist
            found_closer = p1 > p2
            closest_distance = p2 if found_closer else p1

            # Check if current value is closer than last close value.
            if last_close.dist > closest_distance:
                if found_closer:
                    last_close = reading

            gap = 2 * closest_distance * math.sin(alpha/2)

            # Calculate long side of the distance triangle
            d1 = p1 * math.cos(alpha / 2)
            d2 = p2 * math.cos(alpha / 2)
            # Middle point between end of first distance triangle and second
            d = d2 - (d2-d1) / 2

            if largest_gap_reading == None or gap > largest_gap:
                largest_gap_reading = Reading(degree1 + alpha/2, d)
                largest_gap = gap

        return Reading(largest_gap_reading.degree - 90, largest_gap_reading.dist)
