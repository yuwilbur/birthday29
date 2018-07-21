from ..renderer import color
from ..engine.primitive import Solid
from ..engine.component import Component
from ..engine.game_object_manager import GameObjectManager

class Material(Component):
	def __init__(self, game_object):
		super(Material, self).__init__(game_object)
		if not self.getGameObject().hasComponent(Solid):
			raise ValueError("Material component needs a solid.")
		self.color = color.WHITE