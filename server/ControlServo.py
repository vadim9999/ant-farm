import RPi.GPIO as GPIO
import time
import threading

class ControlServo():
    timer = 3600
    def __init__(self):
        
        self.feedAfter(self.timer)

    def initFeeder(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18,GPIO.OUT)
        self.pwm=GPIO.PWM(18,50)
      
    
    def stopServo(self):
        self.pwm.stop()
        GPIO.cleanup()
    
    def feedAfter(self, time):
        # Fix
        self.timer = time
        self.t = threading.Timer(time, self.feed)
        self.t.start()

    def resetfeedAfter(self):
        self.t.cancel()
        
    def feed(self):
        self.initFeeder()
        self.pwm.start(2.5)
        time.sleep(1)
        self.pwm.ChangeDutyCycle(12.5) 
        time.sleep(1)
        self.pwm.start(2.5)
        time.sleep(1)
        self.pwm.stop()
        self.stopServo()
        self.feedAfter(self.timer)

    def feedNow(self):
        self.initFeeder()
        self.pwm.start(2.5)
        time.sleep(1)
        self.pwm.ChangeDutyCycle(12.5) 
        time.sleep(1)
        self.pwm.start(2.5)
        time.sleep(1)
        self.pwm.stop()
        self.stopServo()