from ..common.events import RGBImageEvent
from ..engine.game_engine import GameEngine
from ..engine.vector import Vector
from ..sync.period_sync import PeriodSync
from ..engine.primitive import Circle
from ..engine.primitive import Rectangle

import pygame
import threading

WHITE = (255, 255, 255)

class Renderer(threading.Thread):
    __instance = None

    @staticmethod
    def getInstance():
        return Renderer.__instance

    def __init__(self, event_dispatcher):
        super(Renderer, self).__init__()
        if Renderer.__instance != None:
            raise Exception("This class is a singleton")
        Renderer.__instance = self
        self._stop_event = threading.Event()
        self._event_dispatcher = event_dispatcher
        self._engine = GameEngine.getInstance()

    def stop(self):
        self._stop_event.set()

    def run(self):
        #screen_attributes = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
        screen_attributes = 0
        display_info = pygame.display.Info()
        self._resolution = (display_info.current_w, display_info.current_h)
        self._screen = pygame.display.set_mode(self._resolution, screen_attributes)
        self._event_dispatcher.add_event_listener(RGBImageEvent.TYPE, self.processRGBImageEvent)
        self._camera_surface = None
        self._center = Vector(self._resolution[0] / 2, self._resolution[1] / 2)
        print self._center

        period_sync = PeriodSync()
        while not self._stop_event.is_set():
            period_sync.Start()
            solids = self._engine.getSolids()
            for solid_id, solid in solids.items():
                position = solid.position + self._center
                if type(solid) == Circle:
                    center = (solid.position.x + self._center.x, solid.position.y + self._center.y)
                    pygame.draw.circle(self._screen, WHITE, center, solid.getRadius())
                elif type(solid) == Rectangle:
                    dimensions = solid.getDimensions()
                    rect = pygame.Rect(0,0,0,0)
                    rect.width = dimensions[0]
                    rect.height = dimensions[1]
                    rect.center = (self._center.x, self._center.y)
                    pygame.draw.rect(self._screen, WHITE, rect)
                else:
                    print type(solid)
            if not self._camera_surface == None:
                self._screen.blit(self._camera_surface, (0,0), (0, 0, self._camera_surface.get_width(), self._camera_surface.get_height()))
            pygame.display.update()
            period_sync.End()
            period_sync.Sync()

    def processRGBImageEvent(self, event):
            self._camera_surface = pygame.image.frombuffer(event.data()[0], event.data()[1], 'RGB')

    
        
