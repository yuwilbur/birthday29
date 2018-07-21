from ..common.event import EventDispatcher
from ..common.events import RGBImageEvent
from ..common.events import GrayscaleImageEvent
from ..common.events import TestEvent
from ..common import config
from ..common.singleton import Singleton
from ..engine.game_engine import GameEngine
from ..engine.vector import Vector
from ..engine.transform import Transform
from ..sync.period_sync import PeriodSync
from ..engine.primitive import Solid
from ..engine.primitive import Circle
from ..engine.primitive import Rectangle
from ..engine.material import Material
from ..engine.ui import UI
from ..renderer import color
from ..sync.manager import Manager

import pygame

class Renderer(Manager):
    __metaclass__ = Singleton
    class PlayerInfo(object):
        def __init__(self):
            self.camera_surface = None

    def __init__(self):
        super(Renderer, self).__init__()
        self._engine = GameEngine()
        display_info = pygame.display.Info()
        #resolution = Vector(display_info.current_w, display_info.current_h)
        resolution = Vector(1280, 720)
        self._text_height = 200
        self._camera_height = 160
        self._info_width = 160
        self._resolution = resolution

    def processGrayscaleImageEvent(self, event):
        resolution = (event.data()[0].shape[0], event.data()[0].shape[1])
        #self._p1_info.camera_surface = pygame.image.frombuffer(event.data()[0], resolution, 'RGB')
        #self._p2_info.camera_surface = pygame.image.frombuffer(event.data()[1], resolution, 'RGB')

    def getResolution(self):
        return self._resolution

    def setup(self):
        print 'Resolution', self._resolution
        screen_attributes = 0
        if config.FULL_SCREEN:
            screen_attributes = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
        self._screen = pygame.display.set_mode(self._resolution.toIntTuple(), screen_attributes)
        EventDispatcher().add_event_listener(GrayscaleImageEvent.TYPE, self.processGrayscaleImageEvent)
        self._p1_info = Renderer.PlayerInfo()
        self._p2_info = Renderer.PlayerInfo()
        self._p1_info.text_surface = pygame.Surface((self._info_width, self._text_height))
        self._center = self._resolution / 2
        print 'Center', self._center

    def update(self):
        self._screen.fill(color.BLACK.toTuple())
        materials = self._engine.getObjectsWithType(Material)
        for material_id, material in materials.items():
            position = (material.getComponent(Transform).position + self._center).toIntTuple()
            if material.hasComponent(Circle):
                pygame.draw.circle(self._screen, material.color.toTuple(), position, material.getComponent(Circle).radius)
            elif material.hasComponent(Rectangle):
                rect = pygame.Rect(0,0,0,0)
                rect.size = material.getComponent(Rectangle).dimensions.toIntTuple()
                rect.center = position
                pygame.draw.rect(self._screen,  material.color.toTuple(), rect)
        pygame.draw.rect(self._screen, color.BLACK.toTuple(), pygame.Rect(0,0,self._info_width,self._resolution.y))
        pygame.draw.rect(self._screen, color.BLACK.toTuple(), pygame.Rect(self._resolution.x - self._info_width,0,self._resolution.x,self._resolution.y))
        if not self._p1_info.camera_surface == None:
            dimensions = (self._info_width, self._camera_height)
            size = (0, 0, dimensions[0], dimensions[1])
            position = (0, self._resolution.y - dimensions[1])
            self._screen.blit(self._p1_info.camera_surface, position, size)
        if not self._p2_info.camera_surface == None:
            dimensions = (self._info_width, self._camera_height)
            size = (0, 0, dimensions[0], dimensions[1])
            position = (self._resolution.x - dimensions[0], self._resolution.y - dimensions[1])
            self._screen.blit(self._p2_info.camera_surface, position, size)
        uis = self._engine.getObjectsWithType(UI)
        for ui_id, ui in uis.items():
            surface = ui.getComponent(UI).getSurface()
            if surface == None:
                continue
            position = (ui.getComponent(Transform).position - Vector(surface.get_width() / 2, surface.get_height() / 2)).toIntTuple()
            self._screen.blit(surface, position, (0, 0, surface.get_width(), surface.get_height()))
        pygame.display.update()

    
        
