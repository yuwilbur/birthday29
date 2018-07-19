from ..sync.period_sync import PeriodSync

from abc import abstractmethod
import threading

class Game(object):
	def __init__(self, name):
		self._name = name
		self._info_width = 160
		self._camera_height = 160
		self._controls_height = 160
		self._text_height = 200
	
	@abstractmethod
	def setup(self):
		return

	@abstractmethod
	def update(self):
		return

	@abstractmethod
	def stop(self):
		return