from ..common.event import EventDispatcher
from ..common.events import RGBImageEvent
from ..common.singleton import Singleton
from ..engine.game_engine import GameEngine
from ..engine.vector import Vector
from ..sync.period_sync import PeriodSync
from ..engine.primitive import Circle
from ..engine.primitive import Rectangle
from ..engine.solid import Solid
from ..engine.material import Material
from ..renderer import color
from ..sync.manager import Manager

import pygame

class Renderer(Manager):
    __metaclass__ = Singleton

    def __init__(self):
        super(Renderer, self).__init__()
        self._event_dispatcher = EventDispatcher()
        self._engine = GameEngine()
        display_info = pygame.display.Info()
        self._resolution = Vector(display_info.current_w, display_info.current_h - 200)

    def processRGBImageEvent(self, event):
            self._camera_surface = pygame.image.frombuffer(event.data()[0], event.data()[1], 'RGB')

    def getResolution(self):
        return self._resolution

    def setup(self):
        print 'Resolution', self._resolution
        #screen_attributes = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
        screen_attributes = 0
        self._screen = pygame.display.set_mode(self._resolution.toIntTuple(), screen_attributes)
        self._event_dispatcher.add_event_listener(RGBImageEvent.TYPE, self.processRGBImageEvent)
        self._camera_surface = None
        self._center = self._resolution / 2
        print 'Center', self._center

    def update(self):
        self._screen.fill(color.BLACK.toTuple())
        solids = self._engine.getSolids()
        for solid_id, solid in solids.items():
            position = (solid.position + self._center).toIntTuple()
            if solid.hasComponent(Circle):
                pygame.draw.circle(self._screen, solid.getComponent(Material).color.toTuple(), position, solid.getComponent(Circle).radius)
            elif solid.hasComponent(Rectangle):
                rect = pygame.Rect(0,0,0,0)
                rect.size = solid.getComponent(Rectangle).dimensions.toIntTuple()
                rect.center = position
                pygame.draw.rect(self._screen, solid.getComponent(Material).color.toTuple(), rect)
        if not self._camera_surface == None:
            self._screen.blit(self._camera_surface, (0,0), (0, 0, self._camera_surface.get_width(), self._camera_surface.get_height()))
        pygame.display.update()

    
        
