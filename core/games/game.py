from ..sync.period_sync import PeriodSync

from abc import abstractmethod

class Game(object):
	def __init__(self, name):
		self._name = name
	
	@abstractmethod
	def setup(self):
		return

	@abstractmethod
	def update(self):
		return

	@abstractmethod
	def stop(self):
		return