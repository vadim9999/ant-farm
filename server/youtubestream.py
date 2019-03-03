import subprocess
import picamera
import time
YOUTUBE="rtmp://b.rtmp.youtube.com/live2/"
KEY= "6kbh-kq1m-zbty-e4rt"
stream_cmd = 'ffmpeg -f h264 -r 25 -f lavfi -i anullsrc -c:v copy -c:a aac -strict experimental -f flv ' + YOUTUBE + KEY

stream_pipe = subprocess.Popen(stream_cmd, shell=True, stdin=subprocess.PIPE)
camera = picamera.PiCamera(resolution=(640, 480), framerate=25)
try:
  now = time.strftime("%Y-%m-%d-%H:%M:%S")
  camera.framerate = 25
  camera.vflip = True
  camera.hflip = True
  camera.start_recording(stream.stdin, format='h264', bitrate = 2000000)
  while True:
     camera.wait_recording(1)
except KeyboardInterrupt:
     camera.stop_recording()
finally:
  camera.close()
  stream.stdin.close()
  stream.wait()
  print("Camera safely shut down")
  print("Good bye")
