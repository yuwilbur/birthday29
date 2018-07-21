from ..engine.vector import Vector
from ..engine.component import Component

class Solid(Component):
	def __init__(self, game_object):
		super(Solid, self).__init__(game_object)
		self.mass = 1
		self.velocity = Vector()
		self.acceleration = Vector()
