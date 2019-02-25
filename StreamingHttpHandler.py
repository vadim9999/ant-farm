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

    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        print(self.rfile.read(int(self.headers['Content-Length'])))
        self.wfile.write("hello".encode('utf-8'))

    #Handler for the GET requests
    def do_GET(self):
            print(self.path)
            if self.path == "/":
                self.path = '/index.html'

            if self.path == '/sensors':
                content_type = 'text/html; charset=utf-8'
                content = str([[21,80],[22,70],[20,85],2])
                content = content.encode('utf-8')

                self.send_response(200)
                self.send_header('Content-Type', content_type)
                self.send_header('Content-Length', len(content))
                # @TODO add last modified
                self.end_headers()
                self.wfile.write(content)

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
