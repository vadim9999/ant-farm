# Ant Farm

Ant Farm contains web-server and application on OS Android. 

**Goal**: Develop and program the Python Web server and an Android application using the Raspberry to support the activity of an Ant Farm. 

**Automated control system allow:**
1. Video streaming in YouTube.
2. Feed ants after a certain time.
3. Informing about the water level in the tank.
4. Provision of information on temperature and humidity in the form of cats.

1. Writing web server on Python3.7 used this libraries: 
 - picamera
 - http.server
 - socketserver
 - subprocess
 - os
2. Frontend:
 - HTML
 - CSS
 - JS
 - AJAX
 - Bootstrap
 - Font Awesome

 ## Using this project
 
 1. Clone this repository in `home` directory of Raspberry Pi Zero Wireless.
 2. Open `ant-farm` and execute command 'sudo python3.7 setup.py'.
 
 ## Screenshots

<img src = "https://github.com/vadim9999/ant-farm/blob/master/screenshots/1.png"  height="340" width="440" >
<img src = "https://github.com/vadim9999/ant-farm/blob/master/screenshots/2.png"  height="340" width="440" >
<img src = "https://github.com/vadim9999/ant-farm/blob/master/screenshots/3.png"  height="340" width="440" >
<img src = "https://github.com/vadim9999/ant-farm/blob/master/screenshots/4.png"  height="340" width="440" >

## Instruction of using farm

### Installation of Ant Farm:
1. Place the forcarius on the table.
2. Fill the dry feed into the container of the automatic feeder.
3. Remove the float from the drinker and pour water to the top mark. Lower the float to water and close the bowl lid.
4. Adjust the amount of water droplets with the wheel.

### First launch of the farm:
1. Check all the wires for damage.
2. Insert the power plug into the wall outlet (220V). You can also disconnect the USB device from the power supply and connect it to another power supply (5V) or to a PC.
3. Wait 2 minutes until the device boots. Find out if the device is working on a green LED that is in the device housing.
4. Currently, the farm is not connected to any WIFI network. To connect it, install ant-farm.apk on Android.
5. After successful installation, go to the Bluetooth settings on your smartphone. Settings -> Bluetooth -> Enable Bluetooth. Search for devices. In the list of found devices, connect to the ant-farm device. Exit the settings.
6. Go to the Murashina Farm application. Searching for devices will start automatically. In the drop-down list, select ant-farm and press the "connect" key;
7. If the connection is successful, the drop-down list of networks, the field for entering the password and the 3 keys will be activated; otherwise the error window will be displayed;
8. Select a router or WiFi network from the drop down list. Enter a password from this network and click 'Save.' If the connection of RPi to the network was successful, then the first item in the list will be connected to the router with the prefix "connected", otherwise an error message.
9. In order to find the IP address Raspberry Pi, press the "Learn IP" key.
10. The computer and the Ant family should be in the same network. If so, open the Google Chrome browser and enter the IP address you found through the application in the search field.

Using a webpage:
1. On the open page, press the "Start Video Stream" key to view the stream from the camera. To stop - the "Stop" key. To change the quality, click on the gear in the lower right corner and select the quality.
2. To open in full screen mode, click on the square located at the bottom right of the player.
3. To create a stream on the Internet, you need to select the video quality, press the Settings key, and enter the link and the key that was displayed when creating a live stream on YouTube. Click Start Broadcast. To stop, press the "Stop" key.
4. To record video, you must select the quality from the list and press the "Start recording" key. To stop - the "Stop" key.
5. To create the image, select the quality and press the "Create Image" key.
6. To view the media, press the Media key, a window will open in which you can download or delete a video or photo entry.
7. To feed, press the "Feeder Settings" key, then select the interval or the "Feed" key, which will start the feeder mechanism.
The web page displays information about 3 gauges and water level. Each sensor shows the temperature and humidity of the air. The first sensor is located in the "cell" of the formicary, the second in the "arena", the third in the room. In the arena there is a feeder based on raspberry pi, a water tank and a regulating wheel to limit the amount of water droplets.

<img src = "https://github.com/vadim9999/ant-farm/blob/master/screenshots/farm.png"  height="440" width="340" >

