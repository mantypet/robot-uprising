#!/usr/bin/env python3

# Program for a motor test

import ev3dev2.auto as ev3
import time

m = ev3.LargeMotor('outA')
m.run_timed(time_sp=3000, speed_sp=500)

time.sleep(2)
ev3.Sound().speak('Hello world').wait()
