from camera import Camera
from drawEvent import DrawEvent
from event import Event
import time
import copy

class CameraProcess:
    def __init__(self, event_dispatcher):
        self.event_dispatcher = event_dispatcher
        self.camera = Camera(Camera.RESOLUTION_LO)
        self.rawData = self.camera.createEmptyRawData()
        self.processedData = self.camera.createEmptyRawData()

    def update(self):
        self.camera.capture(self.rawData)
        Camera.rawToGrayscale(self.rawData, self.processedData)
        self.event_dispatcher.dispatch_event(Event(DrawEvent.TYPE, copy.deepcopy(self.processedData)))
        
