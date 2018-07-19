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
    class PlayerInfo(object):
        def __init__(self):
            self.camera_surface = None
            self.text_surface = None

    def __init__(self):
        super(Renderer, self).__init__()
        self._event_dispatcher = EventDispatcher()
        self._engine = GameEngine()
        display_info = pygame.display.Info()
        #resolution = Vector(display_info.current_w, display_info.current_h)
        resolution = Vector(1280, 720)
        self._text_height = 200
        self._controls_height = 160
        self._camera_height = 160
        self._info_width = 160
        self._game_resolution = resolution - Vector(self._info_width * 2, 0)
        self._resolution = resolution
        pygame.font.init()
        self._font = pygame.font.SysFont('Arial', 30)

    def drawText(surface, text, color, rect, font, aa=False, bkg=None):
        rect = Rect(rect)
        y = rect.top
        lineSpacing = -2

        # get the height of the font
        fontHeight = font.size("Tg")[1]

        while text:
            i = 1

            # determine if the row of text will be outside our area
            if y + fontHeight < rect.bottom:
                break

            # determine maximum width of line
            while font.size(text[:i])[0] < rect.width and i < len(text):
                i += 1

            # if we've wrapped the text, then adjust the wrap to the last word      
            if i < len(text): 
                i = text.rfind(" ", 0, i) + 1

            # render the line and blit it to the surface
            if bkg:
                image = font.render(text[:i], 1, color, bkg)
                image.set_colorkey(bkg)
            else:
                image = font.render(text[:i], aa, color)

            surface.blit(image, (rect.left, y))
            y += fontHeight + lineSpacing

            # remove the text we just blitted
            text = text[i:]

    def processGrayscaleImageEvent(self, event):
        resolution = (event.data()[0].shape[0], event.data()[0].shape[1])
        self._p1_info.camera_surface = pygame.image.frombuffer(event.data()[0], resolution, 'RGB')
        self._p2_info.camera_surface = pygame.image.frombuffer(event.data()[1], resolution, 'RGB')

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
        self._p1_info = Renderer.PlayerInfo()
        self._p2_info = Renderer.PlayerInfo()
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
        pygame.display.update()

    
        
