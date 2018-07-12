from .common.events import YImageEvent
from multiprocessing import Process, Pipe
import time
import copy

def processYImage(pipe):
    main_pipe, worker_pipe = pipe
    main_pipe.close()
    while True:
        try:
            data = worker_pipe.recv()
            start = time.time()
            total = 0
            y = data[0]
            resolution = data[1]
            width = resolution[0]
            height = resolution[1]
            for i in range(0, width - 1):
                test = i*height
                for j in range(0, height - 1):
                    if y[j + test] > 0:
                        total += 1
                    # total = total + y[j*resolution[0] + i]
            print time.time() - start
        except EOFError:
            break
    
    

class ImageProcessThread():
    def __init__(self, event_dispatcher):
        self._event_dispatcher = event_dispatcher
        self._event_dispatcher.add_event_listener(YImageEvent.TYPE, self.processYImage)
        self._main_pipe, self._worker_pipe = Pipe()
        self._processor = Process(target=processYImage, args=((self._main_pipe, self._worker_pipe),))
        self._processor.daemon = True
        self._processor.start()

    def stop(self):
        self._main_pipe.close()
        self._worker_pipe.close()
        self._processor.join()
        
    def processYImage(self, event):
        resolution = event.data()[1]
        y_data = event.data()[0]
        if not self._worker_pipe.poll():
            self._main_pipe.send((copy.deepcopy(y_data), resolution))
