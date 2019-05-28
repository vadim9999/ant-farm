import logging

class RecordVideo():
    height = 480
    width = 640
    startedRecording = False

    def setVideoResolution(self, height, width):
        self.height = height
        self.width = width

    def isStartedRecording(self):
        return self.startedRecording

    def getConnectedUserId(self):
        return self.userId

    def startRecording(self, filename,resolution, startedPreview, camera, userID):
        self.userId = userID
        if startedPreview == True and self.startedRecording == False:
            try:
                self.startedRecording = True
                filename1 = filename + ".h264"
                camera.start_recording("media/" + filename1,format='h264', splitter_port=2, resize = resolution)
                while self.startedRecording == True:
                    camera.wait_recording(1)
            except Exception as e:
                print("Stor record")
            finally:
                camera.stop_recording(splitter_port = 2)
                self.startedRecording = False

    def stopRecording(self):
        self.startedRecording = False
