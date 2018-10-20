from ev3dev2.motor import MoveTank

class CustomMoveTank(MoveTank):


    def turn(self, degrees):

        degrees = degrees * 15

        negative_turn = degrees < 0
        if negative_turn:
            degrees = -degrees

        speed = -60 if negative_turn else 60

        rotations = (degrees - degrees % 360) / 360
        degrees = degrees - rotations * 360

        # Set all parameters
        self.left_motor.on_for_rotations(speed, rotations, block=False)
        self.right_motor.on_for_rotations(-speed, rotations, block=True)
        self.left_motor.on_for_degrees(speed, degrees=degrees, block=False)
        self.right_motor.on_for_degrees(-speed, degrees=degrees, block=False)
