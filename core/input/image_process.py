from ..common.event import EventDispatcher
from ..common.events import *
from ..engine.vector import Vector

from multiprocessing import Process, Pipe, Pool
import copy
import time
import operator
import numpy as np

def createCirclePoints(radius):
    points = list()
    points.append(np.array([0, -radius]))
    points.append(np.array([0, radius]))
    points.append(np.array([radius, 0]))
    points.append(np.array([-radius, 0]))
    #radius_sqrt_two = int(radius / 1.414)
    #points.append(np.array([radius_sqrt_two, radius_sqrt_two]))
    #points.append(np.array([radius_sqrt_two, -radius_sqrt_two]))
    #points.append(np.array([-radius_sqrt_two, radius_sqrt_two]))
    #points.append(np.array([-radius_sqrt_two, -radius_sqrt_two]))
    return points

def processYImage(y):
    outer_radius_ratio = 5.0 / 4.0
    inner_radius_ratio = 3.0 / 4.0
    lower_radius = 8
    upper_radius = 16
    threshold = 200
    steps = 1

    results = list()
    y[0][0] = 0
    while True:
        candidates = np.argwhere(y > threshold)
        if len(candidates) == 0:
            break
        candidate = candidates[0]
        candidate_y = candidate[0]
        candidate_x = candidate[1]
        radius = min(upper_radius, candidate_y, y.shape[0] - candidate_y, candidate_x, y.shape[1] - candidate_x)
        if radius < lower_radius:
            y[candidate] = 0
            continue
        is_circle = False
        for j in range(candidate_y + radius * 2, candidate_y + lower_radius * 2, -steps):
            if y[j][candidate_x] > threshold:
                is_circle = True
                radius = (j - candidate_y) / 2 + 1
                candidate_y = j - radius
                for i in range(candidate_x - radius, candidate_x, steps):
                    if y[candidate_y][i] > threshold:
                        candidate_x = i + radius
                        break
                break
        if is_circle:
            candidate = np.array([candidate_y, candidate_x])
            inner_points = createCirclePoints(int(radius * inner_radius_ratio))
            outer_points = createCirclePoints(int(radius * outer_radius_ratio))
            #sub_results = list()
            for inner_point in inner_points:
                point = candidate + inner_point
                #sub_results.append(point)
                if y[point[0]][point[1]] < threshold:
                    is_circle = False
                    break
            if not is_circle:
                continue
            for outer_point in outer_points:
                point = candidate + outer_point
                #sub_results.append(point)
                if y[point[0]][point[1]] >= threshold:
                    is_circle = False
                    break
            if not is_circle:
                continue
            results.append(candidate)
        y[candidate[0]-radius:candidate[0]+radius,candidate[1]-radius:candidate[1]+radius] = 0
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
