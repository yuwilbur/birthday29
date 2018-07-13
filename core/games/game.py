from ..sync.period_sync import PeriodSync

from abc import abstractmethod
import threading

class Game(threading.Thread):
	def __init__(self, event_dispatcher, name):
		super(Game, self).__init__()
		self._stop_event = threading.Event()
		self._event_dispatcher = event_dispatcher
		self._name = name

	def stop(self):
		self._stop_event.set()

	def run(self):
		self.setup()
		period_sync = PeriodSync()
		while not self._stop_event.is_set():
			period_sync.Start()
			self.update()
			period_sync.End()
			period_sync.Sync()

	@abstractmethod
	def setup(self):
		return

	@abstractmethod
	def update(self):
		return