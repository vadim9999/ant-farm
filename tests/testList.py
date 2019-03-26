from os import listdir
from os.path import isfile, join

# data = {
#     "sot":{
#         "temp":26,
#         "hum":70,
#     }
# }
#
# print(data["sot"]["hum"])
mypath = "./videos/"
fileNames = [f for f in listdir(mypath) if isfile(join(mypath, f))]
print(str(fileNames))
