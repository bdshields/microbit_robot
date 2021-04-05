from microbit import *
from machine import time_pulse_us
from drive import drive
import neopixel


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

    def detectLeft(self):
        return self.left.read_digital() == 0

class timer:
    def __init__(self):
        self.runtime=running_time()

    def reset(self):
        self.runtime=running_time()

    def getDelay(self):
        return running_time() - self.runtime




meas = ultraSonic()
prox = ir_detector()
move = drive()
rotate_dir = 1
pixel = neopixel.NeoPixel(pin5,18)

delayCounter = timer()

dist = 20


def rotate_stop():
    if meas.getDistance() > 60:
        return True
    else:
        return False

move.go()

while True:

    if meas.getDistance() < 30:
        move.rotate(rotate_dir * 180, rotate_stop)
        rotate_dir *= -1

    if prox.detectLeft():
        move.rotate(15)
        rotate_dir = 1
    elif prox.detectRight():
        move.rotate(-15)
        rotate_dir = -1

