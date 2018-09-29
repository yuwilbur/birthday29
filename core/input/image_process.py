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
import time

def processYImage(img):
    results = list()
    img_height = img.shape[0]
    img_width = img.shape[1]
    threshold = 150
    min_length = 12

    def isWithinBounds(position):
        return position.x >= 0 and position.x < img_width and position.y >= 0 and position.y < img_height
    def addPixel(pixel, size = Vector(1,1), direction = Key.DEBUG):
        results.append(ImageInput(pixel, direction, size))
    def clearArea(center, size):
        img[center.y - size.y / 2: center.y + size.y / 2, center.x - size.x / 2:center.x + size.x / 2] = 0
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
    def useWilburContour(start):
        start_time = time.time()
        cy = start.y
        cx = start.x
        min_x = 0
        max_x = img_width - 1
        min_y = cy
        max_y = img_height - 1

        # Find bottom right corner.
        x = cx
        for y in range(cy + 1, max_y + 1, +1):
            if img[y][x][0] < threshold:
                y -= 1
                break
            for x in range(x, max_x + 1, +1):
                if img[y][x][0] < threshold:
                    if (x > min_x):
                        x -= 1
                    break
        if (x > min_x):
            x -= 1
        for y in range(y, max_y + 1, +1):
            if img[y][x][0] < threshold:
                y -= 1
                break
        right = Vector(x - cx, y - cy)

        # Find top left corner.
        x = cx
        for y in range(cy + 1, max_y + 1, +1):
            if img[y][x][0] < threshold:
                y -= 1
                break
            for x in range(x, min_x - 1, -1):
                if img[y][x][0] < threshold:
                    if (x < max_x):
                        x += 1
                    break
        if (x < max_x):
            x += 1
        for y in range(y, min_y - 1, -1):
            if img[y][x][0] < threshold:
                y += 1
                break
        left = Vector(x - cx, y - cy)

        # Crudely calculate the length.
        center = start + (left+right) / 2
        length = math.sqrt(Vector.DistanceSqu(left, right) * 2.0)
        if center.x - length / 2 < 0:
            length = center.x * 2
        if center.x + length / 2 > img_width - 1:
            length = ((img_width - 1) - center.x) * 2
        if center.y - length / 2 < 0:
            length = center.y * 2
        if center.y + length / 2 > img_height - 1:
            length = ((img_height - 1) - center.y) * 2
        length = int(length)
        print 'wilbur', time.time() - start_time
        return (center, Vector(length, length))
    def useSquareTracing(start):
        start_time = time.time()
        up = 'up'
        right = 'right'
        down = 'down'
        left = 'left'
        delta = {
            up : Vector(0, -1),
            down : Vector(0, 1),
            left : Vector(-1, 0),
            right : Vector(1, 0)
        }
        turn_left = {
            up : left,
            down : right,
            left : down,
            right : up
        }
        turn_right = {
            up : right,
            down : left,
            left : up,
            right : down
        }
        direction = right
        position = start
        position += delta[direction]
        if not isWithinBounds(position):
            return (Vector(), Vector())
        while(not position == start):
            if (img[position.y][position.x][0] >= threshold):
                direction = turn_left[direction]
            else:
                direction = turn_right[direction]
            position += delta[direction]
            while(not isWithinBounds(position)):
                position -= delta[direction]
                direction = turn_right[direction]
                position += delta[direction]
        print 'square', time.time() - start_time
        return (Vector(), Vector())
    def useMooreNeighborTracing(start):
        pass

    cycles = 0
    start_time = time.time()
    while True:
        cycles += 1
        if (time.time() - start_time) > 1.0: # If this cycle exceeds 2 seconds, break out.
            break
        candidates = np.argwhere(img >= threshold)
        if len(candidates) == 0:
            break
        candidate = candidates[0]
        cy = candidate[0]
        cx = candidate[1]
        img[cy][cx][0] = 0
        # Stop processing if the newest value is at the bottom.
        if (cy > img_height - min_length):
            break

        useSquareTracing(Vector(cx, cy))
        useWilburContour(Vector(cx, cy))
        break
        (center, size) = useWilburContour(Vector(cx, cy))
        y = center.y
        x = center.x

        if (size.x <= min_length or size.y <= min_length):
            clearArea(center, size)
            continue

        step = 2
        value = img[y][x][0]
        value_threshold = threshold / 2
        for delta in range(0, min_length - step):
            if abs(value - int(img[y - delta][x][0])) > value_threshold:
                y = y - delta
                break
            if abs(value - int(img[y][x - delta][0])) > value_threshold:
                x = x - delta
                break
            if abs(value - int(img[y][x + delta][0])) > value_threshold:
                x = x + delta
                break

        top = getValue([y - step, x - step], [y - step, x + step])
        bottom = getValue([y + step, x - step], [y + step, x + step])
        left = getValue([y - step, x - step], [y + step, x - step])
        right = getValue([y - step, x + step], [y + step, x + step])
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
            addPixel(center, size, key_direction)
            clearArea(center, size)
    #print cycles
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
