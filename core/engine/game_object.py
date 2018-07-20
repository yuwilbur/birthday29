from ..engine.vector import Vector
from ..engine.game_object_manager import GameObjectManager

class GameObject(object):
	def __init__(self, name):
		self.instance_id = -1
		self.name = name
		self.position = Vector()
		self.rotation = 0
		self._components = dict()
		self._manager = GameObjectManager()
		self._manager.addGameObject(self)

	def addComponent(self, component_type):
		return self._manager.addComponent(self.instance_id, component_type)

	def getComponent(self, component_type):
		return self._manager.getComponent(self.instance_id, component_type)

	def hasComponent(self, component_type):
		return isinstance(self.getComponent(component_type), component_type)