import socketserver
from http.server import HTTPServer
from server.StreamingHttpHandler import StreamingHttpHandler

HTTP_PORT = 80

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