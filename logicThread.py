from common.input import Input
import threading
import time

class LogicThread(threading.Thread):
    def setDispatcher(self, event_dispatcher):
        self.event_dispatcher = event_dispatcher
        
    def run(self):
        loopPeriodThreshold = 0.01
        input = Input(self.event_dispatcher)
        while(True):
            startTime = time.time()
            input.update()
            endTime = time.time()
            loopPeriodDelta = loopPeriodThreshold - (endTime - startTime)
            if (loopPeriodDelta > 0.0):
                time.sleep(loopPeriodDelta)
