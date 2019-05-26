import io
from http.server import BaseHTTPRequestHandler
from os import curdir, sep
from string import Template
from time import sleep
import urllib.parse as urlparse
from .Streaming import Streaming
from .RecordVideo import RecordVideo
from .CaptureImage import CaptureImage
from .ControlServo import ControlServo
from .Sensors import Sensors
from os import listdir
from os.path import isfile, join
import os
import shutil
import json
from subprocess import call

counter = 0
connectedUsers = [1]
class StreamingHttpHandlerCamera(BaseHTTPRequestHandler):
    stream = Streaming()
    recordVideo = RecordVideo()
    captureImage = CaptureImage()
    sensors = Sensors()
    feeder = ControlServo()

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
            data = self.rfile.read(int(self.headers['Content-Length']))
            data = str(data.decode("utf-8"))
            data = json.loads(data)
            camera = self.stream.getCamera()
            self.recordVideo.startRecording(
                data["filename"], data["resolution"], True, camera, userId)
            self.wfile.write("ok".encode('utf-8'))

        if self.path == "/capture_image":
            self.send_response(200)
            self.end_headers()
            camera = self.stream.getCamera()
            data = self.rfile.read(int(self.headers['Content-Length']))
            data = str(data.decode("utf-8"))
            data = json.loads(data)
            self.captureImage.takeImage(
                data["filename"], data["resolution"], camera, True)

        if self.path == "/start":
            self.send_response(200)
            self.end_headers()
            resolution = str(self.rfile.read(
                int(self.headers['Content-Length'])).decode("utf-8"))
            self.stream.startRecording(resolution)

        if self.path == '/start_stream':
            self.send_response(200)
            self.end_headers()
            self.wfile.write("hello".encode('utf-8'))
            self.stream.stopRecording(stopPreviewAllUsers=True)
            resolution = str(self.rfile.read(
                int(self.headers['Content-Length'])).decode("utf-8"))
            self.stream.startStream(userID=userId, resolution1=resolution)

        if self.path == '/set_stream_settings':
            self.send_response(200)
            self.end_headers()
            data = str(self.rfile.read(
                int(self.headers['Content-Length'])).decode("utf-8"))
            settings = json.loads(data)
            self.stream.setYoutubeKey(settings["youtube"], settings["key"])
            self.wfile.write(data.encode('utf-8'))

        if self.path == "/set_settings_feeder":
            self.send_response(200)
            self.end_headers()
            data = self.rfile.read(int(self.headers['Content-Length']))
            data = int(data.decode("utf-8"))
            time = data * 86400
            self.feeder.feedAfter(time)

    def do_GET(self):

        if self.path == '/':
            self.send_response(301)
            global counter
            counter = counter + 1
            self.send_header('Location', '/index.html?id='+str(counter))  
            self.end_headers()
            return

        elif self.path == '/sensors':
            content_type = 'text/html; charset=utf-8'

            connectedId = 0
            if self.stream.isStartedPreview() == True:
                if self.stream.isStartedStream() == True:
                    connectedId = self.stream.getConnectedUserId()
                elif self.recordVideo.isStartedRecording() == True:
                    connectedId = self.recordVideo.getConnectedUserId()

            content = (self.sensors.getSensorsData(
                connectedId)).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)

        else:
            url_parts = list(urlparse.urlparse(self.path))
            self.path = url_parts[2]
            query = dict(urlparse.parse_qsl(url_parts[4]))
            userId = 0

            if url_parts[2].startswith('/download') == True:
                urls = url_parts[2].split("/")

                filepath = "media/" + urls[2]
                with open(filepath, 'rb') as f:
                    self.send_response(200)
                    self.send_header(
                        "Content-Type", 'application/octet-stream')
                    self.send_header(
                        "Content-Disposition", 'attachment; filename="{}"'.format(os.path.basename(filepath)))
                    fs = os.fstat(f.fileno())
                    self.send_header("Content-Length", str(fs.st_size))
                    self.end_headers()
                    shutil.copyfileobj(f, self.wfile)

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

            if len(query) != 0:
                userId = int(query["id"])

            if self.path == "/index.html":
                self.path = 'templates/index.html'

            # -----------feeder-----------------
            if self.path == "/feed":
                self.send_response(200)
                self.end_headers()
                self.feeder.feed()

            # ------------stream------------------
            if self.path == '/stream_settings':
                self.send_response(200)
                self.end_headers()
                data = self.stream.getYoutubeKey()
                self.wfile.write(data.encode('utf-8'))

            if self.path == "/stop_stream":
                self.send_response(200)
                self.end_headers()
                self.stream.stopRecording(stopPreviewAllUsers=True)
                self.stream.stopStream()
                self.wfile.write("hello".encode('utf-8'))

            # ----------record------------------------
            if self.path == "/stop_record":
                self.send_response(200)
                self.end_headers()
                self.recordVideo.stopRecording()
                self.wfile.write("ok".encode('utf-8'))

            # -----------media-----------------
            if self.path == "/media":
                content_type = 'text/html; charset=utf-8'
                mypath = "./media/"
                fileNames = [f for f in listdir(
                    mypath) if isfile(join(mypath, f))]
                if len(fileNames) > 0:
                    fileNames = str(fileNames)
                else:
                    fileNames = ""

                content = fileNames.encode("utf-8")
                self.send_response(200)
                self.send_header('Content-Type', content_type)
                self.send_header('Content-Length', len(content))
                self.end_headers()
                self.wfile.write(content)

            # shtdown & reboot RPI
            if self.path == "/shutdown_pi":
                self.send_response(200)
                self.end_headers()
                call("sudo shutdown -h now", shell=True)
            
            if self.path == "/reboot_pi":
                self.send_response(200)
                self.end_headers()
                call("sudo reboot", shell=True)

            # --------preview--------
            if self.path == "/stop":
                self.send_response(200)
                self.end_headers()
                if(userId != 0):
                    self.stream.stopRecording(userID=userId)

            if self.path == '/wait_start_preview':
                self.send_response(200)
                self.end_headers()
                while True:
                    if self.stream.startedStream == True:
                        break
                    sleep(1)
                self.wfile.write("hello".encode('utf-8'))
            # --------------------------------

            if self.path == '/stream.mjpg':
                if userId != 0:
                    self.stream.startPreview(self, userId)

            try:

                sendReply = False
                if self.path.endswith(".html"):
                    global connectedUsers
                    if userId in connectedUsers:
                        self.send_response(301)
                            
                        counter = counter + 1
                            
                        print("_________counter22122_____________")

                        self.send_header('Location', '/index.html?id='+str(counter))
                        self.end_headers()
                    else:
                        connectedUsers.append(userId)
                        print('it is html ')
                        mimetype = 'text/html'
                        content_type = 'text/html; charset=utf-8'
                        with io.open(self.path, 'r') as f:
                            index_template = f.read()
                        tpl = Template(index_template)
                        values = self.sensors.getAnimationValues()
                        content = tpl.safe_substitute(dict(
                            animationValuesSot=values["valuesHumSot"],
                            animationValuesArena=values["valuesHumArena"],
                            animationValuesOutside=values["valuesHumOutside"]))

                        content = content.encode('utf-8')
                        self.send_response(200)
                        self.send_header('Content-Type', content_type)
                        self.send_header('Content-Length', len(content))
                        self.end_headers()
                        self.wfile.write(content)

                if self.path.endswith(".jpg"):
                    mimetype = 'image/jpg'
                    sendReply = True
                if self.path.endswith(".gif"):
                    mimetype = 'image/gif'
                    sendReply = True
                if self.path.endswith(".js"):
                    mimetype = 'application/javascript'
                    sendReply = True
                if self.path.endswith("min.js.map"):
                    mimetype = 'application/javascript'
                    sendReply = True
                if self.path.endswith(".css"):
                    mimetype = 'text/css'
                    sendReply = True
                if self.path.endswith("min.css.map"):
                    mimetype = 'text/css'
                    sendReply = True
                if self.path.endswith(".png"):
                    mimetype = 'text/png'
                    sendReply = True
                if self.path.endswith(".woff2"):
                    mimetype = 'text/png'
                    sendReply = True
                if self.path.endswith(".woff"):
                    mimetype = 'text/png'
                    sendReply = True
                if self.path.endswith(".ttf"):
                    mimetype = 'text/png'
                    sendReply = True

                if sendReply == True:
                    f = open(curdir + sep + self.path, 'rb')
                    self.send_response(200)
                    self.send_header('Content-type', mimetype)
                    self.end_headers()
                    self.wfile.write(f.read())
                    f.close()
                return

            except IOError as ex:
                self.send_error(404, 'File Not Found: %s' % self.path)

