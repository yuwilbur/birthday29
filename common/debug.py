import pygame
import time

class Debugger:
    def __init__(self):
        pygame.font.init()
        self._fontArial = pygame.font.SysFont('Arial', 12)
        self._log = ''

    def append(self, log):
        self._log += log

    def clear(self):
        self._log = ''

    def createSurface(self):
        return self._fontArial.render(self._log, False, (0, 255, 0))

class PerformanceLogger:
    def __init__(self, name):
        self._name = name
        self._log = 0.0
        self._lastGetLog = 0.0

    def startLog(self):
        self._start = time.time()

    def endLog(self):
        self._end = time.time()

    def getLog(self):
        if(time.time() - self._lastGetLog > 0.2):
            self._lastGetLog = time.time()
            self._log = self._end - self._start
        return self._name + ' ' + format(self._log*1000, '.0f') + 'ms'
