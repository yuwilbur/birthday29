from ..common.singleton import Singleton
from ..common.event import EventDispatcher
from ..engine.game_object import GameObject
from ..engine.collider import Collider
from ..engine.primitive import Circle
from ..engine.primitive import Rectangle
from ..engine.solid import Solid
from ..engine.vector import Vector
from ..sync.manager import Manager
from ..sync.period_sync import PeriodSync

import copy

class GameEngine(Manager):
	__metaclass__ = Singleton

	def __init__(self):
		super(GameEngine, self).__init__()
		self._event_dispatcher = EventDispatcher()
		self._solid_objects = dict()
		self._collider_objects = dict()
		self._game_objects = dict()
		
	def runPhysics(self, solid):
		solid.getComponent(Solid).velocity += solid.getComponent(Solid).acceleration * PeriodSync.PERIOD
		solid.position += solid.getComponent(Solid).velocity * PeriodSync.PERIOD

	def runCollision(self, collider, other):
		if isinstance(collider, Rectangle):
			if isinstance(other, Rectangle):
				pass
			elif isinstance(other, Circle):
				pass
		elif isinstance(collider, Circle):
			if isinstance(other, Rectangle):
				pass
			if isinstance(other, Circle):
				pass

	def getSolids(self):
		return self._solid_objects

	def getGameObjects(self):
		return self._game_objects

	def createCircle(self, radius, collides=True):
		circle = GameObject("Circle")
		circle.addComponent(Circle).radius = radius
		if collides:
			circle.addComponent(Collider)
		return self.addGameObject(circle)

	def createRectangle(self, dimensions, collides=True):
		rectangle = GameObject("Rectangle")
		rectangle.addComponent(Rectangle).dimensions = dimensions
		if collides:
			rectangle.addComponent(Collider)
		return self.addGameObject(rectangle)

	def addGameObject(self, game_object):
		game_object.instanceId = len(self._game_objects)
		self._game_objects[game_object.instanceId] = game_object
		if game_object.hasComponent(Solid):
			self._solid_objects[game_object.instanceId] = game_object
		if game_object.hasComponent(Collider):
			self._collider_objects[game_object.instanceId] = game_object
		return game_object

	def update(self):
		for key in self._solid_objects:
				self.runPhysics(self._solid_objects[key])
		for key_l in self._collider_objects:
			for key_r in self._collider_objects:
				if key_l == key_r:
					break
				self.runCollision(self._collider_objects[key_l], copy.deepcopy(self._collider_objects[key_r]))