import socketserver
from threading import Condition
from http.server import HTTPServer, BaseHTTPRequestHandler
from glob import glob
from os import curdir, sep
from string import Template
from wsgiref.simple_server import make_server
from threading import Thread
from ws4py.websocket import WebSocket
import sys 

from server.StreamingHttpHandlerCamera import StreamingHttpHandlerCamera
from server.BluetoothServer import BluetoothServer

HTTP_PORT = 80

class StreamingServer(socketserver.ThreadingMixIn, HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


def main():
    try:
        http_server = StreamingServer(('', HTTP_PORT), StreamingHttpHandlerCamera)
       
        bluetooth = BluetoothServer()
        bluetooth_thread = Thread(target = bluetooth.run_server)
        bluetooth_thread.daemon = True
        print("Starting Bluetooth server")
        bluetooth_thread.start()

        print ('Started httpserver on port ' , HTTP_PORT)
        http_server.serve_forever()
        
    except KeyboardInterrupt:
        print("keyBoard from setup")
        
    finally:
        print("shutdown http_server")
        http_server.socket.close()
        print("wait bluetooth")
        sys.exit() 

        if not bluetooth_thread.isAlive(): 
            print('thread killed') 
        
if __name__ == '__main__':
    main()
