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
    img = img.reshape((img_width,img_height))
    threshold = 150
    min_length = 12

    def isWithinBounds(position):
        return position.x >= 0 and position.x < img_width and position.y >= 0 and position.y < img_height
    def addPixel(pixel, size = Vector(1,1), direction = Key.DEBUG):
        results.append(ImageInput(pixel, direction, size))
    def clearArea(center, size):
        img[center.y - size.y / 2: center.y + size.y / 2 + 1, center.x - size.x / 2:center.x + size.x / 2 + 1] = 0
    def getValueFromArea(center, size):
        return np.average(img[center.y - size.y / 2: center.y + size.y / 2 + 1, center.x - size.x / 2:center.x + size.x / 2 + 1])
    def getValue(center):
        if center.x < 0:
            return 0
        if center.x >= img_width:
            return 0
        if center.y < 0:
            return 0
        if center.y >= img_height:
            return 0 
        return img[center.y][center.x]
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
            if img[y][x] < threshold:
                y -= 1
                break
            for x in range(x, max_x + 1, +1):
                if img[y][x] < threshold:
                    if (x > min_x):
                        x -= 1
                    break
        if (x > min_x):
            x -= 1
        for y in range(y, max_y + 1, +1):
            if img[y][x] < threshold:
                y -= 1
                break
        right = Vector(x - cx, y - cy)

        # Find top left corner.
        x = cx
        for y in range(cy + 1, max_y + 1, +1):
            if img[y][x] < threshold:
                y -= 1
                break
            for x in range(x, min_x - 1, -1):
                if img[y][x] < threshold:
                    if (x < max_x):
                        x += 1
                    break
        if (x < max_x):
            x += 1
        for y in range(y, min_y - 1, -1):
            if img[y][x] < threshold:
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
        #print 'wilbur', time.time() - start_time
        return (center, Vector(length, length))
    def useSquareTracing(start):
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

        def onUp(position):
            position.y -= 1
        def onDown(position):
            position.y += 1
        def onLeft(position):
            position.x -= 1
        def onRight(position):
            position.x += 1

        onMove = {
            up : onUp,
            down : onDown,
            left : onLeft,
            right : onRight
        }

        top_left = copy.copy(start)
        bot_right = copy.copy(start)

        start_time = time.time()
        direction = right
        start_direction = direction
        position = start
        while(getValue(position + delta[direction]) < threshold):
            direction = turn_right[direction]
            if direction == start_direction:
                return (start, Vector(1,1))
        position += delta[direction]
        #onMove[direction](position)
        while(not position == start):
            if (time.time() - start_time) > 0.25:
                break
            if (getValue(position) >= threshold):
                if (position.y > bot_right.y):
                    bot_right.y = position.y
                if (position.x < top_left.x):
                    top_left.x = position.x
                if (position.x > bot_right.x):
                    bot_right.x = position.x
                direction = turn_left[direction]
            else:
                direction = turn_right[direction]
            #position += delta[direction]
            onMove[direction](position)
        #print time.time() - start_time
        return ((top_left + bot_right) / 2, bot_right - top_left + Vector(3,3))
    def useMooreNeighborTracing(start):
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
        top_left = copy.copy(start)
        bot_right = copy.copy(start)

        start_time = time.time()
        direction = right
        position = start + delta[direction]
        start_direction = copy.copy(direction)
        while(getValue(position + delta[direction]) < threshold):
            direction = turn_right[direction]
            if direction == start_direction:
                return (start, Vector(1,1))
        while(not position == start):
            if (time.time() - start_time) > 0.1:
                break
            if (getValue(position) >= threshold):
                if (position.y > bot_right.y):
                    bot_right.y = position.y
                if (position.x < top_left.x):
                    top_left.x = position.x
                if (position.x > bot_right.x):
                    bot_right.x = position.x
            direction = turn_left[direction]
            start_position = position
            position = start_position + delta[direction]
            while(getValue(position) < threshold):
                direction = turn_right[direction]
                position = start_position + delta[direction]
        return ((top_left + bot_right) / 2, bot_right - top_left + Vector(2,2))

    start_time = time.time()
    cycles = 0
    while True:
        if (time.time() - start_time) > 2.0:
            break
        cycles += 1
        candidates = np.argwhere(img >= threshold)
        if len(candidates) == 0:
            break
        candidate = candidates[0]
        cy = candidate[0]
        cx = candidate[1]
        # Stop processing if the newest value is at the bottom.
        if (cy > img_height - min_length):
            break

        #useMooreNeighborTracing(Vector(cx, cy))
        (center, size) = useSquareTracing(Vector(cx, cy))
        #(center, size) = useWilburContour(Vector(cx, cy))
        y = center.y
        x = center.x

        if (size.x <= min_length or size.y <= min_length):
            clearArea(center, size)
            continue

        step = 2
        value = img[y][x]
        value_threshold = threshold / 2
        step_limit = min_length - step
        if (y - step_limit < 0 or x - step_limit < 0 or x + step_limit >= img_width):
            clearArea(center, size)
            continue
        for delta in range(0, step_limit):
            if abs(value - int(img[y - delta][x])) > value_threshold:
                y = y - delta
                break
            if abs(value - int(img[y][x - delta])) > value_threshold:
                x = x - delta
                break
            if abs(value - int(img[y][x + delta])) > value_threshold:
                x = x + delta
                break

        top = getValueFromArea(Vector(x,y - step), Vector(step * 2, 0))
        bottom = getValueFromArea(Vector(x,y + step), Vector(step * 2, 0))
        left = getValueFromArea(Vector(x - step,y), Vector(0, step * 2))
        right = getValueFromArea(Vector(x + step,y), Vector(0, step * 2))
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
    if (time.time() - start_time > 1.0):
         print cycles, time.time() - start_time
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
