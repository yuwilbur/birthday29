from ..engine.game_engine import GameEngine
from ..games.game import Game

class TestGame(Game):
	def __init__(self, event_dispatcher):
		super(TestGame, self).__init__(event_dispatcher, "TestGame")
		self._engine = GameEngine.getInstance()

	def setup(self):
		asd, self._ball = self._engine.createCircle(1)
		self._ball.velocity = 123123
		print self._engine.getSolid(asd).velocity
		#self._wall = self._engine.createRectangle((10,10))
		#print self._engine.getSolid(self._wall).getDimensions()

	def update(self):
		print '1'