from ..engine.vector import Vector

class Solid(object):
	def __init__(self):
		self.instanceId = 0
		self.velocity = Vector()
		self.acceleration = Vector()
		self.position = Vector()
		self.rotation = 0
		self.friction = 0
