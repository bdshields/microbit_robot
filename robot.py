import microbit
import neopixel
from  machine import time_pulse_us

import PCA9685

class ultraSonic:
    def __init__(self):
        self.trig = microbit.pin14
        self.echo = microbit.pin15
        self.trig.write_digital(0)
        self.echo.read_digital()

    def getDistance(self):
        self.trig.write_digital(1)
        self.trig.write_digital(0)
        micros = time_pulse_us(self.echo, 1)
        t_echo = micros / 1000000
        dist_cm = (t_echo / 2) * 34300
        return dist_cm

class drive:
    def __init__(self):
        self.pwm = PCA9685.PCA9685(microbit.i2c, address=67)
        self.pwm.set_pwm(0,0,0)
        self.pwm.set_pwm(2,0,0)
        self.state=0

    def stop(self):
        if(self.state != 0):
            self.pwm.set_pwm(1,0,0)
            self.pwm.set_pwm(3,0,0)
            self.state=0
    def go(self):
        if(self.state != 1):
            self.pwm.set_pwm(1,0,3000)
            self.pwm.set_pwm(3,0,3000)
            self.state=1
   

    def forward(self, duration=None):
        self.pwm.set_pwm(0,0,0)
        self.pwm.set_pwm(2,0,0)
        self.pwm.set_pwm(1,0,3000)
        self.pwm.set_pwm(3,0,3000)
        if duration is not None:
            microbit.sleep(duration)
            self.pwm.set_pwm(1,0,0)
            self.pwm.set_pwm(3,0,0)
        else:
            self.state=1

            


meas = ultraSonic()
move = drive()
move.forward(100)

while True:
    dist = meas.getDistance()
    #microbit.display.scroll(int(dist))
    #microbit.sleep (100)
    if(dist > 15):
        move.go()
    else:
        move.stop()
    
    
    
    
