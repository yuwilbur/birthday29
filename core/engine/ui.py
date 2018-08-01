#from ..renderer import color
from ..engine.component import Component
from ..engine.align import Align
from ..renderer.color import Color

from abc import abstractmethod
import pygame

class UI(Component):
	def __init__(self, game_object):
		super(UI, self).__init__(game_object)

	@abstractmethod
	def getSurface(self):
		pass

class Image(UI):
	def __init__(self, game_object):
		super(Image, self).__init__(game_object)
		self.__class__.__name__ = UI.__name__
		self._surface = None

	def fromNumpy(self, data):
		self._surface = pygame.image.frombuffer(data, data.shape[0:2], 'RGB')

	def getSurface(self):
		return self._surface

class TextBox(UI):
	def __init__(self, game_object):
		super(TextBox, self).__init__(game_object)
		self.__class__.__name__ = UI.__name__
		self.width = 0
		self.height = 0
		self.color = Color.GREEN
		self.font_type = 'Arial'
		self.font_size = 24
		self.align = Align.RIGHT
		self.surface = None
		pygame.font.init()

	def setTexts(self, texts):
		self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
		font = pygame.font.SysFont(self.font_type, self.font_size)
		font_height = font.size("Tg")[1]
		y_position = 0
		for text in texts:
			while text:
				if y_position + font_height > self.surface.get_height():
					break

				i = 1
				while i < len(text):
					if font.size(text[:i])[0] > self.surface.get_width():
						i = text.rfind(" ", 0, i) + 1
						break
					i += 1

				render_text = text[:i]
				render_text_length = font.size(render_text)[0]
				x_position = 0
				if self.align == Align.RIGHT:
					x_position = 0
				elif self.align == Align.LEFT:
					x_position = self.width - render_text_length
				elif self.align == Align.CENTER:
					x_position = (self.width - render_text_length) / 2

				self.surface.blit(font.render(render_text, True, self.color), (x_position, y_position))
				y_position += font_height
				text = text[i:]

	def getSurface(self):
		return self.surface