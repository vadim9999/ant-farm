import RPi.GPIO as GPIO
import time
import threading

class ControlServo():
    
    def __init__(self):
        
        self.feedAfter(60)

    def initFeeder(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18,GPIO.OUT)
        self.pwm=GPIO.PWM(18,50)
      
    
    def stopServo(self):
        self.pwm.stop()
        GPIO.cleanup()
    
    def feedAfter(self, time):
        self.t = threading.Timer(time, self.feed)
        self.t.start()

    def resetfeedAfter(self):
        self.t.cancel()
        
    def feed(self, time):
        self.initFeeder()
        self.pwm.start(2.5)
        time.sleep(1)
        self.pwm.ChangeDutyCycle(12.5) 
        time.sleep(1)
        self.pwm.start(2.5)
        time.sleep(1)
        self.pwm.stop()
        self.stopFeeder()
        self.feedAfter(time)

    def feedNow(self):
        self.initFeeder()
        self.pwm.start(2.5)
        time.sleep(1)
        self.pwm.ChangeDutyCycle(12.5) 
        time.sleep(1)
        self.pwm.start(2.5)
        time.sleep(1)
        self.pwm.stop()
        self.stopFeeder()