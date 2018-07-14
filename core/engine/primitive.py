from ..engine.game_object import GameObject
from ..engine.solid import Solid

class Rectangle(GameObject):
	def __init__(self, dimensions):
		super(Rectangle, self).__init__("Rectangle")
		self.addComponent(Solid)
		self._dimensions = dimensions

	def getDimensions(self):
		return self._dimensions

class Circle(GameObject):
	def __init__(self, radius):
		super(Circle, self).__init__("Circle")
		self.addComponent(Solid)
		self._radius = radius

	def getRadius(self):
		return self._radius