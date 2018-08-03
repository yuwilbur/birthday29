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
from ..renderer.color import Color

class MainMenuGame(YuGame):
	DELTA = 10
	def __init__(self):
		super(MainMenuGame, self).__init__("MainMenuGame")

	def onP1Collision(self, game_object):
		print 'p1'

	def onP2Collision(self, game_object):
		print 'p2'

	def setup(self):
		super(MainMenuGame, self).setup() 
		EventDispatcher().add_event_listener(KeyEvent.TYPE, self.onKeyEvent)

		thickness = 25

		self._p1 = GameObject("p1")
		self._p1.addComponent(Rectangle)
		self._p1.addComponent(Material)
		self._p1.addComponent(Collider)
		self._p1.getComponent(Rectangle).dimensions = Vector(thickness, 150)
		self._p1.getComponent(Collider).setOnCollisionListener(self.onP1Collision)

		self._p2 = GameObject("p2")
		self._p2.addComponent(Rectangle)
		self._p2.addComponent(Material)
		self._p2.addComponent(Collider)
		self._p2.getComponent(Rectangle).dimensions = Vector(thickness, 150) 
		self._p2.getComponent(Collider).setOnCollisionListener(self.onP2Collision)

		self._ball = GameObject("ball")
		self._ball.addComponent(Circle)
		self._ball.addComponent(Material)
		self._ball.addComponent(Collider)
		self._ball.getComponent(Circle).radius = 25

		resolution = self.getResolution()

		def createWall(position, dimensions):
			wall = GameObject("wall")
			wall.addComponent(Rectangle)
			wall.addComponent(Material)
			wall.getComponent(Material).color = Color.BLACK
			wall.addComponent(Collider)
			wall.getComponent(Transform).position = position + self.getOffset()
			wall.getComponent(Rectangle).dimensions = dimensions
			return wall
		createWall(Vector(0, -resolution.y / 2), Vector(resolution.x, thickness))
		createWall(Vector(0, resolution.y / 2), Vector(resolution.x, thickness))
		p1_target = createWall(Vector(resolution.x / 2, 0), Vector(thickness, resolution.y))
		p1_target.getComponent(Collider).setOnCollisionListener(self.onP1Score)
		p2_target = createWall(Vector(-resolution.x / 2, 0), Vector(thickness, resolution.y))
		p2_target.getComponent(Collider).setOnCollisionListener(self.onP2Score)

		self.reset()

	def reset(self):
		start_distance = 500
		self._p1.getComponent(Transform).position = Vector(-start_distance,0) + self.getOffset()
		self._p2.getComponent(Transform).position = Vector(start_distance, 0) + self.getOffset()
		self._ball.getComponent(Transform).position = Vector() + self.getOffset()
		self._ball.getComponent(Solid).velocity = Vector(400, 0)

	def onKeyEvent(self, event):
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