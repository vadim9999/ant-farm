import io
import logging
import socketserver
from threading import Condition
from http.server import HTTPServer, BaseHTTPRequestHandler
import pymjpeg
from glob import glob
from os import curdir, sep
from string import Template
from wsgiref.simple_server import make_server
from threading import Thread

WIDTH = 640
HEIGHT = 480
FRAMERATE = 24
HTTP_PORT = 8002
WS_PORT = 8084
COLOR = u'#444'
BGCOLOR = u'#333'

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

class StreamingHandler(BaseHTTPRequestHandler):

    #Handler for the GET requests
    def do_GET(self):
            print(self.path)
            if self.path=="/":
                    self.path="/index.html"

            # if self.path == '/stream.mjpg':
            #     self.send_response(200)
            # # Response headers (multipart)
            #     for k, v in pymjpeg.request_headers().items():
            #         self.send_header(k, v)
            #         # Multipart content
            #     for filename in glob('img/*'):
            #     # Part boundary string
            #         self.end_headers()
            #         self.wfile.write(pymjpeg.boundary.encode("utf-8"))
            #         self.end_headers()
            #         # Part headers
            #         for k, v in pymjpeg.image_headers(filename).items():
            #             self.send_header(k, v)
            #         self.end_headers()
            #         # Part binary
            #         for chunk in pymjpeg.image(filename):
            #             self.wfile.write(chunk)


            try:
                #Check the file extension required and
                #set the right mime type
                print("block try")
                sendReply = False
                if self.path.endswith(".html"):
                    mimetype='text/html'
                    sendReply = True
                if self.path.endswith(".jpg"):
                    mimetype='image/jpg'
                    sendReply = True
                if self.path.endswith(".gif"):
                    mimetype='image/gif'
                    sendReply = True
                if self.path.endswith(".js"):
                    mimetype='application/javascript'
                    sendReply = True
                if self.path.endswith(".css"):
                    mimetype='text/css'
                    sendReply = True
                if self.path.endswith(".png"):
                        mimetype='text/png'
                        sendReply = True

                if sendReply == True:
                    f = open(curdir + sep + self.path, 'rb')
                    self.send_response(200)
                    # self.send_header('Content-type',mimetype)
                    content_type = 'text/html; charset=utf-8'
                    self.send_header('Content-Type', content_type)
                    # self.index_template = "ok"
                    tpl = Template(self.server.index_template)
                    content = tpl.safe_substitute(dict(
                        WS_PORT=WS_PORT, WIDTH=WIDTH, HEIGHT=HEIGHT, COLOR=COLOR,
                        BGCOLOR=BGCOLOR))
                    content = content.encode('utf-8')
                    self.send_header('Content-Length', len(content))
                    self.end_headers()
                    self.wfile.write(f.read())
                    f.close()

                    return

            except IOError:
                self.send_error(404,'File Not Found: %s' % self.path)

# class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
#                             allow_reuse_address = True
#                             daemon_threads = True
#                             index_template = "Ok"
class StreamingHttpServer(HTTPServer):
    def __init__(self):
        super(StreamingHttpServer, self).__init__(
            ('', HTTP_PORT), StreamingHandler)
        self.index_template = "OK"


                            #with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
    # output = StreamingOutput()
    #camera.start_recording(output, format='mjpeg')
def main():
    http_server = StreamingHttpServer()
    http_server.serve_forever()
    # http_thread = Thread(target=http_server.serve_forever)
    # address = ('', HTTP_PORT)
# server = StreamingHttpServer(address, StreamingHandler)
# server.serve_forever()