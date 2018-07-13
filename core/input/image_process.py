from ..common.events import YImageEvent

from multiprocessing import Process, Pipe, Lock
import copy
import time

def processYImage(y, resolution):
    start = time.time()
    total = 0
    width = resolution[0]
    height = resolution[1]
    for i in range(0, width - 1):
        test = i*height
        for j in range(0, height - 1):
            if y[j + test] > 0:
                total += 1
            # total = total + y[j*resolution[0] + i]
    return time.time() - start

def yImageWorker(lock, pipe):
    main_conn, worker_conn = pipe
    while True:
        lock.acquire()
        data = worker_conn.recv()
        lock.release()
        if data == ImageProcess.END_MESSAGE:
            break;
        if not main_conn.poll():
            worker_conn.send(processYImage(data[0], data[1]))

class ImageProcess():
    END_MESSAGE = 'END'
    def __init__(self, event_dispatcher):
        self._event_dispatcher = event_dispatcher
        self._event_dispatcher.add_event_listener(YImageEvent.TYPE, self.processYImageEvent)
        self._lock = Lock()
        self._main_conn, self._worker_conn = Pipe()
        
        self._worker1 = Process(target=yImageWorker, args=(self._lock, (self._main_conn, self._worker_conn),))
        self._worker1.daemon = True
        self._worker1.start()

        self._worker2 = Process(target=yImageWorker, args=(self._lock, (self._main_conn, self._worker_conn),))
        self._worker2.daemon = True
        self._worker2.start()

    def stop(self):
        self._main_conn.send(ImageProcess.END_MESSAGE)
        self._main_conn.send(ImageProcess.END_MESSAGE)
        self._worker1.join()
        self._worker2.join()
        
    def update(self):
        if not self._main_conn.poll():
            return
        data = self._main_conn.recv()
        print data

    def processYImageEvent(self, event):
        resolution = event.data()[1]
        y_data = event.data()[0]
        if not self._worker_conn.poll():
            self._main_conn.send((copy.deepcopy(y_data), resolution))
