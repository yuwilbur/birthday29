from common.camera import BdCamera
from common.debug import Debugger
from common.debug import PerformanceLogger
import numpy as np 
import pygame
import time
import picamera

RESOLUTION_TYPE = 0

if (RESOLUTION_TYPE == 0):
    RESOLUTION = (320, 160)
elif(RESOLUTION_TYPE == 1):
    RESOLUTION = (640, 320)
elif(RESOLUTION_TYPE == 2):
    RESOLUTION = (1280, 640)

def processData(raw, processed):
    processed[0::3] = raw[0:raw.size / 3]
    processed[1::3] = raw[0:raw.size / 3]
    processed[2::3] = raw[0:raw.size / 3]

def main():
    camera = BdCamera(RESOLUTION)
    pygame.init()
    screenAttributes = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
    screen = pygame.display.set_mode(RESOLUTION, screenAttributes)
    debugger = Debugger()
    cameraLogger = PerformanceLogger('Camera')
    displayLogger = PerformanceLogger('Display')
    processLogger = PerformanceLogger('Process')
    rawData = camera.createEmptyData()
    processedData = camera.createEmptyData()
    _running = True
    while(_running):
        cameraLogger.startLog()
        camera.capture(rawData)
        cameraLogger.endLog()
        debugger.append(cameraLogger.getLog() + ' ')
        
        processLogger.startLog()
        processData(rawData, processedData)
        processLogger.endLog()
        debugger.append(processLogger.getLog() + ' ')

        displayLogger.startLog()
        surface = pygame.image.frombuffer(processedData, RESOLUTION, 'RGB')
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
