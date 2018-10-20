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
        if rotations != 0:
            self.left_motor.on_for_rotations(speed, rotations, block=False)
            self.right_motor.on_for_rotations(-speed, rotations, block=True)
        if degrees != 0:
            self.left_motor.on_for_degrees(speed, degrees=degrees, block=False)
            self.right_motor.on_for_degrees(-speed,
                                            degrees=degrees, block=False)

    def move_cm(self, centimeters):
        degrees = centimeters * 108

        rotations = (degrees - degrees % 360) / 360
        degrees = degrees - rotations * 360
        speed = 60 if degrees > 0 else -60

        # Set all parameters
        if rotations != 0:
            self.left_motor.on_for_rotations(speed, rotations, block=False)
            self.right_motor.on_for_rotations(speed, rotations, block=True)
        if degrees != 0:
            self.left_motor.on_for_degrees(speed, degrees=degrees, block=False)
            self.right_motor.on_for_degrees(speed, degrees=degrees, block=False)
