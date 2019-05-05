import json

class Sensors():

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
        full = False
        middle = False
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