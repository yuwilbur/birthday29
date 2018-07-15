from ..engine.vector import Vector
from ..engine.material import Material

class Solid(object):
	def __init__(self):
		self.mass = 1
		self.velocity = Vector()
		self.acceleration = Vector()
