import RPi.GPIO as GPIO
import time
import threading

class ControlServo():
    def init(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18,GPIO.OUT)
        self.pwm=GPIO.PWM(18,50)
        self.pwm.start(2.5)
        time.sleep(1)
        # print("after start")
        # 2.5 0 degree
        #@TODO find out why need this code            
        # self.pwm.ChangeDutyCycle(12.5) 
        # time.sleep(1)
        # self.pwm.start(2.5)
        # time.sleep(1)
        # ------------
    def SetAngle(self,angle):
	    duty = angle / 18 + 2
	    GPIO.output(18, True)
	    self.pwm.ChangeDutyCycle(duty)
	    time.sleep(1)
	    GPIO.output(18, False)
	    self.pwm.ChangeDutyCycle(0)
    
    def stopServo(self):
        self.pwm.stop()
        GPIO.cleanup()
    
    def feedAfter(self, time):
        self.t = threading.Timer(time, self.feed)
        self.t.start()

    def resetfeedAfter(self):
        self.t.cancel()
        
    def feed(self):
        self.init()
        self.SetAngle(180)
