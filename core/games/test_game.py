from ..engine.game_engine import GameEngine
from ..games.game import Game

class TestGame(Game):
	def __init__(self, event_dispatcher):
		super(TestGame, self).__init__(event_dispatcher, "TestGame")
		self._engine = GameEngine.getInstance()

	def setup(self):
		self._ball = self._engine.createCircle(100)
		self._wall = self._engine.createRectangle((200,100))

	def update(self):
		#print '1'
		return