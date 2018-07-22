from ..common.events import YImageEvent
from ..common.events import TestEvent
from ..common.events import GrayscaleImageEvent
from ..input.camera import Camera
from ..input.frame import Frame

from multiprocessing import Process, Pipe
import time
import copy
import numpy as np
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def cameraWorker(pipe, resolution):
    main_conn, worker_conn = pipe
    camera = Camera(resolution)
    mono_resolution = (resolution[0] / 2, resolution[1])
    y_mono = Frame(resolution, 1)
    y_stereo = [Frame(mono_resolution, 1), Frame(mono_resolution, 1)]
    grayscale_stereo = [Frame(mono_resolution, 3), Frame(mono_resolution, 3)]
    worker_conn.send((CameraProcess.INIT_MESSAGE, (y_stereo, grayscale_stereo)))
    while True:
        y_mono.data = camera.capture()
        y_mono.timestamp = time.time()
        if worker_conn.poll():
            data = worker_conn.recv()
            if data == CameraProcess.END_MESSAGE:
                worker_conn.send(data)
                break;
        elif not main_conn.poll():
            y_mono.split(y_stereo[0], y_stereo[1])
            worker_conn.send((CameraProcess.NORMAL_MESSAGE, y_stereo))

class CameraProcess(object):
    END_MESSAGE = 'END'
    INIT_MESSAGE = 'INIT'
    NORMAL_MESSAGE = 'NORMAL'
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
        if data[0] == CameraProcess.INIT_MESSAGE:
            self._y_stereo = data[1][0]
            self._grayscale_stereo = data[1][1]
        elif data[0] == CameraProcess.NORMAL_MESSAGE:
            self._y_stereo = data[1]
            self._y_stereo[0].scale(self._grayscale_stereo[0], 3)
            self._y_stereo[1].scale(self._grayscale_stereo[1], 3)
            self._event_dispatcher.dispatch_event(GrayscaleImageEvent(self._grayscale_stereo))
            self._event_dispatcher.dispatch_event(YImageEvent(self._y_stereo))
