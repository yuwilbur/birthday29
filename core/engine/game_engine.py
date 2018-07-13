from ..sync.period_sync import PeriodSync

import threading

class GameEngine(threading.Thread):
	def __init__(self, event_dispatcher):
		super(GameEngine, self).__init__()
		self._stop_event = threading.Event()
		self._event_dispatcher = event_dispatcher

	def stop(self):
		self._stop_event.set()

	def run(self):
		period_sync = PeriodSync()
		while not self._stop_event.is_set():
			period_sync.Start()
			period_sync.End()
			period_sync.Sync()