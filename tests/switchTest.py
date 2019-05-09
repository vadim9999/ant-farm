import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
pinLow = 15
GPIO.setmode(GPIO.BCM) 
GPIO.setup(pinLow, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
 # Set pin 10 to be an input pin and set initial value to be pulled low (off)
import time


if GPIO.input(pinLow) == GPIO.HIGH:
        print("Button was pushed!")
time.sleep(1)
if GPIO.input(pinLow) == GPIO.HIGH:
        print("Button was pushed!")
# while True: # Run forever
#     time.sleep(2)
#     if GPIO.input(24) == GPIO.HIGH:
#         print("Button was pushed!")

GPIO.cleanup()
# while True:
#     time.sleep(1)