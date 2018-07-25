from ..common.event import EventDispatcher
from ..common.events import *
from ..games.main_menu_game import MainMenuGame
from ..sync.manager import Manager

class GameManager(Manager):
	def __init__(self):
		super(GameManager, self).__init__()
		self._event_dispatcher = EventDispatcher()
		self._event_dispatcher.add_event_listener(KeyDownEvent.TYPE, self.processKeyDownEvent)
		self._game = None

	def stopGame(self):
		if self._game == None:
			return
		self._game.stop()
		self._game = None

	def startGame(self, game):
		self.stopGame()
		self._game = game
		self._game.setup()

	def processKeyDownEvent(self, event):
		if event.data() == Key.NUM_1:
			self.startGame(MainMenuGame(self._event_dispatcher))

	def setup(self):
		self.startGame(MainMenuGame(self._event_dispatcher))

	def update(self):
		if self._game == None:
			return
		self._game.update()

	def stop(self):
		self.stopGame()