from ..common.events import InputEvent
from ..games.test_game import TestGame

class GameManager():
	def __init__(self, event_dispatcher):
		self._event_dispatcher = event_dispatcher
		self._event_dispatcher.add_event_listener(InputEvent.TYPE, self.processInputEvent)
		self._game = None

	def stopGame(self):
		if not self._game == None:
			self._game.stop()
			self._game.join()

	def startGame(self, game):
		self.stopGame()
		self._game = game
		self._game.setDaemon(True)
		self._game.start()

	def processInputEvent(self, event):
		if event == InputEvent.ONE:
			self.startGame(TestGame(self._event_dispatcher))