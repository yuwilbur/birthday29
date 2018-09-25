from ..common.event import EventDispatcher
from ..common.events import *
from ..engine.vector import Vector
from ..input.image_input import ImageInput

from multiprocessing import Process, Pipe, Pool
import copy
import time
import operator
import numpy as np

def processYImage(img):
    results = list()
    img_height = img.shape[0]
    img_width = img.shape[1]
    threshold = 200
    half_length = 12
    full_length = half_length * 2
    rise = 2

    def addPixel(y, x, direction, length = 0):
        results.append(ImageInput(np.array([y, x]), direction, length))
    def clearArea(top_left, bot_right):
        img[top_left[0]:bot_right[0],top_left[1]:bot_right[1]] = 0
    def getValue(top_left, bot_right):
        count = (bot_right[0] - top_left[0] + 1) * (bot_right[1] - top_left[1] + 1)
        if count == 0:
            return 0.0
        if (top_left[0] == 0 or top_left[1] == 0 or bot_right[0] == img_height - 1 or bot_right[1] == img_width - 1):
            return 0.0
        value = 0.0
        for y in range(top_left[0], bot_right[0] + 1, +1):
            for x in range(top_left[1], bot_right[1] + 1, +1):
                value += img[y][x][0]
        return value / count

    img[0][0] = 0
    while True:
        candidates = np.argwhere(img >= threshold)
        if len(candidates) == 0:
            break
        candidate = candidates[0]
        cy = candidate[0]
        cx = candidate[1]
        img[cy][cx] = 0
        # Stop processing if the newest value is at the bottom.
        if (cy > img_height - half_length):
            break

        y_limit = min(cy + rise, img_height - 1)
        for y in range(cy + 1, cy + rise + 1, +1):
            if (img[y][cx] < threshold):
                break
        if not (y == y_limit):
            continue

        x_limit = min(cx + full_length, img_width - 1)
        for x in range(cx, x_limit + 1, +1):
            if (img[y][x] < threshold):
                break
        x_right = x

        x_limit = max(cx - full_length, 0)
        for x in range(cx, x_limit - 1, -1):
            if (img[y][x] < threshold):
                break
        x_left = x

        x_center = (x_left + x_right) / 2

        x_diff = x_center - cx
        x_threshold = half_length / 4
        if (x_right == img_width - 1 or x_left == 0):
            length = x_right - x_left
        else:
            length = int((x_right - x_left) * 1.2 / 2.0)
        
        x = x_center
        y = (x_right - x_left) / 2 + cy

        if (length < half_length or length > full_length):
            clearArea([cy, x_center - length],[cy + length * 2, x_center + length])
            continue

        diff = max(length / 4, 2)
        top = getValue([y - diff, x - 1], [y - diff, x + 1])
        bottom = getValue([y + diff, x - 1], [y + diff, x + 1])
        left = getValue([y - 1, x - diff], [y + 1, x - diff])
        right = getValue([y - 1, x + diff], [y + 1, x + diff])
        max_value = max(top, bottom, left, right)
        key_direction = None
        if max_value > threshold:
            if (top == max_value):
                key_direction = Key.DOWN
            elif (bottom == max_value):
                key_direction = Key.UP
            elif (left == max_value):
                key_direction = Key.RIGHT
            elif (right == max_value):
                key_direction = Key.LEFT
        if not (key_direction == None):
            addPixel(y, x, key_direction, length)
        clearArea([cy, x_center - length],[cy + length * 2, x_center + length])
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
