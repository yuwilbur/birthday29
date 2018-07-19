from ..engine.game_engine import GameEngine
from ..engine.vector import Vector
from ..games.yu_game import YuGame
from ..engine.ui import TextBox
from ..engine.solid import Solid
from ..common.event import EventDispatcher
from ..common.events import InputEvent

class TestGame(YuGame):
	DELTA = 10
	def __init__(self, name):
		super(TestGame, self).__init__("TestGame")
		self._engine = GameEngine()

	def setup(self):
		super(TestGame, self).setup()
		event_dispatcher = EventDispatcher()
		event_dispatcher.add_event_listener(InputEvent.TYPE, self.processInputEvent)

		resolution = self._resolution

		self._p1 = self._engine.createRectangle(Vector(25, 200))
		self._p1.position = Vector(-300, 0)
		self._p2 = self._engine.createRectangle(Vector(25, 200))
		self._p2.position = Vector(300, 0)

		self._ball = self._engine.createCircle(50)
		self._ball.getComponent(Solid).velocity = Vector(400,100)

		thickness = 50
		self._engine.createRectangle(Vector(resolution.x, thickness)).position = Vector(0, -resolution.y / 2)
		self._engine.createRectangle(Vector(resolution.x, thickness)).position = Vector(0, resolution.y / 2)
		self._engine.createRectangle(Vector(thickness, resolution.y)).position = Vector(-resolution.x / 2, 0)
		self._engine.createRectangle(Vector(thickness, resolution.y)).position = Vector(resolution.x / 2, 0)

		test = self._engine.createTextBox()
		test.getComponent(TextBox).width = 160
		test.getComponent(TextBox).height = 100
		test.getComponent(TextBox).text = "TEST1 TEST2 TEST3 TEST4 TEST5"
		test.position = Vector(80,50)

	def update(self):
		return

	def stop(self):
		return

	def processInputEvent(self, event):
		if event == InputEvent.W:
			self._p1.position.y -= self.DELTA
			return
		elif event == InputEvent.A:
			return
		elif event == InputEvent.S:
			self._p1.position.y += self.DELTA
			return
		elif event == InputEvent.D:
			return
		elif event == InputEvent.I:
			self._p2.position.y -= self.DELTA
			return
		elif event == InputEvent.J:
			return
		elif event == InputEvent.K:
			self._p2.position.y += self.DELTA
			return
		elif event == InputEvent.L:
			return
		return