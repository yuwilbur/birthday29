from ..engine.component import Component
from ..engine.primitive import Solid

class Collider(Component):
	def __init__(self, game_object):
		super(Collider, self).__init__(game_object)
		if not self.getGameObject().hasComponent(Solid):
			raise ValueError("Material component needs a solid.")
		self._on_collision_listener = None

	def setOnCollisionListener(self, listener):
		self._on_collision_listener = listener

	def onCollision(self, game_object):
		if not self._on_collision_listener == None:
			self._on_collision_listener(game_object)
