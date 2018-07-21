from ..engine.vector import Vector
from ..engine.component import Component

class Transform(Component):
	def __init__(self, game_object):
		self.position = Vector()
		self.rotation = Vector()
