from ..engine.vector import Vector

class GameObject(object):
	def __init__(self, name):
		self.instanceId = 0
		self.name = name
		self.position = Vector()
		self.rotation = 0
		self._components = dict()

	def addComponent(self, component):
		self._components[component.__name__] = component()

	def getComponent(self, component):
		return self._components[component.__name__]

	def getComponents(self):
		return self._components