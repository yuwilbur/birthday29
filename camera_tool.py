import numpy as np
import pygame
try:
    import picamera
except ImportError:
    pass
import sys
import copy

class CameraTool:
    RESOLUTION_LO = (320, 160)
    RESOLUTION_MI = (640, 320)
    RESOLUTION_HI = (1280, 640)

    def __init__(self):
        pygame.init()
        displayInfo = pygame.display.Info()
        self.camera = self.createCamera(self.RESOLUTION_LO)
        self.displayResolution = (displayInfo.current_w, displayInfo.current_h)
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 30)

    def createCamera(self, resolution):
        self.resolution = resolution
        self.rawData = np.empty((self.resolution[0], self.resolution[1], 3), dtype=np.uint8)
        self.processedData = copy.deepcopy(self.rawData)
        if not 'picamera' in sys.modules:
            return
        if self.camera is not None:
            self.camera.close()
        self.camera = Camera(self.resolution)

    def run(self):
        screenAttributes = pygame.HWSURFACE | pygame.DOUBLEBUF
        screen = pygame.display.set_mode(self.displayResolution, screenAttributes)
        _running = True
        _paused = False
        while _running:
            if not _paused and not self.camera == None:
                self.camera.capture(self._raw, use_video_port=True, format='yuv')
            self.processedData[:,:,0] = self.rawData[:,:,0]
            self.processedData[:,:,1] = self.rawData[:,:,0]
            self.processedData[:,:,2] = self.rawData[:,:,0]
            surface = pygame.image.frombuffer(self.processedData, self.processedData.shape[0:2], 'RGB')
            surface = pygame.transform.scale(surface, self.displayResolution)
            screen.blit(surface, (0,0), (0,0,surface.get_width(),surface.get_height()))
            log = '[P]ause | [S]ave | [L]oad | ' + str(self.resolution[0]) + 'x' + str(self.resolution[1])
            screen.blit(self.font.render(log, False, (0, 255, 0)), (0,0))
            pygame.display.update()
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
