from ..common.event import EventDispatcher
from ..common.events import *

from multiprocessing import Process, Pipe, Lock
import copy
import time

def processYImage(y):
    return
    start = time.time()
    total = 0
    width = y.shape[0]
    height = y.shape[1]
    for i in range(0, width - 1):
        for j in range(0, height - 1):
            if y[j][i] > 0:
                total += 1
            # total = total + y[j*resolution[0] + i]
    return time.time() - start

def yImageWorker(pipe):
    main_conn, worker_conn = pipe
    while True:
        data = worker_conn.recv()
        if data == ImageProcess.END_MESSAGE:
            break;
        if not main_conn.poll():
            worker_conn.send((data.timestamp, processYImage(data.data)))

class ImageProcess(object):
    END_MESSAGE = 'END'
    def __init__(self, event_dispatcher):
        self._event_dispatcher = event_dispatcher
        self._event_dispatcher.add_event_listener(YImageEvent.TYPE, self.processYImageEvent)
        
        self._main1_conn, self._worker1_conn = Pipe()
        self._worker1 = Process(target=yImageWorker, args=((self._main1_conn, self._worker1_conn),))
        self._worker1.daemon = True
        self._worker1.start()

        self._main2_conn, self._worker2_conn = Pipe()
        self._worker2 = Process(target=yImageWorker, args=((self._main2_conn, self._worker2_conn),))
        self._worker2.daemon = True
        self._worker2.start()

    def processYImageEvent(self, event):
        if not self._worker1_conn.poll():
            self._main1_conn.send(event.data()[0])
        if not self._worker2_conn.poll():
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
            #print 'p1: ', data
        if self._main2_conn.poll():
            data = self._main2_conn.recv()
            #print 'p2: ', data
