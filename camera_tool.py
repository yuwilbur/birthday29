from core.common.camera import Camera
from core.common.debug import Debugger
import numpy as np
import pygame
import picamera

class CameraTool:
    def __init__(self):
        pygame.init()
        displayInfo = pygame.display.Info()
        self.camera = None
        self.displayResolution = (displayInfo.current_w, displayInfo.current_h)

    def createCamera(self, resolution):
        if self.camera is not None:
            self.camera.close()
        self.imageResolution = resolution
        self.camera = Camera(self.imageResolution)
        self.rawData = self.camera.createEmptyFullData()
        self.processedData = self.camera.createEmptyFullData()

    def run(self):
        screenAttributes = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
        screen = pygame.display.set_mode(self.displayResolution, screenAttributes)
        debugger = Debugger()

        self.createCamera(Camera.RESOLUTION_LO)
        _running = True
        _paused = False
        while _running:
            if not _paused:
                self.camera.capture(self.rawData)
            Camera.rawToGrayscale(self.rawData, self.processedData)
            surface = pygame.image.frombuffer(self.processedData, self.imageResolution, 'RGB')
            debugger.clear()
            debugger.append('[P]ause | [S]ave | [L]oad | ' + str(self.imageResolution[0]) + 'x' + str(self.imageResolution[1]))
            surface = pygame.transform.scale(surface, self.displayResolution)
            screen.blit(surface, (0,0), (0,0,surface.get_width(),surface.get_height()))
            screen.blit(debugger.createSurface(), (0,0))
            pygame.display.update()
            debugger.clear()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        _running = False
                        break;
                    if event.key == pygame.K_1:
                        self.createCamera(Camera.RESOLUTION_LO)
                        break;
                    if event.key == pygame.K_2:
                        self.createCamera(Camera.RESOLUTION_MI)
                        break;
                    if event.key == pygame.K_3:
                        self.createCamera(Camera.RESOLUTION_HI)
                        break;
                    if event.key == pygame.K_p:
                        _paused = not _paused
                        break;
                    if event.key == pygame.K_s:
                        np.save(Camera.FILENAME, self.rawData)
                        break;
                    if event.key == pygame.K_l:
                        self.rawData = np.load(Camera.FILENAME)
                        break;

if (__name__ == "__main__"):
    cameraTool = CameraTool()
    cameraTool.run()
