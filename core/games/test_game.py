from ..engine.game_engine import GameEngine
from ..engine.vector import Vector
from ..games.game import Game
from ..engine.solid import Solid

class TestGame(Game):
	def __init__(self, event_dispatcher):
		super(TestGame, self).__init__(event_dispatcher, "TestGame")
		self._engine = GameEngine()

	def setup(self):
		self._ball = self._engine.createCircle(100)
		self._ball.getComponent(Solid).velocity = Vector(100,0)
		self._ball.position = Vector(-300,0)
		#self._wall = self._engine.createRectangle((200,100))
		#self._wall.position = Vector(100,100)
		self._ball2 = self._engine.createCircle(100)
		self._ball2.getComponent(Solid).velocity = Vector(-100, 0)
		self._ball2.position = Vector(300, 0)

	def update(self):
		#print '1'
		return