from ..engine.game_object import GameObject
from ..engine.solid import Solid
from ..engine.vector import Vector

class Rectangle(Solid):
	def __init__(self, game_object):
		super(Rectangle, self).__init__(game_object)
		self.__class__.__name__ = Solid.__name__
		self.dimensions = Vector()

class Circle(Solid):
	def __init__(self, game_object):
		super(Circle, self).__init__(game_object)
		self.__class__.__name__ = Solid.__name__
		self.radius = 0