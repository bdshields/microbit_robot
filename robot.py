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
        sleep(1)
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
move.setSpeed(1,1)
move.setDirection(1,1)
move.update_speed()
move.update_direction()

pixel = neopixel.NeoPixel(pin5,18)

delayCounter = timer()

dist = 20

while True:
    #dist = meas.getDistance()
    #display.scroll(int(dist))
    if(dist > 15):
        move.go()
        #delayCounter.reset()
    else:
        move.stop()
        delayCounter.reset()

    if(prox.detectRight()):
        move.turn(0)
        delayCounter.reset()
    elif(prox.detectLeft()):
        move.turn(1)
        delayCounter.reset()
    
    accel = abs(accelerometer.get_z())
    pixel.clear()
    pixel[int(accel * 17 / 2048)] = (0, 255, 0)
    pixel.show()
    if(delayCounter.getDelay() > 600):
        if(accel > 1000):
            move.turn(0)
            move.turn(0)
            delayCounter.reset()
        
    
    
    
