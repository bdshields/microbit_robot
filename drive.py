from microbit import *

class drive:
    def __init__(self):
        from PCA9685 import PCA9685
        self.pwm = PCA9685(i2c, address=67)
        self.state=0
        self.pwm.set_pwm(0,0,0)
        self.pwm.set_pwm(2,0,0)
        self.new_left_speed=2000
        self.cur_left_speed=2000
        self.new_left_dir=0
        self.cur_left_dir=0
        self.new_right_speed=2000
        self.cur_right_speed=2000
        self.new_right_dir=0
        self.cur_right_dir=0
        
    def setDirection(self, left, right):
        self.new_left_dir=4095 * (left ^ 1)
        self.new_right_dir=4095 * (right ^ 1)

    def setSpeed(self, left, right):
        self.new_left_speed = 1000 * left
        self.new_right_speed = 1000 * right

    def update_speed(self):
        if(self.state == 1):
            if self.new_left_speed != self.cur_left_speed:
                self.pwm.set_pwm(1,0,self.new_left_speed)
            if self.new_right_speed != self.cur_right_speed:
                self.pwm.set_pwm(3,0,self.new_right_speed)
        self.cur_left_speed = self.new_left_speed
        self.cur_right_speed = self.new_right_speed

    def update_direction(self):
        if self.new_left_dir != self.cur_left_dir:
            self.pwm.set_pwm(0,0,self.new_left_dir)
        if self.new_right_dir != self.cur_right_dir:
            self.pwm.set_pwm(2,0,self.new_right_dir)
        self.cur_left_dir = self.new_left_dir
        self.cur_right_dir = self.new_right_dir

    def stop(self):
        if(self.state != 0):
            self.pwm.set_pwm(1,0,0)
            self.pwm.set_pwm(3,0,0)
            self.state=0

    def go(self):
        if(self.state != 1):
            self.pwm.set_pwm(1,0,self.cur_left_speed)
            self.pwm.set_pwm(3,0,self.cur_right_speed)
            self.state=1

    def turn(self,direction):
        oldState = self.state
        self.stop()
        sleep(100)
        if (direction):
            self.setDirection(1,0)
        else:
            self.setDirection(0,1)
        self.setSpeed(1,1)
        self.update_direction()
        self.update_speed()
        self.go()
        sleep(700)
        self.stop()
        sleep(100)
        self.setDirection(1,1)
        self.setSpeed(1,1)
        self.update_direction()
        self.update_speed()
        if(oldState):
            self.go()        

