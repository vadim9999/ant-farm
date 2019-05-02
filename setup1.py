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
# from server.StreamingHttpHandler import StreamingHttpHandler
from server.StreamingHttpHandler import StreamingHttpHandler
from time import sleep, time

WIDTH = 640
HEIGHT = 480
FRAMERATE = 24
HTTP_PORT = 8003
WS_PORT = 8084
COLOR = u'#444'
BGCOLOR = u'#FFFFFF'


class StreamingServer(socketserver.ThreadingMixIn, HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


def main():
    try:
        server = StreamingServer(('', HTTP_PORT), StreamingHttpHandler)
        print ('Started httpserver on port ' , HTTP_PORT)#
        server.serve_forever()
    finally:
        server.socket.close()

if __name__ == '__main__':
    main()
