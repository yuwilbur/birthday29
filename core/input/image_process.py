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
    radius_sqrt_two = int(radius / 1.414)
    points.append(np.array([radius_sqrt_two, radius_sqrt_two]))
    points.append(np.array([radius_sqrt_two, -radius_sqrt_two]))
    points.append(np.array([-radius_sqrt_two, radius_sqrt_two]))
    points.append(np.array([-radius_sqrt_two, -radius_sqrt_two]))
    return points

def processYImage(y):
    radius_per_width_ratio = 2
    detection_ratio = 3.0 / 4.0
    lower_radius = 8
    upper_radius = 16
    threshold = 200

    results = list()
    y[0][0] = 0
    while True:
        candidate = np.argmax(y > threshold)
        if candidate == 0:
            break
        candidate = np.unravel_index(candidate, y.shape)
        candidate_y = candidate[0]
        candidate_x = candidate[1]
        radius = min(upper_radius, candidate_y, y.shape[0] - candidate_y, candidate_x, y.shape[1] - candidate_x)
        if radius < lower_radius:
            y[candidate] = 0
            continue
        width = radius / radius_per_width_ratio
        is_potentially_circle = False
        for j in range(candidate_y, candidate_y + width):
            if y[j][candidate_x] <= threshold:
                is_potentially_circle = True
                width = j - candidate_y
                radius = int((width * radius_per_width_ratio) * detection_ratio)
                candidate_y = candidate_y + radius
                for i in range(candidate_x - radius, candidate_x):
                    if y[candidate_y][i] > threshold:
                        candidate_x = i + radius
                        break
                break
        candidate = np.array([candidate_y, candidate_x])
        if is_potentially_circle:
            circle_points = createCirclePoints(radius)
            is_circle = True
            sub_results = list()
            for circle_point in circle_points:
                point = candidate + circle_point
                sub_results.append(point)
                if y[point[0]][point[1]] < threshold:
                    is_circle = False
                    break
            if is_circle:
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
