import time

class PeriodSync:
    DESIRED_PERIOD = 0.033
    PERIOD = DESIRED_PERIOD

    def Start(self):
        self._start_time = time.time()

    def End(self):
        self._end_time = time.time()
            
    def Sync(self):
    	self.PERIOD = self._end_time - self._start_time
        delta = self.DESIRED_PERIOD - self.PERIOD
        if (delta > 0):
            time.sleep(delta)
    
