class Color(object):
	def __init__(self, rgb = (0, 0, 0)):
		self._r = rgb[0]
		self._g = rgb[1]
		self._b = rgb[2]

	def toTuple(self):
		return (self._r, self._g, self._b)

WHITE = Color((255,255,255))
BLACK = Color((0,0,0))