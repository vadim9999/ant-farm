import json
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import Adafruit_DHT

class Sensors():
    fullWaterPin = 23
    middleWaterPin = 24
    lowWaterPin  = 25
    isInitialize = False

    def initWaterLevel(self):
        print("init waterlevel")
        GPIO.setmode(GPIO.BCM) 
        GPIO.setup(self.fullWaterPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.middleWaterPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.lowWaterPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
    def closeWaterLevel(self):
        GPIO.cleanup()

    def getDataDHTS(self):
        

        humidityOutside, temperatureOutside = Adafruit_DHT.read_retry(11, 27) #DOne
        humiditySot, temperatureSot = Adafruit_DHT.read_retry(11, 17)
        humidityArena, temperatureArena = Adafruit_DHT.read_retry(11, 26)

        if humidityOutside is None and temperatureOutside is None:
            humidityOutside = 20
            temperatureOutside = 30
            print('Failed to get reading. Try again!humidityOutside')

        if humiditySot is None and temperatureSot is None:
            humiditySot = 20
            temperatureSot = 30
            print('Failed to get reading. Try again!humiditySot')

        if humidityArena is None and temperatureArena is None:
            humidityArena = 20
            temperatureArena = 30
            print('Failed to get reading. Try again! temperatureArena')

        result = [
                {
                    "name": "sot",
                            "Temp": temperatureSot,
                            "Hum": humiditySot,
                },
                {
                    "name": "outside",
                            "Temp": temperatureOutside,
                            "Hum": humidityOutside,
                },
                {
                    "name": "arena",
                            "Temp": temperatureArena,
                            "Hum": humidityArena,
                }
            ]
        return result
    

    def getSensorsData(self, connectedId):
        data = {
            "sensors": self.getDataDHTS(),
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
        if GPIO.input(self.fullWaterPin) == GPIO.HIGH:
            full = True
        if GPIO.input(self.middleWaterPin) == GPIO.HIGH:
            middle = True
        if GPIO.input(self.lowWaterPin) == GPIO.HIGH:
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