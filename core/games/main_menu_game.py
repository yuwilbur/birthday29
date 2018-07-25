from ..engine.game_engine import GameEngine
from ..engine.vector import Vector
from ..games.yu_game import YuGame
from ..engine.ui import TextBox
from ..engine.solid import Solid
from ..engine.primitive import Rectangle
from ..engine.primitive import Circle
from ..engine.material import Material
from ..common.event import EventDispatcher
from ..common.events import *
from ..engine.game_object import GameObject
from ..engine.collider import Collider
from ..engine.transform import Transform

class MainMenuGame(YuGame):
	DELTA = 10
	def __init__(self, name):
		super(MainMenuGame, self).__init__("MainMenuGame")
		self._engine = GameEngine()

	def setup(self):
		super(MainMenuGame, self).setup() 
		EventDispatcher().add_event_listener(KeyDownEvent.TYPE, self.processKeyDownEvent)

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

		def createWall(position, dimensions):
			wall = GameObject("wall")
			wall.addComponent(Rectangle)
			wall.addComponent(Material)
			wall.addComponent(Collider)
			wall.getComponent(Transform).position = position
			wall.getComponent(Rectangle).dimensions = dimensions
		createWall(Vector(0, -resolution.y / 2), Vector(resolution.x, thickness))
		createWall(Vector(0, resolution.y / 2), Vector(resolution.x, thickness))
		createWall(Vector(-resolution.x / 2, 0), Vector(thickness, resolution.y))
		createWall(Vector(resolution.x / 2, 0), Vector(thickness, resolution.y))

	def update(self):
		return

	def stop(self):
		return

	def processKeyDownEvent(self, event):
		if event.data() == Key.W:
			self._p1.getComponent(Transform).position.y -= self.DELTA
			return
		elif event.data() == Key.A:
			return
		elif event.data() == Key.S:
			self._p1.getComponent(Transform).position.y += self.DELTA
			return
		elif event.data() == Key.D:
			return
		elif event.data() == Key.I:
			self._p2.getComponent(Transform).position.y -= self.DELTA
			return
		elif event.data() == Key.J:
			return
		elif event.data() == Key.K:
			self._p2.getComponent(Transform).position.y += self.DELTA
			return
		elif event.data() == Key.L:
			return
		return