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
		return False

	def runPhysics(self, solid_l, solid_r):
		print solid_l.name
		solid_l.position = Vector(400,400)

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
		return self.createGameObject(Circle(radius))

	def createRectangle(self, dimensions):
		return self.createGameObject(Rectangle(dimensions))

	def createGameObject(self, game_object):
		game_object_id = len(self._game_objects)
		game_object.instanceId = game_object_id
		self._game_objects[game_object_id] = game_object
		if (isinstance(game_object, Solid)):
			self._solid_objects[game_object_id] = game_object
		return game_object