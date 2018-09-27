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
from ..engine.material import LateMaterial
from ..engine.line import *
from ..engine.ui import UI
from ..sync.manager import Manager
from ..renderer.color import Color

import pygame
import math

class Renderer(Manager):
    __metaclass__ = Singleton
    def __init__(self):
        super(Renderer, self).__init__()
        self._engine = GameEngine()
        display_info = pygame.display.Info()
        resolution = Vector(1280, 720)
        self._resolution = resolution

    def getResolution(self):
        return self._resolution

    def setup(self):
        print 'Resolution', self._resolution
        screen_attributes = 0
        if config.FULL_SCREEN:
            screen_attributes = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
        self._screen = pygame.display.set_mode(self._resolution.toIntTuple(), screen_attributes)
        self._center = self._resolution / 2
        print 'Center', self._center

    def renderLines(self):
        lines = self._engine.getObjectsWithType(Line)
        for line_id, line in lines.items():
            pygame.draw.line(self._screen, line.color, (self._center + line.start).toIntTuple(), (self._center + line.end).toIntTuple())

    def renderDashedLines(self):
        lines = self._engine.getObjectsWithType(DashedLine)
        for line_id, line in lines.items():
            if line.dash_length == 0:
                pygame.draw.line(self._screen, line.color, (self._center + line.start).toIntTuple(), (self._center + line.end).toIntTuple())
            elif line.dash_length < 0:
                continue
            else:
                distance_squ = Vector.DistanceSqu(line.end, line.start)
                direction = (line.end - line.start).toUnitVector()
                step = direction * line.dash_length
                offset = direction * (line.offset % (line.dash_length * 2))
                position = line.start + offset
                while(Vector.DistanceSqu(position, line.start) < distance_squ):
                    pygame.draw.line(self._screen, line.color, (self._center + position).toIntTuple(), (self._center + position + step).toIntTuple())
                    position += step * 2

            

    def renderMaterial(self, material_type):
        materials = self._engine.getObjectsWithType(material_type)
        for material_id, material in materials.items():
            position = (self._center + material.getComponent(Transform).position).toIntTuple()
            if material.hasComponent(Circle):
                pygame.draw.circle(self._screen, material.color, position, material.getComponent(Circle).radius)
            elif material.hasComponent(Rectangle):
                rect = pygame.Rect(0,0,0,0)
                rect.size = material.getComponent(Rectangle).dimensions.toIntTuple()
                rect.center = position
                pygame.draw.rect(self._screen,  material.color, rect)

    def update(self):
        self._screen.fill(Color.BLACK)
        self.renderLines()
        self.renderDashedLines()
        self.renderMaterial(Material)
        self.renderMaterial(LateMaterial)
        uis = self._engine.getObjectsWithType(UI)
        for ui_id, ui in uis.items():
            surface = ui.getComponent(UI).getSurface()
            if surface == None:
                continue
            position = (self._center + ui.getComponent(Transform).position - Vector(surface.get_width() / 2, surface.get_height() / 2)).toIntTuple()
            self._screen.blit(surface, position, (0, 0, surface.get_width(), surface.get_height()))
        pygame.display.update()

    
        
