import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time

# GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)
GPIO.output(18, 1)
time.sleep(20)
GPIO.cleanup()