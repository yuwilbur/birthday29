from ..engine.vector import Vector

class Solid(object):
	def __init__(self):
		self.mass = 1
		self.velocity = Vector()
		self.acceleration = Vector()
		self.material = None
