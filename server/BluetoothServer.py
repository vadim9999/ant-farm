# import bluetooth
from bluetooth import *
import subprocess
import sys 
import trace 
import threading 
import os
import time
import json

from socket import error as socket_error
from .WIFIConnector import WIFIConnector

class BluetoothServer():
    
    def run_server(self):
        subprocess.call(['sudo', 'hciconfig', 'hci0', 'piscan'])
        self.connected = False
        self.server_sock=BluetoothSocket( RFCOMM )
        
        self.server_sock.bind(("",PORT_ANY))
        self.server_sock.listen(1)

        port = self.server_sock.getsockname()[1]

        uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

        advertise_service(self.server_sock, "SampleServer",
                          service_id=uuid,
                          service_classes=[uuid, SERIAL_PORT_CLASS],
                          profiles=[SERIAL_PORT_PROFILE],
                          #                   protocols = [ OBEX_UUID ]
                          )
        try:

            while True:
                print("Waiting for connection on RFCOMM channel %d" % port)
                self.connected = False
                self.client_sock, client_info = self.server_sock.accept()
                
                self.connected = True
                print("Accepted connection from ", client_info)
                wifiConnector = WIFIConnector()
                
                try:
                    while True:
                        data = self.client_sock.recv(1024)            
                        decodedData = str(data.decode("utf-8"))
                        receivedData = json.loads(decodedData)                       
                        
                        if receivedData["request"] == "getWIFIData":                            
                            
                            networks = wifiConnector.getWIFINetworks()                                                     
                            p = subprocess.Popen(['iwgetid', '-r'], stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
                            out, err = p.communicate()
                            time.sleep(1)

                            router = out.split(b'\n')[0].decode("utf-8")
                            
                            data = {
                                "request": "getWIFIData",
                                "router": router,
                                "data": networks
                            }

                            jsonStr = json.dumps(data) + "\n"
                            self.client_sock.send(jsonStr.encode("utf-8"))
                            
                        
                        if receivedData["request"] == "setWIFIData":
                            network = receivedData["network"]
                            password = receivedData["password"]
                            ip_address = wifiConnector.wifi_connect(network,password)
                            
                            data = {
                                "request": "setWIFIData",
                                "ipAddress": ip_address
                            }

                            dataJson = json.dumps(data) + "\n"
                            self.client_sock.send(dataJson.encode("utf-8"))
                            

                        if receivedData["request"] == "getIP":
                            ip = wifiConnector.getIP()
                            data = {
                                "request":"getIP",
                                "ip":ip
                            }
                            dataJson = json.dumps(data) + "\n"
                            self.client_sock.send(dataJson.encode("utf-8"))
                           
        
                except IOError:
                    print("Exception _")
                    
        
        except Exception as e:
            print(e)

        finally:
            print("disconnected")
            if self.connected == True:
                self.client_sock.close()
            self.server_sock.close()

    def shutdown(self):
        self.server_sock.close()
        



