from ..common.event import Event
from ..common.events import RGBImageEvent
from ..common.events import YImageEvent
from ..input.camera import Camera

from multiprocessing import Process, Pipe
import time
import copy

def cameraWorker(pipe, resolution):
    main_conn, worker_conn = pipe
    camera = Camera(resolution)
    raw = camera.createEmptyFullData(resolution)
    y = camera.createEmptyYData(resolution)
    grayscale = camera.createEmptyFullData(resolution)
    while True:
        raw = camera.capture()
        Camera.rawToY(raw, y)
        Camera.rawToGrayscale(raw, grayscale)
        if worker_conn.poll():
            data = worker_conn.recv()
            if data == CameraProcess.END_MESSAGE:
                break;
        elif not main_conn.poll():
            worker_conn.send((y, grayscale))

class CameraProcess(object):
    END_MESSAGE = 'END'
    def __init__(self, event_dispatcher):
        self._event_dispatcher = event_dispatcher
        self._resolution = Camera.RESOLUTION_LO
        self._main_conn, self._worker_conn = Pipe()

        self._worker = Process(target=cameraWorker, args=((self._main_conn, self._worker_conn),self._resolution,))
        self._worker.daemon = True
        self._worker.start()

    def stop(self):
        self._main_conn.send(CameraProcess.END_MESSAGE)
        while self._main_conn.poll():
            self._main_conn.recv()
        self._worker.join()

    def update(self):
        if not self._main_conn.poll():
            return
        data = self._main_conn.recv()
    
        self._event_dispatcher.dispatch_event(Event(YImageEvent.TYPE, (data[0], self._resolution)))
        self._event_dispatcher.dispatch_event(Event(RGBImageEvent.TYPE, (data[1], self._resolution)))
