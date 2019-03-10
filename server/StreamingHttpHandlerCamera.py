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

WIDTH = 640
HEIGHT = 480
FRAMERATE = 24
HTTP_PORT = 8002
WS_PORT = 8084
COLOR = u'#444'
BGCOLOR = u'#FFFFFF'

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

# streaming = False
# connectedClients = 0
class Streaming():
    streaming = False
    connectedClients = 0
    startedRecording = False
    counter = 0
    users = []
    stoppedUserId = 0
    def stopRecording(self,userID):
        self.stoppedUserId = userID

    def sendFromStream(self, selfed):
        selfed.send_response(304)

    def startRecording(self):
        print("StartedRecording")
        print(self.startedRecording)
        if(self.startedRecording == False):
            self.camera = picamera.PiCamera(resolution='640x480', framerate=24)
            self.output = StreamingOutput()
            self.camera.start_recording(self.output, format='mjpeg')
            self.startedRecording = True
            self.streaming = True

    def streamPreview(self,selfed):
        C = http.cookies.SimpleCookie(selfed.headers["Cookie"])
        userId = C['user_id'].value
        print(userId)
        # global connectedClients
        if(self.startedRecording == True):
            selfed.send_response(200)
            selfed.send_header('Age', 0)
            selfed.send_header('Cache-Control', 'no-cache, private')
            selfed.send_header('Pragma', 'no-cache')
            selfed.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            selfed.end_headers()
            sleep(1)
            self.camera.wait_recording(1)

            self.connectedClients = self.connectedClients + 1
            print("users")
            print(str(self.connectedClients))

            # global streaming
            # streaming = True
            self.streaming = True
            try:
                print("try and below while")
                while (userId != self.stoppedUserId):
                    try:
                        with self.output.condition:
                            self.output.condition.wait()
                            frame = self.output.frame
                    except Exception as e:
                        print("!!!!exception " + str(e))

                    selfed.wfile.write(b'--FRAME\r\n')
                    selfed.send_header('Content-Type', 'image/jpeg')
                    selfed.send_header('Content-Length', len(frame))
                    selfed.end_headers()
                    selfed.wfile.write(frame)
                    selfed.wfile.write(b'\r\n')
                self.stoppedUserId = 0
                self.connectedClients = self.connectedClients - 1

                print("******continue execute code")
                selfed.wfile.write(b'--FRAME\r\n')
                selfed.send_header('Content-Type', 'image/jpeg')
                selfed.send_header('Content-Length', len(b''))
                selfed.end_headers()
                selfed.wfile.write(b'')
                selfed.wfile.write(b'\r\n')

            except Exception as e:
                self.connectedClients = self.connectedClients - 1
                logging.warning(
                    'Removed streaming client %s: %s',
                    selfed.client_address, str(e))
            finally:
                print("Stopping camera")
                if (self.connectedClients == 0):
                    print("O users")
                    print(str(self.connectedClients))
                    self.startedRecording = False
                    self.camera.stop_recording()
                    self.camera.close()
        else:
            selfed.send_response(200)
            selfed.end_headers()


class StreamingHttpHandlerCamera(BaseHTTPRequestHandler):
    stream = Streaming()

    # def startRecording(self):
    #     print("Start Recording")
    #     self.camera = picamera.PiCamera(resolution='640x480', framerate=24)

    # def stopStreaming(self):
    #     global streaming
    #     streaming = False

    def do_HEAD(self):
        self.do_GET()

    def do_POST(self):
        if self.path == "/start":
            self.send_response(200)
            self.end_headers()
            # global connectedClients
            # if(connectedClients == 0):
            # self.stream.startRecording()
            # self.stopStreaming()

            # uncoment this code
            # self.stream.startRecording()

            print(self.rfile.read(int(self.headers['Content-Length'])))
            self.wfile.write("hello".encode('utf-8'))

        if self.path == "/stop":
            self.send_response(200)
            self.end_headers()
            # global connectedClients
            # if(connectedClients == 0):
            # self.stream.startRecording()
            # self.stopStreaming()

            C = http.cookies.SimpleCookie(self.headers["Cookie"])
            print(C['user_id'].value)
            self.stream.stopRecording(C['user_id'].value)
            
            print(self.rfile.read(int(self.headers['Content-Length'])))
            self.wfile.write("hello".encode('utf-8'))


    #Handler for the GET requests
    def do_GET(self):
            if self.path == '/':
                self.send_response(301)
                # self.stream.counter = self.stream.counter + 1

                self.send_header('Location', '/index.html?id=3')
                self.end_headers()
                return
            else:
                url_parts = list(urlparse.urlparse(self.path))
                self.path = url_parts[2]
                query = dict(urlparse.parse_qsl(url_parts[4]))
                if len(query) != 0:
                    print(query["id"])

                if self.path == "/index.html":
                    self.path = 'templates/index.html'

                if self.path == "/ok":
                    self.path = 'templates/ok.html'

                if self.path == "/stop":
                    self.send_response(200)
                    self.streaming = False

                if self.path == '/sensors':
                    content_type = 'text/html; charset=utf-8'
                    content = str([[21,60],[22,70],[20,85],2])
                    content = content.encode('utf-8')

                    self.send_response(200)
                    self.send_header('Content-Type', content_type)
                    self.send_header('Content-Length', len(content))
                    # @TODO add last modified
                    self.end_headers()
                    self.wfile.write(content)
                if self.path == '/test':
                    self.stream.sendFromStream(self)

                if self.path == '/stream.mjpg':
                    print("*************/stream.mjpg")

                    # self.stream.streamPreview(self)

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
