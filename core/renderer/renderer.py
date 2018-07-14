from ..common.events import RGBImageEvent
from ..engine.game_engine import GameEngine
from ..engine.vector import Vector
from ..sync.period_sync import PeriodSync
from ..engine.primitive import Circle
from ..engine.primitive import Rectangle
from ..engine.solid import Solid
from ..renderer.color import Color
from ..renderer import color # see if there's a better way for this

import pygame
import threading

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
        print 'Resolution', self._resolution
        self._screen = pygame.display.set_mode(self._resolution, screen_attributes)
        self._event_dispatcher.add_event_listener(RGBImageEvent.TYPE, self.processRGBImageEvent)
        self._camera_surface = None
        self._center = Vector(self._resolution[0] / 2, self._resolution[1] / 2)
        print 'Center', self._center

        period_sync = PeriodSync()
        while not self._stop_event.is_set():
            period_sync.Start()
            self._screen.fill(color.BLACK.toTuple())
            solids = self._engine.getSolids()
            for solid_id, solid in solids.items():
                position = (solid.position + self._center).toIntTuple()
                if solid.hasComponent(Circle):
                    pygame.draw.circle(self._screen, color.WHITE.toTuple(), position, solid.getComponent(Circle).radius)
                elif solid.hasComponent(Rectangle):
                    dimensions = solid.getComponent(Rectangle).dimensions
                    rect = pygame.Rect(0,0,0,0)
                    rect.width = dimensions[0]
                    rect.height = dimensions[1]
                    rect.center = position
                    pygame.draw.rect(self._screen, color.WHITE.toTuple(), rect)
            if not self._camera_surface == None:
                self._screen.blit(self._camera_surface, (0,0), (0, 0, self._camera_surface.get_width(), self._camera_surface.get_height()))
            pygame.display.update()
            period_sync.End()
            period_sync.Sync()

    def processRGBImageEvent(self, event):
            self._camera_surface = pygame.image.frombuffer(event.data()[0], event.data()[1], 'RGB')

    
        
