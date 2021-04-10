from microbit import running_time, i2c

from drive import drive
from RGBled import RGB
from detect import ultraSonic, ir_detector
from PCA9685 import PCA9685

#import neopixel


class timer:
    ''' Measures time in miliseconds '''
    def __init__(self):
        self.runtime=running_time()

    def reset(self):
        self.runtime=running_time()

    def getDelay(self):
        return running_time() - self.runtime


pwm = PCA9685(i2c, address=67)


meas = ultraSonic()
prox = ir_detector()
move = drive(pwm)
led = RGB(pwm)
rotate_dir = 1


#pixel = neopixel.NeoPixel(pin5,18)

turnClearance = 60

def rotate_stop():
    if (meas.getDistance() > turnClearance) and prox.clearLeft() and prox.clearRight():
        return True
    else:
        return False


move.go()

stuck = timer()
turnCounter = 0

while True:

    if meas.getDistance() < 30:
        move.rotate(rotate_dir * 180, rotate_stop)
        rotate_dir *= -1
        turnCounter += 1

    if prox.detectLeft() and not prox.detectRight():
        ''' turn Right '''
        move.rotate(180, prox.clearLeft)
        rotate_dir = 1
        turnCounter += 1
            
    elif prox.detectRight() and not prox.detectLeft():
        ''' turn Left '''
        move.rotate(-180, prox.clearRight)
        rotate_dir = -1
        turnCounter += 1

    elif prox.detectLeft() and prox.detectRight():
        move.rotate(180)
        
    ''' Detect if stuck '''
    if turnCounter > 15:
        turnClearance = 150
        move.rotate(180)
        turnCounter = 0        

    if stuck.getDelay() > 30:
        stuck.reset()
        turnCounter = 0
        turnClearance = 60


