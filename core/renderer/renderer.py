from ..common.event import EventDispatcher
from ..common.events import RGBImageEvent
from ..common.events import GrayscaleImageEvent
from ..common.events import TestEvent
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
        resolution = Vector(display_info.current_w, display_info.current_h)
        resolution.x = 1280
        resolution.y = 720
        self._info_width = 160
        self._game_resolution = resolution - Vector(self._info_width * 2, 0)
        self._resolution = resolution

    def processGrayscaleImageEvent(self, event):
        resolution = (event.data()[0].shape[0], event.data()[0].shape[1])
        self._camera_surface[0] = pygame.image.frombuffer(event.data()[0], resolution, 'RGB')
        self._camera_surface[1] = pygame.image.frombuffer(event.data()[1], resolution, 'RGB')

    def getResolution(self):
        return self._resolution

    def getGameResolution(self):
        return self._game_resolution

    def setup(self):
        print 'Resolution', self._resolution
        #screen_attributes = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
        screen_attributes = 0
        self._screen = pygame.display.set_mode(self._resolution.toIntTuple(), screen_attributes)
        self._event_dispatcher.add_event_listener(GrayscaleImageEvent.TYPE, self.processGrayscaleImageEvent)
        self._camera_surface = [None,None]
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
        if not self._camera_surface[0] == None:
            size = (0, 0, self._camera_surface[0].get_width(), self._camera_surface[0].get_height())
            position = (0, self._resolution.y - self._camera_surface[0].get_height())
            self._screen.blit(self._camera_surface[0], position, size)
        if not self._camera_surface[1] == None:
            size = (0, 0, self._camera_surface[1].get_width(), self._camera_surface[1].get_height())
            position = (self._resolution.x - self._camera_surface[1].get_width(), self._resolution.y - self._camera_surface[1].get_height())
            self._screen.blit(self._camera_surface[1], position, size)
        pygame.display.update()

    
        
