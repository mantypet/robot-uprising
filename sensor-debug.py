#!/usr/bin/env python3

# This program is used for reading different sensor values
# using a sensor debugger class..

from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sound import Sound

from utils.sensor_debugger import Debugger


Sound().beep()
debugger = Debugger()
debugger.run()
