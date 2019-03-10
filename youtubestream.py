import subprocess
import picamera
import time
YOUTUBE="rtmp://b.rtmp.youtube.com/live2/"
KEY= "gv72-kf7z-ga1g-caqu"
stream_cmd = 'ffmpeg -f h264 -r 25 -i - -itsoffset 5.5 -fflags nobuffer -f lavfi -i anullsrc -c:v copy -c:a aac -strict experimental -f flv ' + YOUTUBE + KEY

stream_pipe = subprocess.Popen(stream_cmd, shell=True, stdin=subprocess.PIPE)
camera = picamera.PiCamera(resolution=(1280, 720), framerate=25)
try:
  now = time.strftime("%Y-%m-%d-%H:%M:%S")
  camera.framerate = 25
  camera.vflip = True
  camera.hflip = True
  camera.start_recording(stream_pipe.stdin, format='h264', bitrate = 20000000)
  while True:
     camera.wait_recording(1)
except KeyboardInterrupt:
     camera.stop_recording()
finally:
  camera.close()
  stream_pipe.stdin.close()
  stream_pipe.wait()
  print("Camera safely shut down")
  print("Good bye")
