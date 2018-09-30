from ..engine.component import Component
from ..renderer.color import Color
from ..engine.vector import Vector

class GradientCircle(Component):
	def __init__(self, game_object):
		super(GradientCircle, self).__init__(game_object)
		self.start_color = Color.WHITE
		self.end_color = Color.BLACK
		self.step = 2
		self.thickness = 20
		self.radius = 100
		self.offset = Vector()
