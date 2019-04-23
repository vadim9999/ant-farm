import io
import logging
import socketserver
from threading import Condition

from os import curdir, sep
from string import Template
from wsgiref.simple_server import make_server
from threading import Thread
from ws4py.websocket import WebSocket
import sys 

from server.BluetoothServer import BluetoothServer
from server.thread_with_trace import thread_with_trace

from time import sleep, time


def main():
    try:
        
        bluetooth = BluetoothServer()
        bluetooth.run_server()
        
    except KeyboardInterrupt:
        print("keyBoard from setup")
        
    finally:
        print("finnaly")
        
        print("StartedKill")
        sys.exit() 
        if not bluetooth.isAlive(): 
            print('thread killed') 
       
if __name__ == '__main__':
    main()
