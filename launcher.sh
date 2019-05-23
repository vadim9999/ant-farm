#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home

cd /
cd home/pi/ant-farm
sudo /usr/local/sbin/servod --idle-timeout=2000 --p1pins=12
sudo python3.7 setup.py
cd /
