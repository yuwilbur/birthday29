from common.camera import BdCamera
from common.debug import Debugger
from common.debug import PerformanceLogger
from threading import Thread
from logicThread import LogicThread
from common.event import EventDispatcher
from common.inputEvent import InputEvent
import numpy as np 
import pygame
import time
import picamera
import sys

class Birthday29():
    def run(self):
        camera = BdCamera(BdCamera.RESOLUTION_LO)
        pygame.init()
        #screenAttributes = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
        screenAttributes = 0
        screen = pygame.display.set_mode(BdCamera.RESOLUTION_LO, screenAttributes)
        debugger = Debugger()
        cameraLogger = PerformanceLogger('Camera')
        displayLogger = PerformanceLogger('Display')
        processLogger = PerformanceLogger('Process')
        rawData = camera.createEmptyRawData()
        processedData = camera.createEmptyRawData()
        self._running = True

        event_dispatcher = EventDispatcher()
        event_dispatcher.add_event_listener(InputEvent.TYPE, self.processInputEvent)
        
        logicThread = LogicThread(event_dispatcher)
        logicThread.setDaemon(True)
        logicThread.start()
        
        while(self._running):
            cameraLogger.startLog()
            camera.capture(rawData)
            cameraLogger.endLog()
            debugger.append(cameraLogger.getLog() + ' ')
            
            processLogger.startLog()
            camera.rawToGrayscale(rawData, processedData)
            processLogger.endLog()
            debugger.append(processLogger.getLog() + ' ')

            displayLogger.startLog()
            surface = pygame.image.frombuffer(processedData, BdCamera.RESOLUTION_LO, 'RGB')
            screen.blit(surface, (0,0), (0,0,surface.get_width(),surface.get_height()))
            screen.blit(debugger.createSurface(), (0,0))
            debugger.clear()
            pygame.display.update()
            displayLogger.endLog()
            debugger.append(displayLogger.getLog() + ' ')

            test = 'Test '
            test += str(np.amax(processedData))
            debugger.append(test)

        logicThread.stop()
        logicThread.join()
        pygame.quit()

    def processInputEvent(self, event):
        if event == InputEvent.ESCAPE:
            pygame.quit()
            sys.exit()
        if event == InputEvent.Q:
            self._running = False

if (__name__ == "__main__"):
    Birthday29().run()
