from ..engine.game_engine import GameEngine
from ..engine.vector import Vector
from ..games.yu_game import YuGame
from ..engine.ui import TextBox
from ..engine.solid import Solid
from ..engine.primitive import Rectangle
from ..engine.primitive import Circle
from ..engine.material import Material
from ..common.event import EventDispatcher
from ..common.events import InputEvent
from ..engine.game_object import GameObject
from ..engine.collider import Collider
from ..engine.transform import Transform

class TestGame(YuGame):
	DELTA = 10
	def __init__(self, name):
		super(TestGame, self).__init__("TestGame")
		self._engine = GameEngine()

	def setup(self):
		super(TestGame, self).setup() 
		EventDispatcher().add_event_listener(InputEvent.TYPE, self.processInputEvent)

		self._p1 = GameObject("p1")
		self._p1.addComponent(Rectangle)
		self._p1.addComponent(Material)
		self._p1.addComponent(Collider)
		self._p1.getComponent(Transform).position = Vector(-300,0)
		self._p1.getComponent(Rectangle).dimensions = Vector(25, 200)

		self._p2 = GameObject("p2")
		self._p2.addComponent(Rectangle)
		self._p2.addComponent(Material)
		self._p2.addComponent(Collider)
		self._p2.getComponent(Transform).position = Vector(300, 0)
		self._p2.getComponent(Rectangle).dimensions = Vector(25, 200) 

		self._ball = GameObject("ball")
		self._ball.addComponent(Circle)
		self._ball.addComponent(Material)
		self._ball.addComponent(Collider)
		self._ball.getComponent(Circle).radius = 50
		self._ball.getComponent(Solid).velocity = Vector(400, 100)

		resolution = self.getResolution()
		thickness = 50
		self._wall1 = GameObject()
		self._wall1.addComponent(Rectangle)
		self._wall1.addComponent(Material)
		self._wall1.addComponent(Collider)
		self._wall1.getComponent(Transform).position = Vector(0, -resolution.y / 2)
		self._wall1.getComponent(Rectangle).dimensions = Vector(resolution.x, thickness)

		#self._engine.createRectangle(Vector(resolution.x, thickness)).position = Vector(0, -resolution.y / 2)
		#self._engine.createRectangle(Vector(resolution.x, thickness)).position = Vector(0, resolution.y / 2)
		#self._engine.createRectangle(Vector(thickness, resolution.y)).position = Vector(-resolution.x / 2, 0)
		#self._engine.createRectangle(Vector(thickness, resolution.y)).position = Vector(resolution.x / 2, 0)

		#test = self._engine.createTextBox()
		#test.getComponent(TextBox).width = 160
		#test.getComponent(TextBox).height = 100
		#test.getComponent(TextBox).text = "TEST1 TEST2 TEST3 TEST4 TEST5"
		#test.position = Vector(80,50)

	def update(self):
		return

	def stop(self):
		return

	def processInputEvent(self, event):
		if event == InputEvent.W:
			self._p1.getComponent(Transform).position.y -= self.DELTA
			return
		elif event == InputEvent.A:
			return
		elif event == InputEvent.S:
			self._p1.getComponent(Transform).position.y += self.DELTA
			return
		elif event == InputEvent.D:
			return
		elif event == InputEvent.I:
			self._p2.getComponent(Transform).position.y -= self.DELTA
			return
		elif event == InputEvent.J:
			return
		elif event == InputEvent.K:
			self._p2.getComponent(Transform).position.y += self.DELTA
			return
		elif event == InputEvent.L:
			return
		return