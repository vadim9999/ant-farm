import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)

pwm=GPIO.PWM(18,50)


pwm.start(2.5)
time.sleep(1)
# print("after start")
# 2.5 0 degree

pwm.ChangeDutyCycle(12.5) 
time.sleep(1)
# pwm.ChangeDutyCycle(2.5)


pwm.start(2.5)
time.sleep(1)

pwm.stop()
# pwm.ChangeDutyCycle(7.5)
# time.sleep(1)
# pwm.ChangeDutyCycle(2.5)
# time.sleep(1)
# pwm.ChangeDutyCycle(7.5)
# time.sleep(1)
# pwm.ChangeDutyCycle(12.5)
# time.sleep(1)
# pwm.ChangeDutyCycle(7.5)

# def SetAngle(angle):
	
# 	GPIO.output(18, True)
# 	pwm.start(2.5)
# 	time.sleep(3)
# 	pwm.ChangeDutyCycle(15.5)
# 	time.sleep(1)
# 	GPIO.output(18, False)
# 	pwm.ChangeDutyCycle(0)

# GPIO.output(18, True)
# pwm.start(2.5)
# time.sleep(3)
# pwm.ChangeDutyCycle(12.5)
# time.sleep(1)
# GPIO.output(18, False)
# pwm.start(2.5)
# # SetAngle(90)
# time.sleep(2)
# pwm.stop()
# GPIO.cleanup()



# try:
#     p.ChangeDutyCycle(10)
#         # while True:
#         #         p.ChangeDutyCycle(7.5)
#         #         print ("Left")
#         #         time.sleep(1)
#         #         p.ChangeDutyCycle(12.5)
#         #         print ("Center")
#         #         time.sleep(1)
#         #         p.ChangeDutyCycle(2.5)
#         #         print ("Right")
#         #         time.sleep(1)
# except KeyboardInterrupt:
#         p.stop()
#         GPIO.cleanup()