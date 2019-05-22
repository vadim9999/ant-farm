
import socketserver
from http.server import HTTPServer
from server.StreamingHttpHandler import StreamingHttpHandler

WIDTH = 640
HEIGHT = 480
FRAMERATE = 24
HTTP_PORT = 80
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
