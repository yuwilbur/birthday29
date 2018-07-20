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
		self._game_objects[game_object.instance_id] = game_object

	def getGameObject(self, game_object_id):
		if game_object_id in self._game_objects:
			return self._game_objects[game_object_id]
		return None

	def addComponent(self, game_object_id, component_type):
		component = component_type(game_object_id)
		if not game_object_id in self._game_objects:
			raise ValueError('GameObject has not been constructed yet.')
		component_id = component_type.__name__
		if not component_id in self._components:
			self._components[component_id] = dict()
		self._components[component_id][game_object_id] = component
		# print '1', component_id, ' ', type(self._components[component_id])
		return self.getComponent(game_object_id, component_type)

	def getComponents(self, component_type):
		component_id = component_type.__name__
		if not component_id in self._components:
			return None
		return self._components[component_id]

	def getComponent(self, game_object_id, component_type):
		if not game_object_id in self._game_objects:
			raise ValueError('GameObject has not been constructed yet.')
		component_id = component_type.__name__
		if not component_id in self._components or not game_object_id in self._components[component_id]:
			return None
		#print '2', component_id, ' ', type(self._components[component_id])
		return self._components[component_id][game_object_id]
