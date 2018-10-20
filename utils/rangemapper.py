from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank, MoveSteering
from ev3dev2.motor import SpeedDPS, SpeedRPM, SpeedRPS, SpeedDPM
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor
from ev3dev2.led import Leds
from ev3dev2.display import Display
from ev3dev2.button import Button
from ev3dev2.sound import Sound

class Reading:

    def __init__(self, degree, dist):
        self.degree = degree
        self.dist = dist

class RangeMapper:

    # sensor location determines turn radius in cm
    def __init__(self, sensor_turn_radius=6):
        self.sensor_turn_radius = sensor_turn_radius

    def measure(self):
        infra = InfraredSensor(INPUT_2)
        tank_pair = MoveTank(OUTPUT_B, OUTPUT_C)

        distances = []

        # Mittaa etäisyys kaikissa suunnissa
        # driver.turn(-90)
        for i in range(0, 180):
            dist = infra.distance
            distances.append(Reading(i, self.sensor_turn_radius + dist))
            # driver.turn(1)

        # Return to original position
        

        return distances

    def findGaps(self):
        distances = self.measure()
        print(distances)


