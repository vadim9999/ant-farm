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
from ws4py.websocket import WebSocket

WIDTH = 640
HEIGHT = 480
FRAMERATE = 24
HTTP_PORT = 8002
WS_PORT = 8084
COLOR = u'#444'
BGCOLOR = u'#FFFFFF'


class StreamingHttpHandler(BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.do_GET()

    #Handler for the GET requests
    def do_GET(self):
            print(self.path)
            if self.path == "/":
                self.send_response(301)
                self.send_header('Location', '/index.html')
                self.end_headers()
                return
            elif self.path == '/main.js':
                content_type = 'application/javascript'
                content = self.server.main_content
            elif self.path == '/jsmpg.js':
                content_type = 'application/javascript'
                content = self.server.jsmpg_content
            elif self.path == '/index.html':
                content_type = 'text/html; charset=utf-8'
                tpl = Template(self.server.index_template)
                content = tpl.safe_substitute(dict(
                    WS_PORT=WS_PORT, WIDTH=WIDTH, HEIGHT=HEIGHT, COLOR=COLOR,
                    BGCOLOR=BGCOLOR))
            elif self.path == '/sensors':
                content_type = 'text/html; charset=utf-8'
                content = str([[21,80],[22,70],[20,85],2])

            else:
                self.send_error(404, 'File not found')
                return

            content = content.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', len(content))
            # @TODO add last modified
            self.end_headers()
            self.wfile.write(content)

            #@TODO add method POST for /sensors

            # try:
            #     #Check the file extension required and
            #     #set the right mime type
            #     print("block try")
            #     sendReply = False
            #     if self.path.endswith(".html"):
            #         mimetype='text/html'
            #         sendReply = True
            #     if self.path.endswith(".jpg"):
            #         mimetype='image/jpg'
            #         sendReply = True
            #     if self.path.endswith(".gif"):
            #         mimetype='image/gif'
            #         sendReply = True
            #     if self.path.endswith(".js"):
            #         mimetype='application/javascript'
            #         sendReply = True
            #     if self.path.endswith(".css"):
            #         mimetype='text/css'
            #         sendReply = True
            #     if self.path.endswith(".png"):
            #             mimetype='text/png'
            #             sendReply = True

                # if sendReply == True:
                #     f = open(curdir + sep + self.path, 'rb')
                #     self.send_response(200)
                #     # self.send_header('Content-type',mimetype)
                #     content_type = 'text/html; charset=utf-8'
                #     self.send_header('Content-Type', content_type)
                #     # self.index_template = "ok"
            #         tpl = Template(self.server.index_template)
            #         content = tpl.safe_substitute(dict(
            #             WS_PORT=WS_PORT, WIDTH=WIDTH, HEIGHT=HEIGHT, COLOR=COLOR,
            #             BGCOLOR=BGCOLOR))
            #         content = content.encode('utf-8')
            #         self.send_header('Content-Length', len(content))
            #         self.end_headers()
            #         self.wfile.write(f.read())
            #         f.close()
            #
            #         return
            #
            # except IOError:
            #     self.send_error(404,'File Not Found: %s' % self.path)

# class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
#                             allow_reuse_address = True
#                             daemon_threads = True
#                             index_template = "Ok"
class StreamingHttpServer(HTTPServer):
    def __init__(self):
        super(StreamingHttpServer, self).__init__(
            ('', HTTP_PORT), StreamingHttpHandler)
        with io.open('index.html', 'r') as f:
            self.index_template = f.read()
        with io.open('main.js', 'r') as f:
            self.main_content = f.read()
        with io.open('jsmpg.js', 'r') as f:
            self.jsmpg_content = f.read()


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
if __name__ == '__main__':
    main()