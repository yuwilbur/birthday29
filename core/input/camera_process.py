from ..common.event import EventDispatcher
from ..common.events import *
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
    y_mono = Frame(resolution)
    y_stereo = [Frame(mono_resolution), Frame(mono_resolution)]
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
            worker_conn.send(y_stereo)

class CameraProcess(object):
    END_MESSAGE = 'END'
    def __init__(self):
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
        self._y_stereo = data
        EventDispatcher().dispatch_event(YImageEvent(self._y_stereo))
