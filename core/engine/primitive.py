from ..engine.game_object import GameObject
from ..engine.solid import Solid
from ..engine.vector import Vector

class Rectangle(Solid):
	def __init__(self):
		super(Rectangle, self).__init__()
		self.__class__.__name__ = Solid.__name__
		self.dimensions = Vector()

class Circle(Solid):
	def __init__(self):
		super(Circle, self).__init__()
		self.__class__.__name__ = Solid.__name__
		self._radius = 0