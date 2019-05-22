import io
import logging
from threading import Condition
import picamera
from time import sleep
import subprocess
import os
import signal
import json


class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)


class Streaming():
    connectedClients = 0
    startedPreview = False
    startedStream = False
    users = []
    stoppedUserId = 0
    deleteUsers = False
    splitter_port = False
    connectedUserId = 0
    youtube = ""
    key = ""

    def isStartedPreview(self):
        return self.startedPreview

    def getCamera(self):
        return self.camera

    def isStartedStream(self):
        return self.startedStream

    def getConnectedUserId(self):
        return self.connectedUserId
    # ------------------

    def startCamera(self, resolution1):
        self.camera = picamera.PiCamera(resolution=resolution1, framerate=24)
        self.output = StreamingOutput()

    # *********Preview***********
    def startPreview(self, selfed, user_Id):

        if(self.startedPreview == True):
            selfed.send_response(200)
            selfed.send_header('Age', 0)
            selfed.send_header('Cache-Control', 'no-cache, private')
            selfed.send_header('Pragma', 'no-cache')
            selfed.send_header(
                'Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            selfed.end_headers()
            sleep(1)
            self.camera.wait_recording(1)

            self.connectedClients = self.connectedClients + 1
            self.users.append(user_Id)

            try:

                while (user_Id != self.stoppedUserId):
                    try:
                        with self.output.condition:
                            self.output.condition.wait()
                            frame = self.output.frame

                    except Exception as e:
                        print("!!!!exception " + str(e))

                    selfed.wfile.write(b'--FRAME\r\n')
                    selfed.send_header('Content-Type', 'image/jpeg')
                    selfed.send_header('Content-Length', len(frame))
                    selfed.end_headers()
                    selfed.wfile.write(frame)
                    selfed.wfile.write(b'\r\n')
                self.stoppedUserId = 0
                self.connectedClients = self.connectedClients - 1
                if self.deleteUsers == True:
                    self.users.remove(user_Id)

                selfed.wfile.write(b'--FRAME\r\n')
                selfed.send_header('Content-Type', 'image/jpeg')
                selfed.send_header('Content-Length', len(b''))
                selfed.end_headers()
                selfed.wfile.write(b'')
                selfed.wfile.write(b'\r\n')

            except Exception as e:
                self.connectedClients = self.connectedClients - 1
                logging.warning(
                    'Removed streaming client %s: %s',
                    selfed.client_address, str(e))
            finally:
                if (self.connectedClients == 0):
                    print("O users")
                    print(str(self.connectedClients))
                    self.startedPreview = False
                    if self.splitter_port == True:
                        self.camera.stop_recording(splitter_port=2)
                        self.splitter_port = False
                    else:
                        self.camera.stop_recording()
                        self.camera.close()

        else:
            selfed.send_response(200)
            selfed.end_headers()

    def startRecording(self, resolution):
        if self.startedStream == True:
            self.splitter_port = True

        if self.splitter_port == True:
            self.camera.start_recording(
                self.output, splitter_port=2, format='mjpeg', resize=resolution)
            self.startedPreview = True
        else:
            if(self.startedPreview == False):
                self.startCamera(resolution)
                self.camera.start_recording(self.output, format='mjpeg')
                self.startedPreview = True

    def stopRecording(self, userID=0, stopPreviewAllUsers=False):
        if(stopPreviewAllUsers == True):
            self.deleteUsers = False
            for user in self.users:
                self.stoppedUserId = user
                sleep(2)
            self.users.clear()
        else:
            self.deleteUsers = True
            self.stoppedUserId = userID


# *************Stream***************

    def startRecordingStream(self):
        try:
            while self.startedStream == True:
                self.camera.wait_recording(1)
        except Exception as e:
        finally:
            self.camera.stop_recording()
            self.camera.close()
            os.killpg(os.getpgid(self.stream_pipe.pid), signal.SIGTERM)
            self.startedStream = False

    def setYoutubeKey(self, youtube, key):
        self.youtube = youtube
        self.key = key

    def getYoutubeKey(self):
        data = {
            "youtube": self.youtube,
            "key": self.key
        }
        return json.dumps(data)

    def startStream(self, userID=0, resolution1="640x480"):
        if self.startedStream != True and userID != 0:
            self.connectedUserId = userID
            stream_cmd = 'ffmpeg -f h264 -r 25 -i - -itsoffset 5.5 -fflags nobuffer -f lavfi -i anullsrc -c:v copy -c:a aac -strict experimental -f flv ' + self.youtube + "/" + self.key
            self.stream_pipe = subprocess.Popen(
                stream_cmd, shell=True, stdin=subprocess.PIPE, preexec_fn=os.setsid)
            self.startCamera(resolution1=resolution1)
            self.camera.vflip = True
            self.camera.hflip = True
            self.camera.start_recording(
                self.stream_pipe.stdin, format='h264', bitrate=20000000)

            self.startedStream = True
            self.startRecordingStream()

    def stopStream(self):
        self.startedStream = False
   