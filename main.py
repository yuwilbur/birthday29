from common.camera import Camera
from common.debug import Debugger
from common.debug import PerformanceLogger
from threading import Thread
from logicThread import LogicThread
from common.event import EventDispatcher
from common.inputEvent import InputEvent
from common.periodSync import PeriodSync
import numpy as np 
import pygame
import time
import picamera
import sys

class Birthday29():
    def run(self):
        pygame.init()
        #screenAttributes = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
        screenAttributes = 0
        screen = pygame.display.set_mode(Camera.RESOLUTION_LO, screenAttributes)
        debugger = Debugger()
        displayLogger = PerformanceLogger('Display')
        processLogger = PerformanceLogger('Process')

        self._running = True

        event_dispatcher = EventDispatcher()
        event_dispatcher.add_event_listener(InputEvent.TYPE, self.processInputEvent)
        
        logicThread = LogicThread(event_dispatcher)
        logicThread.setDaemon(True)
        logicThread.start()

        periodSync = PeriodSync()
        while(self._running):
            start_time = time.time()
            
            processLogger.startLog()
            #camera.rawToGrayscale(rawData, processedData)
            processLogger.endLog()
            debugger.append(processLogger.getLog() + ' ')

            displayLogger.startLog()
            # surface = pygame.image.frombuffer(processedData, BdCamera.RESOLUTION_LO, 'RGB')
            # screen.blit(surface, (0,0), (0,0,surface.get_width(),surface.get_height()))
            # screen.blit(debugger.createSurface(), (0,0))
            debugger.clear()
            pygame.display.update()
            displayLogger.endLog()
            debugger.append(displayLogger.getLog() + ' ')

            end_time = time.time()
            
            periodSync.Sync(end_time - start_time)

        logicThread.stop()
        logicThread.join()
        pygame.quit()

    def processInputEvent(self, event):
        if event == InputEvent.ESCAPE:
            self._running = False
            pygame.quit()
            sys.exit()
        if event == InputEvent.Q:
            self._running = False

if (__name__ == "__main__"):
    Birthday29().run()
