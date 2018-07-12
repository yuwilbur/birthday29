from ..common.event import Event
from ..common.events import DrawEvent
from ..common.events import YImageEvent
from ..input.camera import Camera

from multiprocessing import Process, Pipe
import time
import copy

def cameraWorker(pipe, resolution):
    main_conn, worker_conn = pipe
    camera = Camera(resolution)
    raw = camera.createEmptyFullData(resolution)
    while True:
        if worker_conn.poll():
            data = worker_conn.recv()
            if data == CameraProcess.END_MESSAGE:
                break;
        raw = camera.capture()
        if not main_conn.poll():
            worker_conn.send(raw)


class CameraProcess:
    END_MESSAGE = 'END'
    def __init__(self, event_dispatcher):
        self._event_dispatcher = event_dispatcher
        self._resolution = Camera.RESOLUTION_LO
        self._main_conn, self._worker_conn = Pipe()
        self._processor = Process(target=cameraWorker, args=((self._main_conn, self._worker_conn),self._resolution,))
        self._processor.daemon = True
        self._processor.start()
        self._raw = Camera.createEmptyFullData(self._resolution)
        self._grayscale = Camera.createEmptyFullData(self._resolution)
        self._y = Camera.createEmptyYData(self._resolution)

    def stop(self):
        self._main_conn.send(CameraProcess.END_MESSAGE)
        self._processor.join()

    def update(self):
        if not self._main_conn.poll():
            return

        self._raw = self._main_conn.recv()
    
        Camera.rawToY(self._raw, self._y)
        y_data = (self._y, self._resolution)
        self._event_dispatcher.dispatch_event(Event(YImageEvent.TYPE, copy.deepcopy(y_data)))
        
        Camera.rawToGrayscale(self._raw, self._grayscale)
        grayscale_data = (copy.deepcopy(self._grayscale), (0,0), self._resolution)
        self._event_dispatcher.dispatch_event(Event(DrawEvent.TYPE, grayscale_data))
