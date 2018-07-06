from camera import Camera
from drawEvent import DrawEvent
from event import Event
import time
import copy

class CameraProcess:
    def __init__(self, event_dispatcher):
        self._event_dispatcher = event_dispatcher
        self._resolution = Camera.RESOLUTION_LO
        self._camera = Camera(self._resolution)
        self._rawData = self._camera.createEmptyRawData()
        self._processedData = self._camera.createEmptyRawData()

    def update(self):
        self._camera.capture(self._rawData)
        Camera.rawToGrayscale(self._rawData, self._processedData)
        data = (copy.deepcopy(self._processedData), self._resolution)
        self._event_dispatcher.dispatch_event(Event(DrawEvent.TYPE, data))
        
