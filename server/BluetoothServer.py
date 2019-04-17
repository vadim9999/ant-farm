# import bluetooth
from bluetooth import *
import subprocess
import sys 
import trace 
import threading 

from socket import error as socket_error
class BluetoothServer():
    
    def run_server(self):
        subprocess.call(['sudo', 'hciconfig', 'hci0', 'piscan'])
        self.connected = False
        self.server_sock=BluetoothSocket( RFCOMM )
        # self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
                router = "router"
                password = "password"
                try:
                    while True:

                        data = self.client_sock.recv(1024)
        # if len(data) == 0: break
                        print("received [%s]" % data)
                        print(data.decode("utf-8"))
                        decodedData = str(data.decode("utf-8"))
                        receivedData = decodedData.split("_")
                        print(receivedData)
                        print(decodedData == "getWIFIData")

                        if receivedData[0] == "getWIFIData":
                            print("write response wifi")
                            self.client_sock.send(("{\"name\": \"getWIFIData\", \"router\":\"" + router + "\",\"password\":\"" +  password +"\"}\n").encode("utf-8"))
                        if receivedData[0] == "setWIFIData":
                            router = receivedData[1]
                            password = receivedData[2]
                            print(router) 
                            print(password)
        # if decodedData == "setWIFIData\n"
        # client_sock.send("Received data!\n".encode("utf-8"))
                except IOError:
                    print("Exception _")
                    
        
        except (KeyboardInterrupt, BluetoothError) as e:
            print("Exception Bluetooth")
        finally:
            print("disconnected")
            if self.connected == True:
                self.client_sock.close()
            self.server_sock.close()
            print("all done") 
    def shutdown(self):
        self.server_sock.close()
        # self.server_sock.shutdown(socket.SHUT_RDWR)



