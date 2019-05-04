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
from time import sleep, time
import http.cookies
import urllib.parse as urlparse
from urllib.parse import urlencode
from os import listdir
from os.path import isfile, join
import os
import shutil
import sys
import json
from .Sensors import Sensors

WIDTH = 640
HEIGHT = 480
FRAMERATE = 24
HTTP_PORT = 8002
WS_PORT = 8084
COLOR = u'#444'
BGCOLOR = u'#FFFFFF'



# streaming = False
# connectedClients = 0
# FILEPATH = "videos/file.h264"
counter = 0
class StreamingHttpHandler(BaseHTTPRequestHandler):

    # def startRecording(self):
    #     print("Start Recording")
    #     self.camera = picamera.PiCamera(resolution='640x480', framerate=24)

    # def stopStreaming(self):
    #     global streaming
    #     streaming = False
    sensors = Sensors()

    def do_HEAD(self):
        self.do_GET()

    def do_POST(self):
        url_parts = list(urlparse.urlparse(self.path))
        self.path = url_parts[2]
        query = dict(urlparse.parse_qsl(url_parts[4]))
        userId = 0
        if len(query) != 0:
            userId = int(query["id"])
            print(query["id"])
        
        # -----------------record--------------------
        if self.path == "/start_record":
            self.send_response(200)
            self.end_headers()
            print("_____start_recording_video____")
            # print(self.rfile.read(int(self.headers['Content-Length'])))
            data = self.rfile.read(int(self.headers['Content-Length']))
            data = str(data.decode("utf-8"))
            data = data.split("//")
            # self.recordVideo.startRecord(filename,True,self.camera)
            print(data)
            self.wfile.write("ok".encode('utf-8'))

        if self.path == "/start":
            self.send_response(200)
            self.end_headers()

            # print(self.rfile.read(int(self.headers['Content-Length'])))
            resolution = str(self.rfile.read(int(self.headers['Content-Length'])).decode("utf-8"))
            print("resolution")
            print(resolution)
        
        if self.path == '/start_stream':
            self.send_response(200)
            self.end_headers()
            print("_______start_stream")
            print("UserId")
            print(userId)
            print(str(self.rfile.read(int(self.headers['Content-Length'])).decode("utf-8")))
            self.wfile.write("hello".encode('utf-8'))
            print("_________After Stopping recording_________")
        
        if self.path == "/capture_image":
            self.send_response(200)
            self.end_headers()
            # TODO change on json
            data = self.rfile.read(int(self.headers['Content-Length']))
            data = str(data.decode("utf-8"))
            data = data.split("//")
            print(data)
        # ------------------------------------

        if self.path == "/set_settings_feeder":
            print("")
            self.send_response(200)
            self.end_headers()
            
            data = self.rfile.read(int(self.headers['Content-Length']))
            data = str(data.decode("utf-8"))
            print(data)

        

    #Handler for the GET requests
    def do_GET(self):
            if self.path == '/':
                self.send_response(301)
                global counter
                counter = counter + 1
                print("_________counter_____________")
                self.send_header('Location', '/index.html?id='+str(counter))
                self.end_headers()
                return

            elif self.path == '/sensors':
                content_type = 'text/html; charset=utf-8'
                connectedId = 0
                preview = True
                stream = False
                recording = False
                if preview == True:
                    if stream == True:
                        connectedId = 2
                    elif recording == True:
                        connectedId = 2

                
            
                content = (self.sensors.getSensorsData(connectedId)).encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', content_type)
                self.send_header('Content-Length', len(content))
                # @TODO add last modified
                self.end_headers()
                self.wfile.write(content)

            else:
                url_parts = list(urlparse.urlparse(self.path))
                self.path = url_parts[2]
                query = dict(urlparse.parse_qsl(url_parts[4]))
                userId = 0
                

                if url_parts[2].startswith('/download') == True:
                    urls = url_parts[2].split("/")
                    print(urls[2])
                    filepath = "media/" + urls[2]
                    with open(filepath, 'rb') as f:
                        self.send_response(200)
                        self.send_header("Content-Type", 'application/octet-stream')
                        self.send_header(
                            "Content-Disposition", 'attachment; filename="{}"'.format(os.path.basename(filepath)))
                        fs = os.fstat(f.fileno())
                        self.send_header("Content-Length", str(fs.st_size))
                        self.end_headers()
                        shutil.copyfileobj(f, self.wfile)
                        # self.path = 'videos/file.h264'

                if url_parts[2].startswith('/delete') == True:
                    self.send_response(204)
                    self.end_headers()
                    urls = url_parts[2].split("/")
                    print(urls[2])
                    filepath = "media/" + urls[2]
                    if os.path.exists(filepath):
                        os.remove(filepath)
                    else:
                        print("The file does not exist")
                
                # print()
                if len(query) != 0:
                    userId = int(query["id"])
                    print(query["id"])
                # ----feed
                if self.path == "/feed":
                    print("feed")
                    self.send_response(200)
                    self.end_headers()
                # *************
                # Note delete all print(self.rfile.read(int(self.headers['Content-Length'])))
                if self.path == "/stop":
                    self.send_response(200)
                    self.end_headers()
                    # print(self.rfile.read(int(self.headers['Content-Length'])))

                if self.path == '/wait_start_preview':
                    self.send_response(200)
                    self.end_headers()
                    print(self.rfile.read(int(self.headers['Content-Length'])))
                    self.wfile.write("hello".encode('utf-8'))

                # ---- getSettings-------
                if self.path == '/stream_settings':
                    self.send_response(200)
                    self.end_headers()
                    # @TODO change it
                    YOUTUBE="rtmp://a.rtmp.youtube.com/live2/"
                    KEY= "6kbh-kq1m-zbty-e4rt"
                    # ------
                    data = {
                        "youtube": YOUTUBE,
                        "key": KEY
                    }
                    data = str(data)
                    self.wfile.write(data.encode('utf-8'))
                # -----------------------
        # --------------stream---------------------
                

                if self.path == "/stop_stream":
                    self.send_response(200)
                    self.end_headers()
                    print("_________________Stop stream____")
                    print(self.rfile.read(int(self.headers['Content-Length'])))
                    self.wfile.write("hello".encode('utf-8'))

                if self.path == "/index.html":
                    self.path = 'templates/index.html'

                if self.path == "/ok.html":
                    self.path = 'templates/ok.html'
                # if self.path == "/download/file.h264":
                #     with open(FILEPATH, 'rb') as f:
                #         self.send_response(200)
                #         self.send_header("Content-Type", 'application/octet-stream')
                #         self.send_header(
                #             "Content-Disposition", 'attachment; filename="{}"'.format(os.path.basename(FILEPATH)))
                #         fs = os.fstat(f.fileno())
                #         self.send_header("Content-Length", str(fs.st_size))
                #         self.end_headers()
                #         shutil.copyfileobj(f, self.wfile)
                        # self.path = 'videos/file.h264'

                # capture_image
                

                if self.path == "/stop":
                    self.send_response(200)
                
                #-----------finding video files
                if self.path == "/media":
                    print("In videos")
                    content_type = 'text/html; charset=utf-8'
                    mypath = "./media/"
                    fileNames = [f for f in listdir(mypath) if isfile(join(mypath, f))]
                    print()
                    if len(fileNames) > 0:
                        fileNames = str(fileNames)
                    else :
                        fileNames = ""
                    
                    content = fileNames.encode("utf-8")
                    self.send_response(200)
                    self.send_header('Content-Type', content_type)
                    self.send_header('Content-Length', len(content))
                    # @TODO add last modified
                    self.end_headers()
                    self.wfile.write(content)
                
                if self.path == "/stop_record":
                    self.send_response(200)
                    self.end_headers()
                    print("_____stop_recording_video____")
                    # print(self.rfile.read(int(self.headers['Content-Length'])))
                    # self.wfile.write("ok".encode('utf-8'))
        # -------------------------
                # --------------------------------

                if self.path == '/stream.mjpg':
                    print("*************/stream.mjpg")
                    if userId != 0:
                        print("UserId in stream/mjpg")




                    # self.wfile.write(b'--FRAME\r\n')
                    # self.send_header('Content-Type', 'image/jpeg')
                    # self.send_header('Content-Length', len(b'12'))
                    # self.end_headers()
                    # self.wfile.write(b'12')
                    # self.wfile.write(b'\r\n')

                        # if (self.connectedClients == 0 ):

                            # self.camera.start_recording(self.output, format='mjpeg')
                try:
                    #Check the file extension required and
                    #set the right mime type
                    sendReply = False
                    if self.path.endswith(".html"):
                        print('it is html ')
                        mimetype='text/html'
                        content_type = 'text/html; charset=utf-8'
                        with io.open(self.path, 'r') as f:
                            index_template = f.read()

                        tpl = Template(index_template)
                        print("In Template __________")
                        # sotHum = 40

                        # valuesHumSot = ("0 200; {0:0} 180; {1} 150; {2} 135; {2} 135;".format(int(sotHum/3), int(sotHum/2), sotHum))
                        values = self.sensors.getAnimationValues()

                        print(values)
                        content = tpl.safe_substitute(dict(
                            COLOR=COLOR,
                            BGCOLOR=BGCOLOR, animationValuesSot = values["valuesHumSot"],
                            animationValuesArena = values["valuesHumArena"] ,
                            animationValuesOutside = values["valuesHumOutside"] ))

                        content = content.encode('utf-8')
                        self.send_response(200)
                        self.send_header('Content-Type', content_type)
                        self.send_header('Content-Length', len(content))
                        # -------------------------------
                        # cookies
                        # cookie = http.cookies.SimpleCookie()
                        # self.stream.counter = self.stream.counter + 1
                        # # users.append(stream.counter)
                        # cookie['user_id'] = str(self.stream.counter)
                        #
                        # self.send_header("Set-Cookie", cookie.output(header='', sep=''))
                        # --------------------------------------------------------
                        # self.send_header('Last-Modified', self.date_time_string(time()))
                        self.end_headers()
                        self.wfile.write(content)

                    if self.path.endswith(".jpg"):
                        mimetype='image/jpg'
                        sendReply = True
                    if self.path.endswith(".gif"):
                        mimetype='image/gif'
                        sendReply = True
                    if self.path.endswith(".js"):
                        mimetype='application/javascript'
                        sendReply = True
                    if self.path.endswith("min.js.map"):
                        mimetype='application/javascript'
                        sendReply = True
                    if self.path.endswith(".css"):
                        mimetype='text/css'
                        sendReply = True
                    if self.path.endswith("min.css.map"):
                        mimetype='text/css'
                        sendReply = True
                    if self.path.endswith("slim.min.js"):
                        mimetype='application/javascript'
                        sendReply = True
                    if self.path.endswith(".png"):
                            mimetype='text/png'
                            sendReply = True
                    # if self.path.endswith(".h264"):
                    #         mimetype='text/png'
                    #         sendReply = True
                    if self.path.endswith(".woff2"):
                            mimetype='text/png'
                            sendReply = True
                    if self.path.endswith(".woff"):
                            mimetype='text/png'
                            sendReply = True
                    if self.path.endswith(".ttf"):
                            mimetype='text/png'
                            sendReply = True

                    if sendReply == True:
                        f = open(curdir + sep + self.path, 'rb')
                        self.send_response(200)
                        self.send_header('Content-type',mimetype)
                        self.end_headers()
                        self.wfile.write(f.read())
                        f.close()
                    return

                except IOError as ex:
                    self.send_error(404,'File Not Found: %s' % self.path)



# class StreamingHttpServer():
#     def startServer(self):
#         self.http_server = HTTPServer(('', HTTP_PORT), StreamingHttpHandler)
#         self.http_server.serve_forever()
#
#     def stopServer(self):
#         self.http_server.socket.close()
