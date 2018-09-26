from ..engine.component import Component
from ..engine.game_object_manager import GameObjectManager
from ..renderer.color import Color
from ..engine.vector import Vector

class Line(Component):
	def __init__(self, game_object):
		super(Line, self).__init__(game_object)
		self.start = Vector()
		self.end = Vector()
		self.color = Color.WHITE
