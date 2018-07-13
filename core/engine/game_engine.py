from ..sync.period_sync import PeriodSync
from ..engine.solid import Solid
from ..engine.primitive import Circle
from ..engine.primitive import Rectangle
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

	def stop(self):
		self._stop_event.set()

	def run(self):
		period_sync = PeriodSync(0.02) # 50Hz
		while not self._stop_event.is_set():
			period_sync.Start()
			for solid in self._solid_objects:
				break
			print len(self._solid_objects)
			#print len(self._solids)
			period_sync.End()
			period_sync.Sync()

	def getGameObjects(self):
		return self._game_objects

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