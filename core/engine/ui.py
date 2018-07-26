#from ..renderer import color
from ..engine.component import Component
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
		self.text = ""
		self.width = 0
		self.height = 0
		self.color = Color.GREEN
		self.font_type = 'Arial'
		self.font_size = 24

	def getSurface(self):
		surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
		pygame.font.init()
		font = pygame.font.SysFont(self.font_type, self.font_size)
		font_height = font.size("Tg")[1]
		y = 0
		text = self.text
		while text:
			i = 1

			# determine if the row of text will be outside our area
			if y + font_height > surface.get_height():
				break

			# determine maximum width of line
			while font.size(text[:i])[0] < surface.get_width() and i < len(text):
				i += 1

			# if we've wrapped the text, then adjust the wrap to the last word      
			if i < len(text): 
				i = text.rfind(" ", 0, i) + 1
			surface.blit(font.render(text[:i], True, self.color), (0, y))
			y += font_height

			# remove the text we just blitted
			text = text[i:]
		return surface