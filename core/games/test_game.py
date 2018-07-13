from ..engine.game_engine import GameEngine
from ..games.game import Game

class TestGame(Game):
	def __init__(self, event_dispatcher):
		super(TestGame, self).__init__(event_dispatcher, "TestGame")
		self._ball = GameEngine.getInstance().createCircle(1)
		print GameEngine.getInstance().getSolid(self._ball).getRadius()
		self._wall = GameEngine.getInstance().createRectangle((10,10))
		print GameEngine.getInstance().getSolid(self._wall).getDimensions()

	def setup(self):
		return

	def update(self):
		print '1'