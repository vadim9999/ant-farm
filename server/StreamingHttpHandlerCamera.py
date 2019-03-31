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
from .Streaming import Streaming
from .RecordVideo import RecordVideo

WIDTH = 640
HEIGHT = 480
FRAMERATE = 24
HTTP_PORT = 8002
WS_PORT = 8084
COLOR = u'#444'
BGCOLOR = u'#FFFFFF'



# streaming = False
# connectedClients = 0


class StreamingHttpHandlerCamera(BaseHTTPRequestHandler):
    stream = Streaming()
    recordVideo = RecordVideo()
    # def startRecording(self):
    #     print("Start Recording")
    #     self.camera = picamera.PiCamera(resolution='640x480', framerate=24)

    # def stopStreaming(self):
    #     global streaming
    #     streaming = False

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

        if self.path == "/start_record":
            self.send_response(200)
            self.end_headers()
            print("_____start_recording_video____")

            # self.recordVideo.test()

            # print(self.rfile.read(int(self.headers['Content-Length'])))
            filename = self.rfile.read(int(self.headers['Content-Length']))
            # print(self.stream.test())
            camera = self.stream.getCamera()
            print(str(filename))
            self.recordVideo.startRecording(str(filename), True, camera)
            self.wfile.write("ok".encode('utf-8'))

        



    #Handler for the GET requests
    def do_GET(self):
            if self.path == '/':
                self.send_response(301)
                self.stream.counter = self.stream.counter + 1
                print("_________counter_____________")
                print(self.stream.counter)
                self.send_header('Location', '/index.html?id='+str(self.stream.counter))
                self.end_headers()
                return
            elif self.path == '/sensors':
                content_type = 'text/html; charset=utf-8'
                data = {
                    "sot":{
                        "temp":26,
                        "hum":70,
                    }
                }
                # data["sot"]["temp"]
                #
                content = str([[21,60],[22,70],[20,85],2])
                content = content.encode('utf-8')

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
                if len(query) != 0:
                    userId = int(query["id"])
                    print(query["id"])

                if self.path == "/index.html":
                    self.path = 'templates/index.html'

                if self.path == "/video":
                    self.path = '/video.h264'
                # migrate from post
                if self.path == '/test':
                    self.path = "templates/test.html"
                # self.send_response(200)
                # self.end_headers()
                    # print(self.rfile.read(int(self.headers['Content-Length'])))
                    # self.wfile.write("hello".encode('utf-8'))

                if self.path == "/stop_record":
                    self.send_response(200)
                    self.end_headers()
                    print("_____stop_recording_video____")
                    print(self.rfile.read(int(self.headers['Content-Length'])))
                    self.recordVideo.stopRecording()
                    self.wfile.write("ok".encode('utf-8'))
        # -------------------------------------
                if self.path == "/stop":
                    self.send_response(200)
                    self.end_headers()
                    # global connectedClients
                    # if(connectedClients == 0):
                    # self.stream.startRecording()
                    # self.stopStreaming()
                    # -------------------------------
                    # cookies
                    # C = http.cookies.SimpleCookie(self.headers["Cookie"])
                    # print(C['user_id'].value)
                    # self.stream.stopRecording(C['user_id'].value)
                # --------------------------------
                    if(userId != 0):
                        self.stream.stopRecording(userID = userId)
                        print(self.rfile.read(int(self.headers['Content-Length'])))
                        self.wfile.write("hello".encode('utf-8'))

                if self.path == '/wait_start_preview':
                    self.send_response(200)
                    self.end_headers()
                    while True:
                        if self.stream.startedStream == True:
                            break
                        sleep(1)
                    print(self.rfile.read(int(self.headers['Content-Length'])))
                    self.wfile.write("hello".encode('utf-8'))

                if self.path == '/start_stream':
                    self.send_response(200)
                    self.end_headers()
                    print("_______start_stream")
                    print("UserId")
                    print(userId)
                    print(self.rfile.read(int(self.headers['Content-Length'])))
                    self.wfile.write("hello".encode('utf-8'))
                    self.stream.stopRecording(stopPreviewAllUsers = True)
                    print("_________After Stopping recording_________")
                    self.stream.startStream(userID = userId)


                if self.path == "/stop_stream":
                    self.send_response(200)
                    self.end_headers()
                    print("_________________Stop stream____")
                    self.stream.stopRecording(stopPreviewAllUsers = True)
                    self.stream.stopStream()
                    print(self.rfile.read(int(self.headers['Content-Length'])))
                    self.wfile.write("hello".encode('utf-8'))

        # -------------------------------------
                # -------

                #-----------finding video files
                if self.path == "/videos":
                    print("In videos")
                    content_type = 'text/html; charset=utf-8'
                    mypath = "./videos/"
                    fileNames = [f for f in listdir(mypath) if isfile(join(mypath, f))]
                    fileNames = str(fileNames)
                    content = fileNames.encode("utf-8")
                    self.send_response(200)
                    self.send_header('Content-Type', content_type)
                    self.send_header('Content-Length', len(content))
                    # @TODO add last modified
                    self.end_headers()
                    self.wfile.write(content)
                # --------------------------------

                if self.path == "/stop":
                    self.send_response(200)
                    self.streaming = False

                if self.path == "/start":


                    # global connectedClients
                    # if(connectedClients == 0):
                    # self.stream.startRecording()
                    # self.stopStreaming()

                    # uncoment this code
                    # @TODO add video resolution

                    self.stream.startRecording()

                    self.send_response(200)
                    self.send_header('Content-Type', content_type)
                    # self.send_header('Content-Length', len(content))
                    # @TODO add last modified
                    self.end_headers()

                    # print(self.rfile.read(int(self.headers['Content-Length'])))
                    # self.wfile.write("hello".encode('utf-8'))

                if self.path == '/test':
                    self.stream.sendFromStream(self)

                if self.path == '/stream.mjpg':
                    print("*************/stream.mjpg")
                    if userId != 0:
                        print("UserId in stream/mjpg")
                        self.stream.startPreview(self, userId)



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
                        sotHum = 60

                        values = ("0 200; {0:0} 180; {1} 150; {2} 135; {2} 135;".format(int(sotHum/3), int(sotHum/2), sotHum))
                        print(values)
                        content = tpl.safe_substitute(dict(
                            WS_PORT=WS_PORT, WIDTH=WIDTH, HEIGHT=HEIGHT, COLOR=COLOR,
                            BGCOLOR=BGCOLOR, animationValues = values))

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
                    if self.path.endswith(".png"):
                            mimetype='text/png'
                            sendReply = True
                    if self.path.endswith(".h264"):
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
