from ..common.singleton import Singleton

class GameObjectManager(object):
	__metaclass__ = Singleton
	
	def __init__(self):
		self._game_objects = dict()
		self._components = dict()
		self._unique_id = 0

	def addGameObject(self, game_object):
		if game_object.instance_id == -1:
			game_object.instance_id = self._unique_id
			self._unique_id += 1
		self._game_objects[game_object] = game_object

	def addComponent(self, game_object, component_type):
		component = component_type(game_object)
		if not game_object in self._game_objects:
			raise ValueError('GameObject has not been constructed yet.')
		component_id = component_type.__name__
		if not component_id in self._components:
			self._components[component_id] = dict()
		self._components[component_id][game_object] = component
		return self.getComponent(game_object, component_type)

	def getComponents(self, component_type):
		component_id = component_type.__name__
		if not component_id in self._components:
			return None
		return self._components[component_id]

	def getComponent(self, game_object, component_type):
		if not game_object in self._game_objects:
			raise ValueError('GameObject has not been constructed yet.')
		component_id = component_type.__name__
		if not component_id in self._components or not game_object in self._components[component_id]:
			return None
		return self._components[component_id][game_object]
