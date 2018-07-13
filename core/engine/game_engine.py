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
		self._solids = dict()

	def stop(self):
		self._stop_event.set()

	def run(self):
		period_sync = PeriodSync()
		while not self._stop_event.is_set():
			period_sync.Start()
			period_sync.End()
			period_sync.Sync()

	def createCircle(self, radius):
		return self.createSolid(Circle(radius))

	def getSolid(self, solid):
		return self._solids[solid]

	def createRectangle(self, dimensions):
		return self.createSolid(Rectangle(dimensions))

	def createSolid(self, solid):
		solid_id = len(self._solids)
		solid.instanceId = solid_id
		self._solids[solid_id] = solid
		return (solid_id, solid)