import time

class PeriodSync:
    def __init__(self, period=None):
        if period == None:
            self._period = 0.033 # 30Hz
        else:
            self._period = period

    def Start(self):
        self._start_time = time.time()

    def End(self):
        self._end_time = time.time()
            
    def Sync(self):
        delta = self._period - (self._end_time - self._start_time)
        if (delta > 0):
            time.sleep(delta)
    
