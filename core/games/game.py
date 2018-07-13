class Game():
	def __init__(self, name):
		self._name = name

	@abstractmethod
	def update(self):
		pass