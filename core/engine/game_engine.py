from ..common.singleton import Singleton
from ..common.event import EventDispatcher
from ..engine.game_object import GameObject
from ..engine.collider import Collider
from ..engine.primitive import Circle
from ..engine.primitive import Rectangle
from ..engine.solid import Solid
from ..engine.ui import TextBox
from ..engine.ui import UI
from ..engine.vector import Vector
from ..sync.manager import Manager
from ..sync.period_sync import PeriodSync
from ..engine.material import Material
from ..engine.game_object_manager import GameObjectManager

import copy
import math

class GameEngine(Manager):
	__metaclass__ = Singleton

	def __init__(self):
		super(GameEngine, self).__init__()
		self._game_object_manager = GameObjectManager()
		
	def runPhysics(self, solid):
		solid.getComponent(Solid).velocity += solid.getComponent(Solid).acceleration * PeriodSync.PERIOD
		solid.position += solid.getComponent(Solid).velocity * PeriodSync.PERIOD

	def runCircleCircleCollision(self, collider, reference):
		x1 = collider.position
		m1 = collider.getComponent(Solid).mass
		v1 = collider.getComponent(Solid).velocity
		s1 = collider.getComponent(Circle).radius
		x2 = reference.position
		m2 = reference.getComponent(Solid).mass
		v2 = reference.getComponent(Solid).velocity
		s2 = reference.getComponent(Circle).radius
		if (Vector.DistanceSqu(x1, x2) > math.pow(s1 + s2, 2)):
			return
		velocity = v1 - (x1 - x2) * (2 * m2 / (m1 + m1) * Vector.Dot(v1 - v2, x1 - x2) / Vector.DistanceSqu(x2, x1))
		collider.getComponent(Solid).velocity = velocity

	def runCircleRectangleCollision(self, collider, reference):
		x1 = collider.position
		m1 = collider.getComponent(Solid).mass
		v1 = collider.getComponent(Solid).velocity
		s1 = collider.getComponent(Circle).radius
		x2 = reference.position
		m2 = reference.getComponent(Solid).mass
		v2 = reference.getComponent(Solid).velocity
		s2 = reference.getComponent(Rectangle).dimensions
		if x1.x <= x2.x + s2.x / 2 and x1.x >= x2.x - s2.x / 2:
			if (not (math.fabs(x1.y - x2.y) < s1 + s2.y / 2) or
				not (v1.y * (x2.y - x1.y) >= 0)):
				return
		elif x1.y <= x2.y + s2.y / 2 and x1.y >= x2.y - s2.y / 2:
			if (not (math.fabs(x1.x - x2.x) < s1 + s2.x / 2) or
				not (v1.x * (x2.x - x1.x) >= 0)):
				return
		else:
			corners = [
				x2 + Vector(s2.x, s2.y) / 2,
				x2 + Vector(-s2.x, s2.y) / 2,
				x2 + Vector(s2.x, -s2.y) / 2,
				x2 + Vector(-s2.x, -s2.y) / 2
			]
			closest_corner = corners[0]
			if Vector.DistanceSqu(x1, corners[1]) < Vector.DistanceSqu(x1, closest_corner):
				closest_corner = corners[1]
			if Vector.DistanceSqu(x1, corners[2]) < Vector.DistanceSqu(x1, closest_corner):
				closest_corner = corners[2]
			if Vector.DistanceSqu(x1, corners[3]) < Vector.DistanceSqu(x1, closest_corner):
				closest_corner = corners[3]
			circle_radius_squ = math.pow(s1, 2)
			if (not Vector.DistanceSqu(x1, closest_corner) <= circle_radius_squ or
				not Vector.Dot(v1, closest_corner - x1) >= 0):
				return
		if (x1.x >= x2.x - s2.x / 2 and x1.x <= x2.x + s2.x / 2):
			collider.getComponent(Solid).velocity = Vector(v1.x, -v1.y)
		elif (x1.y >= x2.y - s2.y / 2 and x1.y <= x2.y + s2.y / 2):
			collider.getComponent(Solid).velocity = Vector(-v1.x, v1.y)
		else:
			collider.getComponent(Solid).velocity = -Vector(v1.y, v1.x)

	def getObjectsWithType(self, component_type):
		return GameObjectManager().getComponents(component_type)

	def update(self):
		pass
		# collider_objects = GameObjectManager().getComponents(Collider)
		# for (key, value) in collider_objects:
		# 	self.runPhysics(value)
		# reference_objects = copy.deepcopy(collider_objects)
		# for (collider_key, collider) in collider_objects.items():
		# 	for (reference_key, reference) in reference_objects.items():
		# 		if collider_key == reference_key:
		# 			continue
		# 		if collider.hasComponent(Circle):
		# 			if reference.hasComponent(Circle):
		# 				self.runCircleCircleCollision(collider, reference)
		# 			if reference.hasComponent(Rectangle):
		# 				self.runCircleRectangleCollision(collider, reference)