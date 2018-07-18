from ..common.event import Event
from ..common.events import RGBImageEvent
from ..common.events import YImageEvent
from ..common.events import TestEvent
from ..common.events import GrayscaleImageEvent
from ..input.camera import Camera

from multiprocessing import Process, Pipe
import time
import copy
import numpy as np

def cameraWorker(pipe, resolution):
    main_conn, worker_conn = pipe
    camera = Camera(resolution)
    mono_resolution = (resolution[0] / 2, resolution[1])
    y_mono = Camera.createImage(resolution, 1)
    y_stereo = (Camera.createImage(mono_resolution, 1), Camera.createImage(mono_resolution, 1))
    grayscale_mono = Camera.createImage(resolution, 3)
    grayscale_stereo = (Camera.createImage(mono_resolution, 3), Camera.createImage(mono_resolution, 3))
    getGrayscale = False
    getY = False
    getFullGrayscale = True
    while True:
        y_mono = camera.capture()
        if worker_conn.poll():
            data = worker_conn.recv()
            if data == CameraProcess.END_MESSAGE:
                worker_conn.send(data)
                break;
        elif not main_conn.poll():
            Camera.monoToStereo(y_mono, y_stereo)
            if getGrayscale:
                Camera.rawToGrayscale(raw_split[0], grayscale[0])
                Camera.rawToGrayscale(raw_split[1], grayscale[1])
                worker_conn.send((CameraProcess.RGB_MESSAGE, grayscale))
            if getY:
                Camera.rawToY(raw_split[0], y[0])
                Camera.rawToY(raw_split[1], y[1])
                worker_conn.send((CameraProcess.Y_MESSAGE, y))
            if getFullGrayscale:
                Camera.yToGrayscale(y_mono, grayscale_mono)
                worker_conn.send((CameraProcess.FULL_MESSAGE, grayscale_mono))

class CameraProcess(object):
    END_MESSAGE = 'END'
    Y_MESSAGE = 'Y'
    RGB_MESSAGE = 'RGB'
    FULL_MESSAGE = 'FULL'
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
            #self._event_dispatcher.dispatch_event(Event(YImageEvent.TYPE, (datay, data[1].resolution)))
            pass
        elif data[0] == self.RGB_MESSAGE:
            width, height, channels = data[1][0].shape
            self._event_dispatcher.dispatch_event(GrayscaleImageEvent((data[1][0], (width, height))))
            pass
        elif data[0] == self.FULL_MESSAGE:
            width, height, channels = data[1].shape
            self._event_dispatcher.dispatch_event(TestEvent((data[1], (width, height))))
            pass
