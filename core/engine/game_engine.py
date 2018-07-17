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

	def isColliding(self, collider, reference):
		def isCircleCircleColliding(circle1, circle2):
			minDistanceSqu = math.pow(circle1.getComponent(Circle).radius + circle2.getComponent(Circle).radius, 2)
			distanceSqu = Vector.DistanceSqu(circle1.position, circle2.position)
			return distanceSqu <= minDistanceSqu

		def isCircleRectangleColliding(circle, rectangle):
			circle_comp = circle.getComponent(Circle)
			rectangle_comp = rectangle.getComponent(Rectangle)
			rectangle_topright = rectangle.position + (rectangle_comp.dimensions / 2)
			rectangle_botleft = rectangle.position - (rectangle_comp.dimensions / 2)
			if circle.position.x <= rectangle_topright.x and circle.position.x >= rectangle_botleft.x:
				return math.pow(circle.position.y - rectangle.position.y, 2) < math.pow(circle_comp.radius + rectangle_comp.dimensions.y / 2, 2)
			elif circle.position.y <= rectangle_topright.y and circle.position.y >= rectangle_botleft.y:
				return math.pow(circle.position.x - rectangle.position.x, 2) < math.pow(circle_comp.radius + rectangle_comp.dimensions.x / 2, 2)
			else:
				circle_radius_squ = math.pow(circle.getComponent(Circle).radius, 2)
				return (Vector.DistanceSqu(circle.position, rectangle_botleft + Vector(0,0)) <= circle_radius_squ or
					Vector.DistanceSqu(circle.position, rectangle_botleft + Vector(0, rectangle_comp.dimensions.y)) <= circle_radius_squ or
					Vector.DistanceSqu(circle.position, rectangle_botleft + Vector(rectangle_comp.dimensions.x, 0)) <= circle_radius_squ or
					Vector.DistanceSqu(circle.position, rectangle_botleft + rectangle_comp.dimensions) <= circle_radius_squ)

		if collider.hasComponent(Circle):
			if reference.hasComponent(Circle):
				return isCircleCircleColliding(collider, reference)
			if reference.hasComponent(Rectangle):
				return isCircleRectangleColliding(collider, reference)
		if collider.hasComponent(Rectangle):
			if reference.hasComponent(Rectangle):
				return False
			if reference.hasComponent(Circle):
				return isCircleRectangleColliding(reference, collider)
		return False

	def runCollision(self, collider, reference):
		def runCircleCircleCollision(circle1, circle2):
			x1 = circle1.position
			m1 = circle1.getComponent(Solid).mass
			v1 = circle1.getComponent(Solid).velocity
			x2 = circle2.position
			m2 = circle2.getComponent(Solid).mass
			v2 = circle2.getComponent(Solid).velocity
			velocity = v1 - (x1 - x2) * (2 * m2 / (m1 + m1) * Vector.Dot(v1 - v2, x1 - x2) / Vector.DistanceSqu(x2, x1))
			collider.getComponent(Solid).velocity = velocity

		def runCircleRectangleCollision(circle, rectangle):
			x1 = circle.position
			m1 = circle.getComponent(Solid).mass
			v1 = circle.getComponent(Solid).velocity
			x2 = rectangle.position
			m2 = rectangle.getComponent(Solid).mass
			v2 = rectangle.getComponent(Solid).velocity
			d2 = rectangle.getComponent(Rectangle).dimensions
			if (x1.x >= x2.x - d2.x / 2 and x1.x <= x2.x + d2.x / 2):
				print 'go up / down'
				circle.getComponent(Solid).velocity = Vector(v1.x, -v1.y)
			elif (x1.y >= x2.y - d2.y / 2 and x1.y <= x2.y + d2.y / 2):
				print 'go left / right'
				circle.getComponent(Solid).velocity = Vector(-v1.x, v1.y)

		if collider.hasComponent(Circle):
			if reference.hasComponent(Circle):
				runCircleCircleCollision(collider, reference)
			elif reference.hasComponent(Rectangle):
				runCircleRectangleCollision(collider, reference)
		if collider.hasComponent(Rectangle):
			if reference.hasComponent(Rectangle):
				return
			if reference.hasComponent(Circle):
				return

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
		for collider in self._collider_objects:
			for reference in reference_objects:
				if collider == reference:
					continue
				if self.isColliding(self._collider_objects[collider], reference_objects[reference]):
					self.runCollision(self._collider_objects[collider], reference_objects[reference])