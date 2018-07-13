from ..engine.solid import Solid

class Rectangle(Solid):
	def __init__(self, dimensions):
		super(Rectangle, self).__init__("Rectangle")
		self._dimensions = dimensions

	def getDimensions(self):
		return self._dimensions

class Circle(Solid):
	def __init__(self, radius):
		super(Circle, self).__init__("Circle")
		self._radius = radius

	def getRadius(self):
		return self._radius