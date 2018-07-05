from camera import Camera
import time

class CameraProcess:
    def __init__(self, event_dispatcher):
        self.event_dispatcher = event_dispatcher
        self.camera = Camera(Camera.RESOLUTION_LO)
        self.rawData = self.camera.createEmptyRawData()
        # self.processedData = self.camera.createEmptyRawData()

    def update(self):
        #start_time = time.time()
        self.camera.capture(self.rawData)
        #print "camera: " + str(time.time() - start_time)
        
