from ..common.singleton import Singleton
from ..common.event import EventDispatcher
from ..engine.game_object import GameObject
from ..engine.collider import Collider
from ..engine.primitive import Circle
from ..engine.primitive import Rectangle
from ..engine.solid import Solid
from ..engine.vector import Vector
from ..sync.period_sync import PeriodSync

import copy
import threading

class GameEngine(threading.Thread):
	__metaclass__ = Singleton

	PERIOD = 0.02 # 50Hz

	def __init__(self):
		super(GameEngine, self).__init__()
		self._stop_event = threading.Event()
		self._event_dispatcher = EventDispatcher()
		self._solid_objects = dict()
		self._collider_objects = dict()
		self._game_objects = dict()
		self._lock = threading.Lock()

	def runPhysics(self, solid):
		solid.getComponent(Solid).velocity += solid.getComponent(Solid).acceleration * self.PERIOD
		solid.position += solid.getComponent(Solid).velocity * self.PERIOD

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

	def stop(self):
		self._stop_event.set()

	def run(self):
		period_sync = PeriodSync(self.PERIOD)
		while not self._stop_event.is_set():
			period_sync.Start()
			self._lock.acquire()
			for key in self._solid_objects:
				self.runPhysics(self._solid_objects[key])
			for key_l in self._collider_objects:
				for key_r in self._collider_objects:
					if key_l == key_r:
						break
					self.runCollision(self._collider_objects[key_l], copy.deepcopy(self._collider_objects[key_r]))
			self._lock.release()
			period_sync.End()
			period_sync.Sync()

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
		self._lock.acquire()
		game_object.instanceId = len(self._game_objects)
		self._game_objects[game_object.instanceId] = game_object
		if game_object.hasComponent(Solid):
			self._solid_objects[game_object.instanceId] = game_object
		if game_object.hasComponent(Collider):
			self._collider_objects[game_object.instanceId] = game_object
		self._lock.release()
		return game_object