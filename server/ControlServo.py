import RPi.GPIO as GPIO
import time
import threading

class ControlServo():
    timer = 3600
    servoChannel = 0
    def __init__(self):
        
        self.feedAfter(self.timer)
    
    
    def setServo(self, servoChannel, position):
        servoStr ="%u=%u\n" % (servoChannel, position)
        with open("/dev/servoblaster", "wb") as f:
            f.write(servoStr.encode("utf-8"))
    
    def feedAfter(self, time):
        self.timer = time
        self.t = threading.Timer(time, self.feedTimer)
        self.t.start()

    def resetfeedAfter(self):
        self.t.cancel()

    def feedTimer(self):
        self.feed()
        self.feedAfter(self.timer)

    def feed(self):
        val = 50
        self.direction = 1
        self.setServo(self.servoChannel, val)

        while True:
            self.setServo(self.servoChannel, val)
            if val == 249:
                break
            val = val + 1

        time.sleep(1)
        while True:
            self.setServo(self.servoChannel, val)
            if val == 50:
                break
            val = val - 1
        