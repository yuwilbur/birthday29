from ..common.event import Event
from ..common.events import RGBImageEvent
from ..common.events import YImageEvent
from ..input.camera import Image
from ..input.camera import Camera

from multiprocessing import Process, Pipe
import time
import copy
import numpy as np

def cameraWorker(pipe, resolution):
    main_conn, worker_conn = pipe
    camera = Camera(resolution)
    raw = Image(resolution, 3)
    grayscale = Image(resolution, 3)
    y = Image(resolution, 1)
    getGrayscale = True
    getY = True
    while True:
        raw.data = camera.capture()
        if worker_conn.poll():
            data = worker_conn.recv()
            if data == CameraProcess.END_MESSAGE:
                worker_conn.send(data)
                break;
        elif not main_conn.poll():
            if getGrayscale:
                Camera.rawToGrayscale(raw, grayscale)
                worker_conn.send((CameraProcess.RGB_MESSAGE, grayscale))
            if getY:
                Camera.rawToY(raw, y)
                worker_conn.send((CameraProcess.Y_MESSAGE, y))

class CameraProcess(object):
    END_MESSAGE = 'END'
    Y_MESSAGE = 'Y'
    RGB_MESSAGE = 'RGB'
    def __init__(self, event_dispatcher):
        self._event_dispatcher = event_dispatcher
        self._resolution = Camera.RESOLUTION_LO
        self._main_conn, self._worker_conn = Pipe()

        self._worker = Process(target=cameraWorker, args=((self._main_conn, self._worker_conn),self._resolution,))
        self._worker.daemon = True
        self._worker.start()

    def stop(self):
        self._main_conn.send(CameraProcess.END_MESSAGE)
        while True:
            if self._main_conn.poll(0.1):
                if self._main_conn.recv() == CameraProcess.END_MESSAGE:
                    break
            self._main_conn.send(CameraProcess.END_MESSAGE)
        self._worker.join()

    def update(self):
        if not self._main_conn.poll():
            return
        data = self._main_conn.recv()

        if data[0] == self.Y_MESSAGE:
            self._event_dispatcher.dispatch_event(Event(YImageEvent.TYPE, (data[1].data, data[1].resolution)))
        elif data[0] == self.RGB_MESSAGE:
            self._event_dispatcher.dispatch_event(Event(RGBImageEvent.TYPE, (data[1].data, data[1].resolution)))
