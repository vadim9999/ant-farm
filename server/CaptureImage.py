
class CaptureImage():
    height = 480
    width = 640

    def setImageResolution(self, height, width):
        self.height = height
        self.width = width

    def takeImage(self,filename,resolution,camera, startedRecording):
        print("CaptureImage")
        print(filename)
        if startedRecording == True:
            camera.capture('media/'+ filename + ".jpg",use_video_port=True, resize = resolution)
            print("image Captured!")
        