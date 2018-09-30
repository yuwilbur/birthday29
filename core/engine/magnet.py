from ..engine.vector import Vector
from ..engine.component import Component

class Magnet(Component):
	def __init__(self, game_object):
		super(Magnet, self).__init__(game_object)
		self.offset = Vector()
