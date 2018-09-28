import time

class PeriodSync:
    PERIOD = 0.02 # 30Hz

    def Start(self):
        self._start_time = time.time()

    def End(self):
        self._end_time = time.time()
            
    def Sync(self):
        delta = self.PERIOD - (self._end_time - self._start_time)
        if (delta > 0):
            time.sleep(delta)
    
