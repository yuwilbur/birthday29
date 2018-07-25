from ..common.event import EventDispatcher
from ..common.events import *

from multiprocessing import Process, Pipe, Pool
import copy
import time
import numpy as np

def heavyWork():
    total = 0
    for x in range(0,100000):
        total += 1
        total /= 3
    return total

def processYImage(y):
    candidates = np.argwhere(y > 200)
    #print len(candidates)
    #print len(candidates)
    #total = 0
    #for candidate in candidates:
    #    total += y[candidate[0]][candidate[1]]
    return copy.deepcopy(candidates)
    #return len(candidates)
    #return 0

def yImageWorker(pipe):
    main_conn, worker_conn = pipe
    while True:
        data = worker_conn.recv()
        if data == ImageProcess.END_MESSAGE:
            break;
        if not main_conn.poll():
            result = processYImage(data.data)
            worker_conn.send((data.timestamp, result))

class ImageProcess(object):
    END_MESSAGE = 'END'
    def __init__(self):
        EventDispatcher().add_event_listener(YImageEvent.TYPE, self.onYImageEvent)

        self._main1_conn, self._worker1_conn = Pipe()
        self._worker1 = Process(target=yImageWorker, args=((self._main1_conn, self._worker1_conn),))
        self._worker1.daemon = True
        self._worker1.start()

        self._main2_conn, self._worker2_conn = Pipe()
        self._worker2 = Process(target=yImageWorker, args=((self._main2_conn, self._worker2_conn),))
        self._worker2.daemon = True
        self._worker2.start()

    def onYImageEvent(self, event):
        if not self._main1_conn.poll():
            self._main1_conn.send(event.data()[0])
        if not self._main2_conn.poll():
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
            EventDispatcher().dispatch_event(LatencyEvent(LatencyEvent.P1_PROCESSING, data[0]))
            EventDispatcher().dispatch_event(CameraResultEvent(CameraResultEvent.P1, data[1]))
        if self._main2_conn.poll():
            data = self._main2_conn.recv()
            EventDispatcher().dispatch_event(LatencyEvent(LatencyEvent.P2_PROCESSING, data[0]))
            EventDispatcher().dispatch_event(CameraResultEvent(CameraResultEvent.P2, data[1]))
