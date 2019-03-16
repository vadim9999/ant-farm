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
    height 480
    width 640

    def setVideoResolution(self, height, width):
        self.height = height
        self.width = width

    def startRecord(self, filename = "video"):
