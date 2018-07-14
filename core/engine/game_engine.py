from ..sync.period_sync import PeriodSync
from ..engine.game_object import GameObject
from ..engine.collider import Collider
from ..engine.primitive import Circle
from ..engine.primitive import Rectangle
from ..engine.solid import Solid
from ..engine.vector import Vector

import copy
import threading

class GameEngine(threading.Thread):
	__instance = None
	PERIOD = 0.02 # 50Hz

	@staticmethod
	def getInstance():
		return GameEngine.__instance

	def __init__(self, event_dispatcher):
		if GameEngine.__instance != None:
			raise Exception("This class is a singleton")
		GameEngine.__instance = self

		super(GameEngine, self).__init__()
		self._stop_event = threading.Event()
		self._event_dispatcher = event_dispatcher
		self._solid_objects = dict()
		self._collider_objects = dict()
		self._game_objects = dict()

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
			for key in self._solid_objects:
				self.runPhysics(self._solid_objects[key])
			for key_l in self._collider_objects:
				for key_r in self._collider_objects:
					if key_l == key_r:
						break
					self.runCollision(self._collider_objects[key_l], copy.deepcopy(self._collider_objects[key_r]))
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
		game_object.instanceId = len(self._game_objects)
		self._game_objects[game_object.instanceId] = game_object
		for component in game_object.getComponents():
			if component == Solid.__name__:
				self._solid_objects[game_object.instanceId] = game_object
			if component == Collider.__name__:
				self._collider_objects[game_object.instanceId] = game_object
		return game_object