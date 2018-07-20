from ..renderer import color
from ..engine.component import Component

class Material(Component):
	def __init__(self, game_object_id):
		super(Material, self).__init__(game_object_id)
		self.color = color.WHITE