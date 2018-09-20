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
    def clearArea(top_left, bot_right):
        img[top_left[0]:bot_right[0],top_left[1]:bot_right[1]] = 0
        # for y in range(top_left[0], bot_right[0]):
        #     for x in range(top_left[1], bot_right[1]):
        #         results.append(ImageInput(np.array([y, x]), 0))
    def getValue(top_left, bot_right):
        count = (bot_right[0] - top_left[0] + 1) * (bot_right[1] - top_left[1] + 1)
        if count == 0:
            return 0.0
        value = 0.0
        for y in range(top_left[0], bot_right[0] + 1):
            for x in range(top_left[1], bot_right[1] + 1):
                value += img[y][x][0]
        return value / count
    img_height = img.shape[0]
    img_width = img.shape[1]
    threshold = 125
    half_length = 8
    full_length = half_length * 2
    rise = half_length / 2.0

    img[0][0] = 0
    while True:
        candidates = np.argwhere(img >= threshold)
        if len(candidates) == 0:
            break
        candidate = candidates[0]
        cy = candidate[0]
        cx = candidate[1]
        img[cy][cx] = 0
        if min(cx, cy) <= half_length or max(cx, cy) >= img_height - half_length:
            continue
        if img[cy + rise][cx] < threshold:
            continue

        left_slope = 0
        x = cx
        for y in range(cy + 1, cy + int(rise), +1):
            for x in range(x, cx + half_length, +1):
                if (img[y][x] < threshold):
                    break
        left_slope = (x - cx - 1) / rise
        if left_slope == 0:
            clearArea([cy, cx - half_length],[cy + full_length, cx + half_length])
            continue

        right_slope = 0
        x = cx
        for y in range(cy + 1, cy + int(rise), +1):
            for x in range(x, cx - half_length, -1):
                if (img[y][x] < threshold):
                    break
        right_slope = (x - cx - 1) / rise
        if right_slope == 0:
            clearArea([cy, cx - half_length],[cy + full_length, cx + half_length])
            continue

        mid_y = cy
        bot_y = cy
        slope = (right_slope + left_slope) / 2.0
        for y in range(cy + 1, cy + full_length, +1):
            x = cx + int(slope * (y - cy))
            if (mid_y == cy):
                if (img[y][x] < threshold):
                    mid_y = y - 1
            else:
                if (img[y][x] >= threshold):
                    bot_y = y - 1
                    break
        if bot_y == cy:
            clearArea([cy, cx - half_length],[cy + full_length, cx + half_length])
            continue

        diff_y = (bot_y - mid_y) - (mid_y - cy)
        if (diff_y * diff_y) > 2*2:
            y = mid_y
        else:
            y = bot_y
        
        length = int((y - cy) * 1.25)
        cy = y
        cx = x

        top = getValue([cy - 2, cx - 1], [cy - 2, cx + 1])
        bottom = getValue([cy + 2, cx - 1], [cy + 2, cx + 1])
        left = getValue([cy - 1, cx - 2], [cy + 1, cx - 2])
        right = getValue([cy - 1, cx + 2], [cy + 1, cx + 2])
        max_value = max(top, bottom, left, right)
        if (top == max_value):
            key_direction = Key.DOWN
        elif (bottom == max_value):
            key_direction = Key.UP
        elif (left == max_value):
            key_direction = Key.RIGHT
        elif (right == max_value):
            key_direction = Key.LEFT
        else:
            break

        results.append(ImageInput(np.array([cy, cx]), key_direction))
        clearArea([cy - length, cx - length],[cy + length, cx + length])
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
