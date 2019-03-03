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
from server.StreamingHttpHandler import StreamingHttpHandler

WIDTH = 640
HEIGHT = 480
FRAMERATE = 24
HTTP_PORT = 8002
WS_PORT = 8084
COLOR = u'#444'
BGCOLOR = u'#FFFFFF'



def main():
    try:
	#Create a web server and define the handler to manage the
	#incoming request
        http_server = HTTPServer(('', HTTP_PORT), StreamingHttpHandler)
        print ('Started httpserver on port ' , HTTP_PORT)#
    # Wait forever for incoming htto requests
        http_server.serve_forever()
    except KeyboardInterrupt:
	    print ('^C received, shutting down the web server')
	    http_server.socket.close()
#     http_thread = Thread(target=http_server.serve_forever)
#     address = ('', HTTP_PORT)
# server = StreamingHttpServer(address, StreamingHandler)
# server.serve_forever()
if __name__ == '__main__':
    main()
