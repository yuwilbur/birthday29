from ..engine.vector import Vector

class Solid(object):
	def __init__(self):
		self.mass = 0
		self.velocity = Vector()
		self.acceleration = Vector()
		self.material = None
