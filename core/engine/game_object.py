from ..engine.vector import Vector
from ..engine.game_object_manager import GameObjectManager

class GameObject(object):
	def __new__(cls):
		self = super(GameObject, cls).__new__(cls)
		self.instance_id = -1
		self.position = Vector()
		self.rotation = 0
		GameObjectManager().addGameObject(self)
		return self

	def __hash__(self):
		return self.instance_id

	def __eq__(self, other):
		return self.instance_id == other.instance_id

	def addComponent(self, component_type):
		return GameObjectManager().addComponent(self, component_type)

	def getComponent(self, component_type):
		return GameObjectManager().getComponent(self, component_type)

	def hasComponent(self, component_type):
		return isinstance(self.getComponent(component_type), component_type)