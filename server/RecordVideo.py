import io
import logging
import socketserver
from threading import Condition
from http.server import HTTPServer, BaseHTTPRequestHandler
from glob import glob
from os import curdir, sep
from string import Template
from wsgiref.simple_server import make_server
from threading import Thread
from ws4py.websocket import WebSocket
import picamera
from time import sleep, time
import http.cookies
import urllib.parse as urlparse
from urllib.parse import urlencode
import subprocess
import os
import signal

class RecordVideo():
    height = 480
    width = 640
    startedRecording = False

    def setVideoResolution(self, height, width):
        self.height = height
        self.width = width
    def test(self):
        print("_________int_test____")
        return ("In test Video record ")

    def startRecording(self, filename, startedPreview, camera):
        print("_____in_start_Record____")
        if startedPreview == True:
            try:
                print("_________start_recording video")
                self.startedRecording = True
                filename1 = filename + ".h264"
                camera.start_recording(filename1,format='h264', splitter_port=2)
                while self.startedRecording == True:
                    camera.wait_recording(1)
                print("____Executing after record")
            except Exception as e:
                logging.warning(
                    'Stop recording video', str(e))
            finally:
                print("____Block finally___")
                print("____Stopping_splitter_port")
                camera.stop_recording(splitter_port = 2)
                self.startedRecording = False

    def stopRecording(self):
        self.startedRecording = False
