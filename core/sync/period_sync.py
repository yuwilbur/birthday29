from ..common.singleton import Singleton

import time

class PeriodSync:
    __metaclass__ = Singleton

    DESIRED_PERIOD = 0.033

    def __init__(self):
    	super(PeriodSync, self).__init__()
    	self.period = self.DESIRED_PERIOD

    def Start(self):
        self._start_time = time.time()

    def End(self):
        self._end_time = time.time()
            
    def Sync(self):
    	self.period = self._end_time - self._start_time
        delta = self.DESIRED_PERIOD - self.period
        if (delta > 0):
            time.sleep(delta)
    
