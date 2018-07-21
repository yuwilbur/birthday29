from ..engine.component import Component
from ..engine.primitive import Solid

class Collider(Component):
	def __init__(self, game_object_id):
		super(Collider, self).__init__(game_object_id)
		if not self.getGameObject().hasComponent(Solid):
			raise ValueError("Material component needs a solid.")