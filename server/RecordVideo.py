import logging

class RecordVideo():
    height = 480
    width = 640
    startedRecording = False

    def setVideoResolution(self, height, width):
        self.height = height
        self.width = width

    def test(self):
        print("_________int_test____")
        return ("In test Video record ")

    def isStartedRecording(self):
        return self.startedRecording

    def getConnectedUserId(self):
        return self.userId

    def startRecording(self, filename,resolution, startedPreview, camera, userID):
        self.userId = userID
        print("_____in_start_Record____")
        if startedPreview == True and self.startedRecording == False:
            try:
                print("_________start_recording video")
                self.startedRecording = True
                filename1 = filename + ".h264"
                camera.start_recording("media/" + filename1,format='h264', splitter_port=2, resize = resolution)
                while self.startedRecording == True:
                    camera.wait_recording(1)
                print("____Executing after record")
            except Exception as e:
                logging.warning(
                    'Stop recording video', str(e))
            finally:
                print("____Block finally___")
                print("____Stopping_splitter_port")
                camera.stop_recording(splitter_port = 2)
                self.startedRecording = False

    def stopRecording(self):
        self.startedRecording = False
