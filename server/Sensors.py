import json
import RPi.GPIO as GPIO  
import Adafruit_DHT


class Sensors():
    fullWaterPin = 23
    middleWaterPin = 24
    lowWaterPin = 25
    

    def __init__(self):
        self.initWaterLevel()

    def initWaterLevel(self):
        GPIO.setmode(GPIO.BCM)
        try:
            GPIO.setup(self.fullWaterPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.setup(self.middleWaterPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.setup(self.lowWaterPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        except:
            print("Err")
            
    def getDataDHTS(self):

        humidityOutside, temperatureOutside = Adafruit_DHT.read_retry(
            11, 27)  
        humiditySot, temperatureSot = Adafruit_DHT.read_retry(11, 17)
        humidityArena, temperatureArena = Adafruit_DHT.read_retry(11, 26)

        if humidityOutside is None and temperatureOutside is None:
            humidityOutside = 20
            temperatureOutside = 30

        if humiditySot is None and temperatureSot is None:
            humiditySot = 20
            temperatureSot = 30

        if humidityArena is None and temperatureArena is None:
            humidityArena = 20
            temperatureArena = 30

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

    def getSensorsData(self, connectedId, startedStreaming):
        data = {
            "sensors": self.getDataDHTS(),
            "waterLevel": self.getWaterLevel(),
            "connectedId": connectedId,
            "streaming": startedStreaming
        }

        data = json.dumps(data)
        return data

    def getWaterLevel(self):
        
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
        sotHum = 80
        outsideHum = 80
        arenaHum = 80

        valuesHumSot = ("0 200; {0:0} 180; {1} 150; {2} 135; {2} 135;"
                        .format(int(sotHum/3), int(sotHum/2), sotHum))

        valuesHumArena = ("0 200; {0:0} 180; {1} 150; {2} 135; {2} 135;"
                          .format(int(arenaHum/3), int(arenaHum/2), arenaHum))

        valuesHumOutside = ("0 200; {0:0} 180; {1} 150; {2} 135; {2} 135;"
                            .format(int(outsideHum/3), int(outsideHum/2), outsideHum))

        data = {
            "valuesHumSot": valuesHumSot,
            "valuesHumArena": valuesHumArena,
            "valuesHumOutside": valuesHumOutside
        }

        return data
