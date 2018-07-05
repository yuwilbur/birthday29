import pygame
import time

class Debugger:
    def __init__(self):
        pygame.font.init()
        self.fontArial = pygame.font.SysFont('Arial', 12)
        self.log = ''

    def append(self, log):
        self.log += log

    def clear(self):
        self.log = ''

    def createSurface(self):
        return self.fontArial.render(self.log, False, (0, 255, 0))

class PerformanceLogger:
    def __init__(self, name):
        self.name = name
        self.log = 0.0
        self.lastGetLog = 0.0

    def startLog(self):
        self.start = time.time()

    def endLog(self):
        self.end = time.time()

    def getLog(self):
        if(time.time() - self.lastGetLog > 0.2):
            self.lastGetLog = time.time()
            self.log = self.end - self.start
        return self.name + ' ' + format(self.log*1000, '.0f') + 'ms'
