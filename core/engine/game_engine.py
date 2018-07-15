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
import math

class GameEngine(Manager):
	__metaclass__ = Singleton

	def __init__(self):
		super(GameEngine, self).__init__()
		self._event_dispatcher = EventDispatcher()
		self._solid_objects = dict()
		self._collider_objects = dict()
		self._game_object_instance_id = 0
		
	def runPhysics(self, solid):
		solid.getComponent(Solid).velocity += solid.getComponent(Solid).acceleration * PeriodSync.PERIOD
		solid.position += solid.getComponent(Solid).velocity * PeriodSync.PERIOD

	def isColliding(self, collider, reference):
		if collider.hasComponent(Circle):
			if reference.hasComponent(Circle):
				minDistanceSqu = collider.getComponent(Circle).radius + reference.getComponent(Circle).radius
				minDistanceSqu *= minDistanceSqu
				distanceSqu = Vector.DistanceSqu(collider.position, reference.position)
				return distanceSqu <= minDistanceSqu
		return False

	def runCollision(self, collider, reference):
		if collider.hasComponent(Circle):
			if reference.hasComponent(Circle):
				x1 = collider.position
				m1 = collider.getComponent(Solid).mass
				v1 = collider.getComponent(Solid).velocity
				x2 = reference.position
				m2 = reference.getComponent(Solid).mass
				v2 = reference.getComponent(Solid).velocity
				velocity = v1 - (x1 - x2) * (2 * m2 / (m1 + m1) * Vector.Dot(v1 - v2, x1 - x2) / Vector.DistanceSqu(x2, x1))
				collider.getComponent(Solid).velocity = velocity

	def getSolids(self):
		return self._solid_objects

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
		game_object.instance_id = self._game_object_instance_id
		self._game_object_instance_id += 1
		if game_object.hasComponent(Solid):
			self._solid_objects[game_object.instance_id] = game_object
		if game_object.hasComponent(Collider):
			self._collider_objects[game_object.instance_id] = game_object
		return game_object

	def update(self):
		for key in self._solid_objects:
				self.runPhysics(self._solid_objects[key])
		reference_objects = copy.deepcopy(self._collider_objects)
		for collider in self._collider_objects:
			for reference in reference_objects:
				if collider == reference:
					continue
				if self.isColliding(self._collider_objects[collider], reference_objects[reference]):
					self.runCollision(self._collider_objects[collider], reference_objects[reference])