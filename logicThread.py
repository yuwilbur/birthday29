from common.input import Input
import threading
import time

class LogicThread(threading.Thread):
    def __init__(self, event_dispatcher):
        super(LogicThread, self).__init__()
        self._stop_event = threading.Event()
        self.input = Input(event_dispatcher)

    def stop(self):
        self._stop_event.set()
        
    def run(self):
        loopPeriodThreshold = 0.01
        while(not self._stop_event.is_set()):
            startTime = time.time()
            self.input.update()
            endTime = time.time()
            loopPeriodDelta = loopPeriodThreshold - (endTime - startTime)
            if (loopPeriodDelta > 0.0):
                time.sleep(loopPeriodDelta)
