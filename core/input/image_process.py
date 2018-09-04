from ..common.event import EventDispatcher
from ..common.events import *
from ..engine.vector import Vector
from ..input.image_input import ImageInput

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
    def clearRegion(y, top_left, bot_right):
        y[top_left[0]:bot_right[0],top_left[1]:bot_right[1]] = 0
    threshold = 150
    outer_radius_ratio = 5.0 / 4.0
    inner_radius_ratio = 3.0 / 4.0
    step = 4
    max_length = 16
    min_length = 8

    results = list()
    y[0][0] = 0
    while True:
        candidates = np.argwhere(y >= threshold)
        if len(candidates) == 0:
            break
        candidate = candidates[0]
        cy = candidate[0]
        cx = candidate[1]
        if (y[cy+1][cx] < threshold):
            y[cy][cx] = 0
            continue
        # Determine the center of the target.
        c_top = np.array([cy,cx])
        c_left = np.array([cy,cx])
        for c_left[1] in range(c_left[1] - 1, max(0, c_left[1] - max_length), -1):
            if y[c_left[0]][c_left[1]] >= threshold:
                continue
            last_point = True
            y_start = c_left[0]
            for c_left[0] in range(c_left[0] + 1, min(y.shape[1], c_left[0] + step), 1):
                if y[c_left[0]][c_left[1]] >= threshold:
                    last_point = False
                    break
            if last_point:
                c_left[0] = (c_left[0] + y_start) / 2
                c_left[1] += 1
                break
        c_right = np.array([cy,cx])
        for c_right[1] in range(c_right[1] + 1, max(y.shape[0], c_right[1] + max_length), 1):
            if y[c_right[0]][c_right[1]] >= threshold:
                continue
            last_point = True
            y_start = c_right[0]
            for c_right[0] in range(c_right[0] + 1, min(y.shape[1], c_right[0] + step), 1):
                if y[c_right[0]][c_right[1]] >= threshold:
                    last_point = False
                    break
            if last_point:
                c_right[0] = (c_right[0] + y_start) / 2
                c_right[1] -= 1
                break
        c_center = (c_left + c_right) / 2

        # Determine the direction of the target.
        c_top = c_center + (c_top - c_center) / 3
        c_left2 = c_center + (c_left - c_center) / 3
        c_right2 = c_center + (c_right - c_center) / 3
        results.append(ImageInput(candidate, 0))
        results.append(ImageInput(c_top, 0))
        results.append(ImageInput(c_left, 0))
        results.append(ImageInput(c_left2, 0))
        results.append(ImageInput(c_right, 0))
        results.append(ImageInput(c_right2, 0))
        results.append(ImageInput(c_center, 0))
        #results.append(ImageInput(np.array([cy + int(step), int(step / slope_right + cx)]), 0))
        #results.append(ImageInput(np.array([cy + int(test), int(test / slope + cx)]), 0))
        y[cy][cx] = 0
        break
        # if candidate_y + upper_radius * 2 >= y.shape[0] or candidate_x + upper_radius >= y.shape[1] or candidate_x - upper_radius < 0:
        #     y[candidate] = 0
        #     continue
        # is_target = False
        # radius = 1
        # for j in range(candidate_y + upper_radius * 2, candidate_y + lower_radius * 2, -1):
        #     #print j
        #     if y[j][candidate_x] > threshold:
        #         is_target = True
        #         radius = (j - candidate_y) / 2 + 1
        #         candidate_y = j - radius
        #         for i in range(candidate_x - radius, candidate_x, 1):
        #             if y[candidate_y][i] > threshold:
        #                 candidate_x = i + radius
        #                 break
        #         break
        # if is_target:
        #     candidate = np.array([candidate_y, candidate_x])
        #     inner_points = createCirclePoints(int(radius * inner_radius_ratio))
        #     outer_points = createCirclePoints(int(radius * outer_radius_ratio))
        #     #sub_results = list()
        #     for inner_point in inner_points:
        #         point = candidate + inner_point
        #         #sub_results.append(point)
        #         if y[point[0]][point[1]] < threshold:
        #             is_target = False
        #             break
        #     if not is_target:
        #         continue
        #     for outer_point in outer_points:
        #         point = candidate + outer_point
        #         #sub_results.append(point)
        #         if y[point[0]][point[1]] >= threshold:
        #             is_target = False
        #             break
        #     if not is_target:
        #         continue
        #     results.append(ImageInput(candidate, 0))
        # y[candidate[0]-radius:candidate[0]+radius,candidate[1]-radius:candidate[1]+radius] = 0
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
