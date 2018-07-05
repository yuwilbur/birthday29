from common.camera import BdCamera
from common.debug import Debugger
from common.debug import PerformanceLogger
import numpy as np 
import pygame
import time
import picamera

RESOLUTION = 0

if (RESOLUTION == 0):
    WIDTH = 320
    HEIGHT = 240
elif(RESOLUTION == 1):
    WIDTH = 640
    HEIGHT = 480
elif(RESOLUTION == 2):
    WIDTH = 1280
    HEIGHT = 720

def processData(raw, processed):
    processed[0::3] = raw[0:raw.size / 3]
    processed[1::3] = raw[0:raw.size / 3]
    processed[2::3] = raw[0:raw.size / 3]

def main():
    camera = BdCamera(WIDTH, HEIGHT)
    pygame.init()
    screenAttributes = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
    screen = pygame.display.set_mode((WIDTH,HEIGHT), screenAttributes)
    debugger = Debugger()
    _running = True
    cameraLogger = PerformanceLogger('Camera')
    displayLogger = PerformanceLogger('Display')
    processLogger = PerformanceLogger('Process')
    rawData = camera.createEmptyData()
    processedData = camera.createEmptyData()
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
        surface = pygame.image.frombuffer(processedData, (WIDTH,HEIGHT), 'RGB')
        screen.blit(surface, (0,0), (0,0,WIDTH,HEIGHT))
        screen.blit(debugger.createSurface(), (0,0))
        debugger.clear()
        pygame.display.update()
        displayLogger.endLog()
        debugger.append(displayLogger.getLog() + ' ')
            
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    _running = False
    
if (__name__ == "__main__"):
    main()
