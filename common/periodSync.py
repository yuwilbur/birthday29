import time

class PeriodSync:
    def __init__(self, period=None):
        if period == None:
            self.period = 0.01
        else:
            self.period = period
            
    def Sync(self, period):
        if (self.period > period):
            time.sleep(self.period - period)
    
