# import bluetooth
from bluetooth import *
import subprocess
# subprocess.call(['sudo', 'hciconfig', 'hci0', 'piscan'])

server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service( server_sock, "SampleServer",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ],
#                   protocols = [ OBEX_UUID ]
                    )

print("Waiting for connection on RFCOMM channel %d" % port)

client_sock, client_info = server_sock.accept()
print("Accepted connection from ", client_info)
router = "router"
password = "password"
try:
    while True:

        data = client_sock.recv(1024)
        # if len(data) == 0: break
        print("received [%s]" % data)
        print(data.decode("utf-8"))
        decodedData = str(data.decode("utf-8"))
        receivedData = decodedData.split("_")
        print(receivedData)
        print(decodedData == "getWIFIData")

        if receivedData[0] == "getWIFIData":
            print("write response wifi")
            client_sock.send(("{\"name\": \"getWIFIData\", \"router\":\"" + router + "\",\"password\":\"" +  password +"\"}\n").encode("utf-8"))
        if receivedData[0] == "setWIFIData":
            router = receivedData[1]
            password = receivedData[2]
            print(router) 
            print(password)
        # if decodedData == "setWIFIData\n"
        # client_sock.send("Received data!\n".encode("utf-8"))
except IOError:
    pass
finally:
    print("disconnected")

    client_sock.close()
    server_sock.close()
    print("all done")


