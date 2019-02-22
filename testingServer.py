from wsgiref.simple_server import make_server
from ws4py.websocket import WebSocket
from ws4py.server.wsgirefserver import WSGIServer, WebSocketWSGIRequestHandler
from ws4py.server.wsgiutils import WebSocketWSGIApplication
from ws4py.streaming import Stream
from struct import Struct
from ws4py.messaging import  TextMessage
from ws4py.framing import Frame
from threading import Thread
from time import sleep, time

WIDTH = 640
HEIGHT = 480
FRAMERATE = 24
HTTP_PORT = 8082
WS_PORT = 8084
COLOR = u'#444'
BGCOLOR = u'#333'
JSMPEG_MAGIC = b'jsmp'
JSMPEG_HEADER = Struct('>4sHH')
VFLIP = False
HFLIP = False

class EchoWebSocket(WebSocket):
    def opened(self):
        print("send self")

        self.send("Connection is OK")
        # self.send(JSMPEG_HEADER.pack(JSMPEG_MAGIC, WIDTH, HEIGHT), binary=True)

    def received_message(self, message):
        print('I am in WebSocket')
        print(message)
        self.send(message, message.is_binary)

class BroadcastThread(Thread):
    def __init__(self, server):
        super(BroadcastThread, self).__init__()

        self.websocket_server = server

    def run(self):
        try:
            while True:
                buf = "ok"
                if buf:
                    self.websocket_server.manager.broadcast(buf, binary=False)
                    sleep(5)
                # elif self.converter.poll() is not None:
                #     break
        finally:
            print('Finnaly')

server = make_server('', 8084, server_class=WSGIServer,
                     handler_class=WebSocketWSGIRequestHandler,
                     app=WebSocketWSGIApplication(handler_cls = EchoWebSocket))

# test_mask = 'XXXXXX'
# f = Frame(OPCODE_TEXT, 'hello world', masking_key=test_mask, fin=1)
# bytes = f.build()
# bytes.encode('hex')

server.initialize_websockets_manager()
websocket_thread = Thread(target=server.serve_forever)
broadcast_thread = BroadcastThread(server)
try:

    print('Starting websockets thread')
    websocket_thread.start()

    print('Starting broadcast thread')
    broadcast_thread.start()
    while (True):
        sleep(10)
finally:
    print("error")
# from ws4py import configure_logger
# from ws4py.websocket import WebSocket
# from ws4py.messaging import Message, TextMessage
#
# logger = configure_logger(stdout=True)
#
# class DataSource(object):
#     def __init__(self):
#         self.frames = set()
#         self.frame = None
#         self.remaining_bytes = None
#
#     def setblocking(self, flag):
#         pass
#
#     def feed(self, message):
#         if isinstance(message, Message):
#             message = message.single(mask=True)
#         else:
#             message = TextMessage(message).single(mask=True)
#         self.frames.add(message)
#
#     def recv(self, size):
#         if not self.frame:
#             if not self.frames:
#                 return b''
#             self.frame = self.frames.pop()
#             self.remaining_bytes = self.frame
#
#         current_bytes = self.remaining_bytes[:size]
#         self.remaining_bytes = self.remaining_bytes[size:]
#
#         if self.remaining_bytes is b'':
#             self.frame = None
#             self.remaining_bytes = None
#
#         return current_bytes
#
# class LogWebSocket(WebSocket):
#     def opened(self):
#         logger.info("WebSocket now ready")
#
#     def closed(self, code=1000, reason="Burp, done!"):
#         logger.info("Terminated with reason '%s'" % reason)
#
#     def received_message(self, m):
#         logger.info("Received message: %s" % m)
#
# if __name__ == '__main__':
#     source = DataSource()
#     ws = LogWebSocket(sock=source)
#
#     source.feed(u'hello there')
#     source.feed(u'a bit more')
#
#     ws.run()