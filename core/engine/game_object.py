from ..engine.vector import Vector

class GameObject(object):
	def __init__(self, name):
		self.instance_id = 0
		self.name = name
		self.position = Vector()
		self.rotation = 0
		self._components = dict()

	def addComponent(self, component_type):
		self._components[component_type.__name__] = component_type()
		return self.getComponent(component_type)

	def getComponent(self, component_type):
		return self._components[component_type.__name__]

	def hasComponent(self, component_type):
		return isinstance(self.getComponent(component_type), component_type)