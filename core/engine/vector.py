import math

class Vector(object):
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y

	def toTuple(self):
		return (self.x, self.y)

	def toIntTuple(self):
		return (int(self.x), int(self.y))

	def toIntTupleInvert(self):
		return (int(self.y), int(self.x))

	def toUnitVector(self):
		return self / Vector.Distance(self, Vector())

	def magnitude(self):
		return Vector.Distance(self, Vector())

	def __neg__(self):
		return Vector(-self.x, -self.y)

	def __add__(self, other):
		return Vector(self.x + other.x, self.y + other.y)

	def __sub__(self, other):
		return self + (-other)

	def __mul__(self, other):
		if isinstance(other, (int, float)):
			return Vector(self.x * other, self.y * other)
		elif isinstance(other, Vector):
			return Vector(self.x * other.x, self.y * other.y)

	def __div__(self, other):
		if isinstance(other, (int, float)):
			return Vector(self.x / other, self.y / other)

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y

	@staticmethod
	def DistanceSqu(self, other):
		deltaSqu = self - other
		deltaSqu = deltaSqu * deltaSqu
		return deltaSqu.x + deltaSqu.y

	@staticmethod
	def Distance(self, other):
		return math.sqrt(Vector.DistanceSqu(self, other))

	@staticmethod
	def Dot(self, other):
		return self.x * other.x + self.y * other.y
	
	def __repr__(self):
		return '(' + `self.x` + ', ' + `self.y` + ')'

	@staticmethod
	def Zero():
		return Vector()