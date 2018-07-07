from camera import Camera
from event import Event
from events import DrawEvent
from events import YImageEvent
import time
import copy
import numpy

class CameraProcess:
    def __init__(self, event_dispatcher):
        self._event_dispatcher = event_dispatcher
        self._resolution = Camera.RESOLUTION_LO
        self._camera = Camera(self._resolution)
        self._raw = self._camera.createEmptyFullData()
        self._grayscale = self._camera.createEmptyFullData()
        self._y = self._camera.createEmptyYData()

    def update(self):
        self._camera.capture(self._raw)
    
        Camera.rawToY(self._raw, self._y)
        y_data = (self._y, self._resolution)
        self._event_dispatcher.dispatch_event(Event(YImageEvent.TYPE, copy.deepcopy(y_data)))
        
        Camera.rawToGrayscale(self._raw, self._grayscale)
        grayscale_data = (copy.deepcopy(self._grayscale), (0,0), self._resolution)
        self._event_dispatcher.dispatch_event(Event(DrawEvent.TYPE, grayscale_data))
