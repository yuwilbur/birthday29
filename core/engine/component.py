from ..engine.game_object_manager import GameObjectManager

class Component(object):
	def __init__(self, game_object):
		self._game_object = game_object

	def getGameObject(self):
		return self._game_object

	def addComponent(self, component_type):
		return self.getGameObject().addComponent(component_type)

	def getComponent(self, component_type):
		return self.getGameObject().getComponent(component_type)

	def hasComponent(self, component_type):
		return isinstance(self.getGameObject().getComponent(component_type), component_type)