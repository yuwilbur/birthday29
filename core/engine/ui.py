from ..renderer import color

from abc import abstractmethod
import pygame

class UI(object):
	@abstractmethod
	def getSurface(self):
		pass

class TextBox(UI):
	def __init__(self):
		super(TextBox, self).__init__()
		self.__class__.__name__ = UI.__name__
		self.text = ""
		self.width = 0
		self.height = 0
		self.color = color.RED
		self.font_type = 'Arial'
		self.font_size = 30

	def createSurface(self):
		surface = pygame.Surface((self.width, self.height))
		lineSpacing = -2
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

			surface.blit(font.render(text[:i], True, self.color.toTuple()), (0, y))
			y += font_height + lineSpacing

			# remove the text we just blitted
			text = text[i:]
		return surface

	def getSurface(self):
		return self.createSurface()