from ..common.events import YImageEvent

from multiprocessing import Process, Pipe
import time
import copy

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
    print time.time() - start

def yImageWork(pipe):
    main_conn, worker_conn = pipe
    main_conn.close()
    while True:
        try:
            data = worker_conn.recv()
            if data == ImageProcess.END_MESSAGE:
                break;
            processYImage(data[0], data[1])
            if not main_conn.poll():
                worker_conn.send(("1"))
        except EOFError:
            break

class ImageProcess():
    END_MESSAGE = 'END'
    def __init__(self, event_dispatcher):
        self._event_dispatcher = event_dispatcher
        self._event_dispatcher.add_event_listener(YImageEvent.TYPE, self.processYImageEvent)
        self._main_conn, self._worker_conn = Pipe()
        self._processor = Process(target=yImageWork, args=((self._main_conn, self._worker_conn),))
        self._processor.daemon = True
        self._processor.start()

    def stop(self):
        self._main_conn.send(ImageProcess.END_MESSAGE)
        self._processor.join()
        
    def update(self):
        if self._main_conn.poll():
            data = self._main_conn.recv()
            #print data

    def processYImageEvent(self, event):
        resolution = event.data()[1]
        y_data = event.data()[0]
        if not self._worker_conn.poll():
            self._main_conn.send((copy.deepcopy(y_data), resolution))
