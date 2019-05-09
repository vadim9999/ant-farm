import json
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time
import threading

class Sensors():
    full = 14
    middle = 15
    low  = 18
    isInitialize = False

    def initWaterLevel(self):
        print("init waterlevel")
        GPIO.setmode(GPIO.BCM) 
        GPIO.setup(self.full, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.middle, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.low, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    def closeWaterLevel(self):
        GPIO.cleanup()

    def getSensorsData(self, connectedId):
        data = {
            "sensors": [
                {
                    "name": "sot",
                            "Temp": 26,
                            "Hum": 60,
                },
                {
                    "name": "outside",
                            "Temp": 26,
                            "Hum": 50,
                },
                {
                    "name": "arena",
                            "Temp": 26,
                            "Hum": 80,
                }
            ],
            "waterLevel": self.getWaterLevel(),
            "connectedId": connectedId
        }
        data = json.dumps(data)
        return data
    

    def getWaterLevel(self):
        if self.isInitialize == False:
            self.isInitialize = True
            self.initWaterLevel()
            
        
        full = False
        middle = False
        low = False 
        if GPIO.input(self.full) == GPIO.HIGH:
            full = True
        if GPIO.input(self.middle) == GPIO.HIGH:
            middle = True
        if GPIO.input(self.low) == GPIO.HIGH:
            low = True
        level = 80
        if full == True and middle == False and low == False:
            level = 20
        elif full == True and middle == True and low == False:
            level = 40
        elif full == False and middle == True and low == False:
            level = 60
        elif full == False and middle == True and low == True:
            level = 80
        else: 
            level = 90

        return level

    def getAnimationValues(self):
        sotHum = 60
        
        outsideHum = 50
        arenaHum = 80

        valuesHumSot = ("0 200; {0:0} 180; {1} 150; {2} 135; {2} 135;"
        .format(int(sotHum/3), int(sotHum/2), sotHum))

        valuesHumArena = ("0 200; {0:0} 180; {1} 150; {2} 135; {2} 135;"
        .format(int(arenaHum/3), int(arenaHum/2), arenaHum))

        valuesHumOutside = ("0 200; {0:0} 180; {1} 150; {2} 135; {2} 135;"
        .format(int(outsideHum/3), int(outsideHum/2), outsideHum))

        data = {
            "valuesHumSot" : valuesHumSot,
            "valuesHumArena" : valuesHumArena,
            "valuesHumOutside" : valuesHumOutside
        }

        return data