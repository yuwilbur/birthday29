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
from ..engine.material import Material

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

	def runCircleCircleCollision(self, collider, reference):
		min_distance_squ = math.pow(collider.getComponent(Circle).radius + reference.getComponent(Circle).radius, 2)
		distance_squ = Vector.DistanceSqu(collider.position, reference.position)
		if (distance_squ > min_distance_squ):
			return
		x1 = collider.position
		m1 = collider.getComponent(Solid).mass
		v1 = collider.getComponent(Solid).velocity
		x2 = reference.position
		m2 = reference.getComponent(Solid).mass
		v2 = reference.getComponent(Solid).velocity
		velocity = v1 - (x1 - x2) * (2 * m2 / (m1 + m1) * Vector.Dot(v1 - v2, x1 - x2) / Vector.DistanceSqu(x2, x1))
		collider.getComponent(Solid).velocity = velocity

	def runCircleRectangleCollision(self, collider, reference):
		circle = collider.getComponent(Circle)
		rectangle = reference.getComponent(Rectangle)
		rectangle_topright = reference.position + (rectangle.dimensions / 2)
		rectangle_botleft = reference.position - (rectangle.dimensions / 2)
		if collider.position.x <= rectangle_topright.x and collider.position.x >= rectangle_botleft.x:
			if not (math.fabs(collider.position.y - reference.position.y) < circle.radius + rectangle.dimensions.y / 2):
				return
		elif collider.position.y <= rectangle_topright.y and collider.position.y >= rectangle_botleft.y:
			if not (math.fabs(collider.position.x - reference.position.x) < circle.radius + rectangle.dimensions.x / 2):
				return
		else:
			circle_radius_squ = math.pow(circle.radius, 2)
			if not (Vector.DistanceSqu(collider.position, Vector(rectangle_botleft.x, rectangle_botleft.y)) <= circle_radius_squ or
				Vector.DistanceSqu(collider.position, Vector(rectangle_botleft.x, rectangle_topright.y)) <= circle_radius_squ or
				Vector.DistanceSqu(collider.position, Vector(rectangle_topright.x, rectangle_botleft.y)) <= circle_radius_squ or
				Vector.DistanceSqu(collider.position,Vector(rectangle_topright.x, rectangle_topright.y)) <= circle_radius_squ):
				return
		x1 = collider.position
		m1 = collider.getComponent(Solid).mass
		v1 = collider.getComponent(Solid).velocity
		x2 = reference.position
		m2 = reference.getComponent(Solid).mass
		v2 = reference.getComponent(Solid).velocity
		d2 = reference.getComponent(Rectangle).dimensions
		if (x1.x >= x2.x - d2.x / 2 and x1.x <= x2.x + d2.x / 2):
			collider.getComponent(Solid).velocity = Vector(v1.x, -v1.y)
		elif (x1.y >= x2.y - d2.y / 2 and x1.y <= x2.y + d2.y / 2):
			collider.getComponent(Solid).velocity = Vector(-v1.x, v1.y)
		else:
			collider.getComponent(Solid).velocity = -Vector(v1.y, v1.x)

	def getSolids(self):
		return self._solid_objects

	def createCircle(self, radius, collides=True):
		circle = GameObject("Circle")
		circle.addComponent(Circle).radius = radius
		if collides:
			circle.addComponent(Collider)
		circle.addComponent(Material)
		return self.addGameObject(circle)

	def createRectangle(self, dimensions, collides=True):
		rectangle = GameObject("Rectangle")
		rectangle.addComponent(Rectangle).dimensions = dimensions
		if collides:
			rectangle.addComponent(Collider)
		rectangle.addComponent(Material)
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
		for (collider_key, collider) in self._collider_objects.items():
			for (reference_key, reference) in reference_objects.items():
				if collider_key == reference_key:
					continue
				if collider.hasComponent(Circle):
					if reference.hasComponent(Circle):
						self.runCircleCircleCollision(collider, reference)
					if reference.hasComponent(Rectangle):
						self.runCircleRectangleCollision(collider, reference)
				#if self.isColliding(collider, reference):
				#	self.runCollision(collider, reference)