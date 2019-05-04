import json

class Sensors():

    def getSensorsData(self, connectedId):
        data = {
            "sensors": [
                {
                    "name": "sot",
                            "Temp": 26,
                            "Hum": 50,
                },
                {
                    "name": "outside",
                            "temp": 26,
                            "Hum": 50,
                },
                {
                    "name": "arena",
                            "Temp": 26,
                            "Hum": 80,
                }
            ],
            "waterLevel": "middle",
            "connectedId": connectedId
        }
        data = json.dumps(data)
        return data

    def getAnimationValues(self):
        sotHum = 60
        arenaHum = 50
        outsideHum = 80

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