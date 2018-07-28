from ..common.event import EventDispatcher
from ..common.events import *

from multiprocessing import Process, Pipe, Pool
import copy
import time
import numpy as np
    
def processYImage(y):
    threshold = 200
    diameter = 12
    circle_points = list()
    circle_points.append((0, 0))
    circle_points.append((diameter, 0))
    circle_points.append((diameter / 2, -diameter / 2))
    circle_points.append((diameter / 2, diameter / 2))
    candidates = np.argwhere(y >= threshold)
    results = list()
    for candidate in candidates:
        is_circle = True
        sub_results = list()
        for circle_point in circle_points:
            point = (candidate[0] + circle_point[0], candidate[1] + circle_point[1])
            sub_results.append(point)
            if y[point[0]][point[1]] < threshold:
                is_circle = False
                break
        if is_circle:
            results.extend(sub_results)
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
