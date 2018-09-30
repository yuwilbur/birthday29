from ..common import config
from ..common.singleton import Singleton
from ..engine.game_engine import GameEngine
from ..engine.vector import Vector
from ..engine.transform import Transform
from ..sync.period_sync import PeriodSync
from ..engine.primitive import Solid
from ..engine.game_object import GameObject
from ..engine.primitive import Circle
from ..engine.primitive import Rectangle
from ..engine.material import *
from ..engine.gradient_rectangle import GradientRectangle
from ..engine.gradient_circle import GradientCircle
from ..engine.line import *
from ..engine.ui import *
from ..sync.manager import Manager
from ..renderer.color import Color

import pygame
import math
import time

class Renderer(Manager):
    __metaclass__ = Singleton
    def __init__(self):
        super(Renderer, self).__init__()
        self._engine = GameEngine()
        display_info = pygame.display.Info()
        resolution = Vector(1280, 720)
        self._resolution = resolution
        self._fps = GameObject("fps")
        self._fps.addComponent(TextBox)
        self._fps.getComponent(TextBox).font_size = 30
        self._fps.getComponent(TextBox).width = 1000
        self._fps.getComponent(TextBox).height = 100
        self._fps.getComponent(TextBox).align = Align.CENTER
        self._fps.getComponent(TextBox).color = Color.BLACK
        self._fps.getComponent(Transform).position = Vector(0, - self._resolution.y / 2 + 60)
        self._fps.getComponent(TextBox).setTexts([""])
        self._start_time = time.time()

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

    def renderGradientRectangles(self):
        rectangles = self._engine.getObjectsWithType(GradientRectangle)
        for rectangle_id, rectangle in rectangles.items():
            width = rectangle.dimensions.x
            if (width == 0):
                continue
            height = rectangle.dimensions.y
            position = self._center + rectangle.getComponent(Transform).position
            step = rectangle.step
            color_diff = [
                (rectangle.end_color[0] - rectangle.start_color[0]) * step / float(width),
                (rectangle.end_color[1] - rectangle.start_color[1]) * step / float(width),
                (rectangle.end_color[2] - rectangle.start_color[2]) * step / float(width),
                (rectangle.end_color[3] - rectangle.start_color[3]) * step / float(width)
                ]
            count = 0
            for x in range(position.x - width / 2, position.x + width / 2, step):
                rect = pygame.Rect(0,0,0,0)
                rect.size = (step, height)
                rect.center = (x, position.y)
                rectangle_color = [
                    int(rectangle.start_color[0] + color_diff[0] * count),
                    int(rectangle.start_color[1] + color_diff[1] * count),
                    int(rectangle.start_color[2] + color_diff[2] * count),
                    int(rectangle.start_color[3] + color_diff[3] * count)
                    ]
                pygame.draw.rect(self._screen, rectangle_color, rect)
                count += 1

    def renderGradientCircles(self):
        circles = self._engine.getObjectsWithType(GradientCircle)
        for circle_id, circle in circles.items():
            radius = circle.radius
            if (radius == 0):
                continue
            position = self._center + circle.getComponent(Transform).position + circle.offset
            step = circle.step
            thickness = min(radius, circle.thickness)
            if (step == 0):
                pygame.draw.circle(self._screen, circle.start_color, position.toIntTuple(), radius, thickness)
                continue
            color_diff = [
                (circle.end_color[0] - circle.start_color[0]) * step / float(thickness),
                (circle.end_color[1] - circle.start_color[1]) * step / float(thickness),
                (circle.end_color[2] - circle.start_color[2]) * step / float(thickness),
                (circle.end_color[3] - circle.start_color[3]) * step / float(thickness)
                ]
            count = 0
            for width in range(thickness, 0, -step):
                color = [
                    int(circle.end_color[0] - color_diff[0] * count),
                    int(circle.end_color[1] - color_diff[1] * count),
                    int(circle.end_color[2] - color_diff[2] * count),
                    int(circle.end_color[3] - color_diff[3] * count)
                    ]
                width = min(width, radius)
                pygame.draw.circle(self._screen, color, position.toIntTuple(), radius, width)
                count += 1

    def renderMaterial(self, material_type):
        materials = self._engine.getObjectsWithType(material_type)
        for material_id, material in materials.items():
            position = (self._center + material.getComponent(Transform).position).toIntTuple()
            if material.hasComponent(Circle):
                pygame.draw.circle(self._screen, material.color, position, material.getComponent(Circle).radius)
            elif material.hasComponent(Rectangle):
                if material.getComponent(Rectangle).dimensions == Vector():
                    continue
                rect = pygame.Rect(0,0,0,0)
                rect.size = material.getComponent(Rectangle).dimensions.toIntTuple()
                rect.center = position
                pygame.draw.rect(self._screen,  material.color, rect, material.width)

    def renderUI(self):
        uis = self._engine.getObjectsWithType(UI)
        for ui_id, ui in uis.items():
            surface = ui.getComponent(UI).getSurface()
            if surface == None:
                continue
            position = (self._center + ui.getComponent(Transform).position - Vector(surface.get_width() / 2, surface.get_height() / 2)).toIntTuple()
            self._screen.blit(surface, position, (0, 0, surface.get_width(), surface.get_height()))

    def update(self):
        latency = str(int(1.0 / (time.time() - self._start_time)))
        self._fps.getComponent(TextBox).setTexts([latency])
        self._start_time = time.time()
        self._screen.fill(Color.BLACK)
        self._screen.set_alpha(None)
        self.renderGradientRectangles()
        self.renderGradientCircles()
        self.renderLines()
        self.renderDashedLines()
        self.renderMaterial(Material)
        self.renderMaterial(LateMaterial)
        self.renderUI()
        self.renderMaterial(PostUIMaterial)
        pygame.display.update()

    
        
