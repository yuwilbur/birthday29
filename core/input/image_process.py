from ..common.event import EventDispatcher
from ..common.events import *
from ..engine.vector import Vector
from ..input.image_input import ImageInput

from multiprocessing import Process, Pipe, Pool
import copy
import time
import operator
import numpy as np
import math

def processYImage(img):
    results = list()
    img_height = img.shape[0]
    img_width = img.shape[1]
    threshold = 125
    half_length = 12
    full_length = half_length * 2
    rise = 2

    def addPixel(y, x, direction, length = 1):
        results.append(ImageInput(np.array([y, x]), direction, length))
    def clearArea(top_left, bot_right):
        img[top_left[0]:bot_right[0],top_left[1]:bot_right[1]] = 0
    def getValue(top_left, bot_right):
        count = (bot_right[0] - top_left[0] + 1) * (bot_right[1] - top_left[1] + 1)
        if count == 0:
            return 0.0
        if (top_left[0] <= 0 or top_left[1] <= 0 or bot_right[0] >= img_height - 1 or bot_right[1] >= img_width - 1):
            return 0.0
        value = 0.0
        for y in range(top_left[0], bot_right[0] + 1, +1):
            for x in range(top_left[1], bot_right[1] + 1, +1):
                value += img[y][x][0]
        return value / count + 1
    def distanceSqu(x1, x2):
        y_diff = x1[0] - x2[0]
        x_diff = x1[1] - x2[1]
        return (y_diff*y_diff + x_diff*x_diff)

    angle_threshold = 1

    img[0][0][0] = 0
    while True:
        candidates = np.argwhere(img >= threshold)
        if len(candidates) == 0:
            break
        candidate = candidates[0]
        cy = candidate[0]
        cx = candidate[1]
        img[cy][cx][0] = 0
        # Stop processing if the newest value is at the bottom.
        if (cy > img_height - half_length):
            break

        min_x = max(cx - full_length, 0)
        max_x = min(cx + full_length, img_width - 1)
        max_y = min(cy + full_length, img_height - 1)

        x = cx
        for y in range(cy + 1, max_y + 1, +1):
            if img[y][x][0] < threshold:
                y -= 1
                break
            for x in range(x, max_x + 1, +1):
                if img[y][x][0] < threshold:
                    x -= 1
                    break
        right = [y - cy, x - cx]

        x = cx
        for y in range(cy + 1, max_y + 1, +1):
            if img[y][x][0] < threshold:
                y -= 1
                break
            for x in range(x, min_x - 1, -1):
                if img[y][x][0] < threshold:
                    x += 1
                    break
        left = [y - cy, x - cx]

        dot = right[0] * left[0] + right[1] * left[1]
        det = right[1] * left[0] - right[0] * left[1]
        angle = math.atan2(det, dot)

        length = int((right[1] - left[1]) * 1.2)

        if (length < half_length or length > full_length):
            clearArea([cy, x - length / 2],[cy + length, x + length / 2])
            continue

        if (angle > angle_threshold):
            y = cy + (right[0] + left[0]) / 2 + 1
            x = cx + (right[1] + left[1]) / 2 + 1
        else:
            y = cy + (right[0] + left[0]) / 4 + 1
            x = cx + (right[1] + left[1]) / 2 + 1

        if (y <= half_length or y >= img_height - half_length or x <= half_length or x <= img_width - half_length):
            continue

        value = img[y][x][0]
        value_threshold = threshold / 2
        for diff in range(0, half_length):
            if (y - diff > 0):
                if abs(value - int(img[y - diff][x][0])) > value_threshold:
                    y = y - diff
                    break
            if (x - diff > 0):
                if abs(value - int(img[y][x - diff][0])) > value_threshold:
                    x = x - diff
                    break
            if (x + diff < img_width):
                if abs(value - int(img[y][x + diff][0])) > value_threshold:
                    x = x + diff
                    break

        if diff == half_length - 1:
            continue

        diff = 2
        top = getValue([y - diff, x - 1], [y - diff, x + 1])
        bottom = getValue([y + diff, x - 1], [y + diff, x + 1])
        left = getValue([y - 1, x - diff], [y + 1, x - diff])
        right = getValue([y - 1, x + diff], [y + 1, x + diff])
        min_value = min(top, bottom, left, right)
        key_direction = None
        if min_value < threshold and min_value > 0.0:
            if (top == min_value):
                key_direction = Key.UP
            elif (bottom == min_value):
                key_direction = Key.DOWN
            elif (left == min_value):
                key_direction = Key.LEFT
            elif (right == min_value):
                key_direction = Key.RIGHT
        if not (key_direction == None):
            addPixel(y, x, key_direction, length)
        clearArea([y - length / 2, x - length / 2],[y + length / 2, x + length / 2])
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
