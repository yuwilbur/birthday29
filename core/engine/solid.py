from ..engine.game_object import GameObject
from ..engine.vector import Vector

class Solid(GameObject):
	def __init__(self, name):
		super(Solid, self).__init__(name)
		self.mass = 0
		self.velocity = Vector()
		self.acceleration = Vector()
		self.position = Vector()
		self.rotation = 0
		self.hasCollider = False
		self.material = None
