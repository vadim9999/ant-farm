# Ant Farm

Ant Farm contains web-server and application on OS Android. 

**Goal**: Develop and program the Python Web server and an Android application using the Raspberry to support the activity of an Ant Farm. 

**Automated control system allow:**
1. Video streaming in YouTube.
2. Feed ants after a certain time.
3. Informing about the water level in the tank.
4. Provision of information on temperature and humidity in the form of cats.

**Writing web server on Python3.7 used this libraries:** 
 - picamera
 - http.server
 - socketserver
 - subprocess
 - os
 
**Frontend:**
 - HTML
 - CSS
 - JS
 - AJAX
 - Bootstrap
 - Font Awesome

 ## Using this project
 
 1. Clone this repository in `home` directory of Raspberry Pi Zero Wireless.
 2. Open `ant-farm` and execute command 'sudo python3.7 setup.py'.
 
 ## Components that was used in the Ant Farm
 
 ### 1. Raspberry Pi Zero Wireless
 
 <img src = "https://user-images.githubusercontent.com/35640573/51474686-bf139480-1d88-11e9-8e91-6340771ea96b.png"  height="240" width="340">
<img src = "https://user-images.githubusercontent.com/35640573/51474785-0bf76b00-1d89-11e9-8ada-9bc09edb9296.png"  height="240" width="340">
<img src = "https://user-images.githubusercontent.com/35640573/51475009-cb4c2180-1d89-11e9-981a-1e947a3ea6ee.png"  height="240" width="340" >

| --- | --- |
| --- | --- |
System on a chip (SoC) | Broadcom BCM2835 (CPU, GPU, DSP and SDRAM)
Processor | 32-bit 1-core ARMv6Z ARM1176JZF-S with a clock frequency of 1 GHz, 16 KB cache L1 and 128 KB cache L2 (ARM11 family)
Graphics processor | The dual-core GPU VideoCore IV® clocked at @ 250 MHz supports the standards OpenGL ES 2.0, OpenVG, MPEG-2, VC-1 and is capable of encoding, decoding and output Full HD video (1080p, 30 FPS, H.264 High-Profile)
RAM | 512 MB SDRAM LPDDR2 400 MHz (with GPU)
Storage | microSDHC memory card slot
Wi-Fi / Bluetooth | Wi-Fi 802.11n and Bluetooth 4.1 (Bluetooth Classic and LE) provided by the Cypress chip CYW43438
Video input | 1 x CSI for camera connection via MIPI interface
Video output | 1 x HDMI via mini HDMI connector (1080p60) 1 x composite video via two pins on the board (labeled TV)
Audio input | Via I²S
Audio output | HDMI
USB ports | 1 Micro USB 2.0 port directly from BCM2835
Peripherals | 40 general-purpose input-output ports (GPIO), UART (Serial), I²S, I²C / TWI, SPI with a selector between two devices; Power Pins: 3.3 V, 5 V and Ground.
Power | 5 V, 2 A via micro USB or GPIO
Power consumption | 100 mA (0.5 W) on average (standby), 350 mA (1.75 W) maximum, under stress (a monitor, keyboard and mouse are connected)
OS | Raspbian, Ubuntu, Debian, Fedora, Arch Linux, Gentoo, RISC OS, Android, Firefox OS, NetBSD, FreeBSD, Slackware, Tiny Core Linux

One of the features of Raspberry Pi is a series of GPIO contacts along the top edge of the board. GPIO stands for general purpose entry / exit. These contacts are the physical interface between Raspberry Pi and external devices.
The GPIO allows Raspberry Pi to control external devices by connecting to electronic circuits. The controller is able to control LEDs, turn them on or off, start electric motors and much more. You can also find out whether the key is pressed to receive temperature and humidity data

Useful links that you can find below:
- [Source of table](https://micro-pi.ru/raspberry-pi-zero-w-rpi0w-bcm2835/)
- [Connecting camera to raspberry pi zero w via connector](https://4te.me/post/camera-raspberry-pi/)

http://isearch.kiev.ua/ru/searchpracticeru/-internetsecurity-ru/1790-how-to-set-up-the-camera-module-raspberry-pi
https://learn.sparkfun.com/tutorials/setting-up-the-pi-zero-wireless-pan-tilt-camera/configure-the-raspberry-pi
https://thepihut.com/blogs/raspberry-pi-tutorials/16021420-how-to-install-use-the-raspberry-pi-camera
с помощью python https://dantheiotman.com/2017/08/28/realtime-video-using-a-raspberry-pi-zero-w-and-python-picamera/
или подключение веб-камеры( можно осуществлять стрим с помощью команды в консоли). 
https://www.raspberrypi.org/documentation/usage/webcams/.

### Camera module for RPI

The device for creating a broadcast on the Internet will be a camera. The video in h264 format will be transmitted using the ffmpeg program to the YouTube server.
In this work the 5-megapixel camera RPI Camera Rev 1.3 based on the sensor OV5647 was used. It connects to the CSI connector that comes with the cable.

<img src = "https://github.com/vadim9999/ant-farm/blob/master/screenshots/camera.png"  height="240" width="340" >

The camera is small in size: 25 x 20 x 9 mm. Supported video formats are 1080r with a frame rate of 30 frames per second (fps), 720p with 60 fps, and 480p with 90 fps. In order for Raspberry Pi to recognize the camera, you need to enable its support at the raspi-config level. To do this, at the command line you must enter:
$ sudo raspi-config
Go to the "Interfaces options" section. Select "P1 Camera" and press "Enter".

<img src = "https://github.com/vadim9999/ant-farm/blob/master/screenshots/camera-settings.png"  height="240" width="340" >

### Sensors DHT11

In this work, the sensors DHT11 are used.
The DHT11 sensor is a digital temperature and humidity sensor that allows you to calibrate the digital signal at the output. It consists of a capacitive humidity sensor and thermistor. In addition, the sensor contains ADC for converting analog values of humidity and temperature.

**Characteristics**:
- Power supply: I / O 3.5-5.5 V;
- Moisture determination: 20-90% RH ± 5% (max.);
- Temperature determination: 0-50 ºC ± 2% (max.);
- Frequency of request: no more than 1 Hz;
- Dimensions 15.5 x 12 x 5.5 mm.
Outputs:
1. VCC (3-5V supply);
2. Data Out - Data output;
3. NC - not used;
4. Land

<img src = "https://github.com/vadim9999/ant-farm/blob/master/screenshots/DHT11.png"  height="240" width="340" >

### Servo
    
    
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

