from microbit import *

MAX_SPEED = 4095

''' Dead-reconning values for rotation '''
ROTATE_SPEED = 2000
ROTATE_RATE = 8

FORWARDS = 0
BACKWARDS = 4095

LEFT_DIR =  0
LEFT_SPEED = 1
RIGHT_DIR = 2
RIGHT_SPEED = 3



def limit(value, min, max):
    if(value < min):
        value = min
    elif (value > max):
        value = max
    return value

class drive:
    def __init__(self):
        from PCA9685 import PCA9685
        self.pwm = PCA9685(i2c, address=67)
        self.state=0
        self.pwm.set_pwm(LEFT_DIR,0,FORWARDS)
        self.pwm.set_pwm(RIGHT_DIR,0,FORWARDS)
        self.left_speed=2000
        self.right_speed=2000

    def adjustSpeed(self, change):
        self.left_speed = limit(self.left_speed + change, 0, MAX_SPEED)
        self.right_speed = limit(self.right_speed + change, 0, MAX_SPEED)
        self.pwm.set_pwm(LEFT_SPEED,0,self.left_speed)
        self.pwm.set_pwm(RIGHT_SPEED,0,self.right_speed)

    def adjustDirection(self, change):
        '''
        minor change in directioon
        -ve = Left
        +ve = Right
        '''
        self.left_speed = limit(self.left_speed + change, 0, MAX_SPEED)
        self.pwm.set_pwm(LEFT_SPEED,0,self.left_speed)


    def stop(self):
        if(self.state != 0):
            self.pwm.set_pwm(LEFT_SPEED,0,0)
            self.pwm.set_pwm(RIGHT_SPEED,0,0)
            self.state=0

    def go(self):
        if(self.state != 1):
            self.pwm.set_pwm(LEFT_SPEED,0,self.left_speed)
            self.pwm.set_pwm(RIGHT_SPEED,0,self.right_speed)
            self.state=1

    def rotate(self,direction, stop=None):
        '''
        direction = degrees of rotation.
                +ve = clockwise
                -ve = anti-clockwise
        
        stop = a function to run to check if should stop
        '''
        oldState = self.state
        if self.state != 0:
            self.stop()
            sleep(100)

        if (direction > 0):
            self.pwm.set_pwm(RIGHT_DIR,0,BACKWARDS)
        else:
            self.pwm.set_pwm(LEFT_DIR,0,BACKWARDS)
            direction *= -1

        self.pwm.set_pwm(LEFT_SPEED,0,ROTATE_SPEED)
        self.pwm.set_pwm(RIGHT_SPEED,0,ROTATE_SPEED)
        
        while direction > 0:
            sleep(ROTATE_RATE)
            direction -= 2
            if stop is not None:
                if stop():
                    break

        self.pwm.set_pwm(LEFT_SPEED,0,0)
        self.pwm.set_pwm(RIGHT_SPEED,0,0)
        self.pwm.set_pwm(LEFT_DIR,0,FORWARDS)
        self.pwm.set_pwm(RIGHT_DIR,0,FORWARDS)
        
        if(oldState == 1):
            sleep(100)
            self.go()     

