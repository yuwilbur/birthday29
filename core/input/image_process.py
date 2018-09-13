from ..common.event import EventDispatcher
from ..common.events import *
from ..engine.vector import Vector
from ..input.image_input import ImageInput

from multiprocessing import Process, Pipe, Pool
import copy
import time
import operator
import numpy as np

def processYImage(y):
    def clearRegion(y, top_left, bot_right):
        y[top_left[0]:bot_right[0],top_left[1]:bot_right[1]] = 0
    threshold = 150
    outer_radius_ratio = 5.0 / 4.0
    inner_radius_ratio = 3.0 / 4.0
    step = 4
    min_thickness = 3
    max_thickness = 6
    max_length = 24

    results = list()
    y[0][0] = 0
    while True:
        candidates = np.argwhere(y >= threshold)
        if len(candidates) == 0:
            break
        candidate = candidates[0]
        cy = candidate[0]
        cx = candidate[1]

        thickness1 = 0
        thickness2 = 0
        for top_y in range(cy, cy + max_length):
            if (y[top_y][cx] < threshold):
                thickness1 = top_y - cy
                break
        if thickness1 > max_thickness:
            results.append(ImageInput(np.array([top_y, cx]), 0))
            clearRegion(y, np.array([cy,cx - max_length / 2]), np.array([cy + max_length, cx + max_length / 2]))
            continue

        for center_y in range(top_y, top_y + max_thickness):
            if (y[center_y][cx] >= threshold):
                thickness2 = center_y - top_y
                break
        results.append(ImageInput(np.array([center_y, cx]), 0))
        break


        # for center_y in range(top_y, top_y + max_length):
        #     if (y[center_y][cx] >= threshold):
        #         thickness2 = center_y - top_y
        #         break
        # center_y = cy + min(thickness1, thickness2) * 2
        # if (y[center_y][cx] >= threshold):
        #     pass
        # else:
        #     pass
        # results.append(ImageInput(np.array([center_y, cx]), 0))
    return results

def yImageWorker(pipe):
    main_conn, worker_conn = pipe
    while True:
        data = worker_conn.recv()
        if data == ImageProcess.END_MESSAGE:
           break;
        result = processYImage(data.data)
        worker_conn.send((data.timestamp, result))

class ImageProcess(object):
    END_MESSAGE = 'END'
    def __init__(self):
        EventDispatcher().add_event_listener(YImageEvent.TYPE, self.onYImageEvent)

        self._main1_conn, self._worker1_conn = Pipe()
        self._worker1_ready = True
        self._worker1 = Process(target=yImageWorker, args=((self._main1_conn, self._worker1_conn),))
        self._worker1.daemon = True
        self._worker1.start()

        self._main2_conn, self._worker2_conn = Pipe()
        self._worker2_ready = True
        self._worker2 = Process(target=yImageWorker, args=((self._main2_conn, self._worker2_conn),))
        self._worker2.daemon = True
        self._worker2.start()

    def onYImageEvent(self, event):
        if self._worker1_ready:
            self._worker1_ready = False
            self._main1_conn.send(event.data()[0])
        if self._worker2_ready:
            self._worker2_ready = False
            self._main2_conn.send(event.data()[1])

    def stop(self):
        self._main1_conn.send(ImageProcess.END_MESSAGE)
        while self._main1_conn.poll():
           self._main1_conn.recv()
        self._main2_conn.send(ImageProcess.END_MESSAGE)
        while self._main2_conn.poll():
           self._main2_conn.recv()
        self._worker1.join()
        self._worker2.join()

    def update(self):
        if self._main1_conn.poll():
            data = self._main1_conn.recv()
            self._worker1_ready = True
            EventDispatcher().dispatch_event(LatencyEvent(LatencyEvent.P1_PROCESSING, data[0]))
            EventDispatcher().dispatch_event(CameraResultEvent(CameraResultEvent.P1, data[1]))
        if self._main2_conn.poll():
            data = self._main2_conn.recv()
            self._worker2_ready = True
            EventDispatcher().dispatch_event(LatencyEvent(LatencyEvent.P2_PROCESSING, data[0]))
            EventDispatcher().dispatch_event(CameraResultEvent(CameraResultEvent.P2, data[1]))
