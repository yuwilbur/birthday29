from ..engine.game_object_manager import GameObjectManager

class Component(object):
	def __init__(self, game_object_id):
		self._game_object = GameObjectManager().getGameObject(game_object_id)

	def getGameObject(self):
		return self._game_object