from common.camera import BdCamera
from common.debug import Debugger
from common.debug import PerformanceLogger
import numpy as np 
import pygame
import time
import picamera

def main():
    camera = BdCamera(BdCamera.RESOLUTION_LO)
    pygame.init()
    screenAttributes = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
    screen = pygame.display.set_mode(BdCamera.RESOLUTION_LO, screenAttributes)
    debugger = Debugger()
    cameraLogger = PerformanceLogger('Camera')
    displayLogger = PerformanceLogger('Display')
    processLogger = PerformanceLogger('Process')
    rawData = camera.createEmptyRawData()
    processedData = camera.createEmptyRawData()
    _running = True
    while(_running):
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
            
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    _running = False
    
if (__name__ == "__main__"):
    main()
