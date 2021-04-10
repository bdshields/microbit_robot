from microbit import pin14, pin15, pin2, pin11
from machine import time_pulse_us


class ultraSonic:
    def __init__(self):
        self.trig = pin14
        self.echo = pin15
        self.trig.write_digital(0)
        self.echo.read_digital()

    def getDistance(self):
        self.trig.write_digital(1)
        self.trig.write_digital(0)
        micros = time_pulse_us(self.echo, 1)
        t_echo = micros / 1000000
        dist_cm = (t_echo / 2) * 34300
        return dist_cm

class ir_detector:
    def __init__(self):
        self.left = pin2
        self.right = pin11
        self.left.read_digital()
        self.right.read_digital()
        self.left.set_pull(0)
        self.right.set_pull(0)
    
    def detectRight(self):
        return self.right.read_digital() == 0
    def clearRight(self):
        return self.right.read_digital() != 0

    def detectLeft(self):
        return self.left.read_digital() == 0
    def clearLeft(self):
        return self.left.read_digital() != 0

