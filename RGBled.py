

RED = 4
GREEN = 5
BLUE = 6

OFF = 0
FULL = 4095

class RGB():
    def __init__(self, pwm):
        self.pwm = pwm
        self.set(0,0,0)

    def set(self, red, green, blue):
        ''' 0.0 ... 1.0 '''
        self.pwm.set_pwm(RED,red*4095,4095)
        self.pwm.set_pwm(GREEN,green*4095,4095)
        self.pwm.set_pwm(BLUE,blue*4095,4095)

