from ..engine.game_object_manager import GameObjectManager

class Component(object):
	def __init__(self, game_object_id):
		self._game_object_id = game_object_id
		self._game_object_manager = GameObjectManager()

	def getGameObject(self):
		return self._game_object_manager.getGameObject(self._game_object_id)