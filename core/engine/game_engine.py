from ..sync.period_sync import PeriodSync
from ..engine.solid import Solid
from ..engine.primitive import Circle
from ..engine.primitive import Rectangle
from ..engine.vector import Vector

import copy
import threading

class GameEngine(threading.Thread):
	__instance = None

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
		self._game_objects = dict()
		self._solid_objects = dict()

	def checkPhysics(self, solid_l, solid_r):
		if not solid_l.velocity == Vector.Zero() or not solid_l.acceleration == Vector.Zero():
			return True
		if not solid_l.hasCollider:
			return False
		return False

	def runPhysics(self, solid_l, solid_r):
		old_solid_l = copy.deepcopy(solid_l)
		solid_l.position = solid_l.position + solid_l.velocity
		if isinstance(solid_l, Rectangle):
			if isinstance(solid_r, Rectangle):
				pass
			elif isinstance(solid_r, Circle):
				pass
		elif isinstance(solid_l, Circle):
			if isinstance(solid_r, Rectangle):
				pass
			if isinstance(solid_r, Circle):
				pass

	def stop(self):
		self._stop_event.set()

	def run(self):
		period_sync = PeriodSync(0.02) # 50Hz
		while not self._stop_event.is_set():
			period_sync.Start()
			solid_objects = copy.deepcopy(self._solid_objects)	
			for key_l in solid_objects:
				for key_r in solid_objects:
					if self.checkPhysics(solid_objects[key_l], solid_objects[key_r]):
						self.runPhysics(self._solid_objects[key_l], self._solid_objects[key_r])
			period_sync.End()
			period_sync.Sync()

	def getGameObjects(self):
		return self._game_objects

	def getSolids(self):
		return self._solid_objects

	def createCircle(self, radius):
		return self.addGameObject(Circle(radius))

	def createRectangle(self, dimensions):
		return self.addGameObject(Rectangle(dimensions))

	def addGameObject(self, game_object):
		game_object_id = len(self._game_objects)
		game_object.instanceId = game_object_id
		self._game_objects[game_object_id] = game_object
		if (isinstance(game_object, Solid)):
			self._solid_objects[game_object_id] = game_object
		return game_object