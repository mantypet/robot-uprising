# Sensor debugging utility that assumes all sensors to be attached.
# Can be used to read values in certain environments.

from ev3dev2.button import Button

from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor
from ev3dev2.display import Display
from ev3dev2.sound import Sound

from time import sleep

class Debugger:

    def __init__(self, in1=INPUT_1, in2=INPUT_2, in3=INPUT_3, in4=INPUT_4):
        self.in1 = in1
        self.in2 = in2
        self.in3 = in3
        self.in4 = in4

    def run(self):
        button = Button()

       #ultra = UltrasonicSensor(self.in1)
        infra = InfraredSensor(self.in2)
        touch = TouchSensor(self.in3)
        color = ColorSensor(self.in4)

        self.mode = 1
        self.max = 5
        while not button.backspace:
            #if self.mode == 1:
             #   print("U,Distance: %d" % ultra.distance_centimeters)
            if self.mode == 2:
                print("I,Proximity: %d" % infra.proximity)
            if self.mode == 3:
                print("T,Pressed: %s" % ("Yes" if touch.is_pressed else "No"))
            if self.mode == 4:
                print("C,Reflected light: %d" % color.reflected_light_intensity)
            if self.mode == 5:
                print("C,Ambient light: %d" % color.ambient_light_intensity)
            if button.right:
                self.change_mode()
                

    def change_mode(self):
        Sound().beep()

        self.mode = self.mode + 1
        if self.mode > self.max:
            self.mode = 1
        sleep(5)
