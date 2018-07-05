from common.camera import BdCamera
from common.debug import Debugger
import numpy as np
import pygame
import picamera

WIDTH = 640
HEIGHT = 480

filename = 'testcamera.npy'

def processData(raw, processed):
    processed[0::3] = raw[0:raw.size / 3]
    processed[1::3] = raw[0:raw.size / 3]
    processed[2::3] = raw[0:raw.size / 3]

def main():
    camera = BdCamera(640,480)
    pygame.init()
    screenAttributes = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
    screen = pygame.display.set_mode((WIDTH,HEIGHT), screenAttributes)
    debugger = Debugger()
    rawData = camera.createEmptyData()
    processedData = camera.createEmptyData()
    _running = True
    _paused = False
    while _running:
        if not _paused:
            camera.capture(rawData)
        processData(rawData, processedData)
        surface = pygame.image.frombuffer(processedData, (WIDTH,HEIGHT), 'RGB')
        debugger.clear()
        debugger.append("[P]ause | [S]ave | [L]oad")
        screen.blit(surface, (0,0), (0,0,WIDTH,HEIGHT))
        screen.blit(debugger.createSurface(), (0,0))
        pygame.display.update()
        debugger.clear()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    _running = False
                    break;
                if event.key == pygame.K_p:
                    _paused = not _paused
                    break;
                if event.key == pygame.K_s:
                    np.save(filename, rawData)
                    break;
                if event.key == pygame.K_l:
                    rawData = np.load(filename)
                    break;

if (__name__ == "__main__"):
    main()
