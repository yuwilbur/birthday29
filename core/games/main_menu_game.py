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
from ..sync.period_sync import PeriodSync
from ..engine.line import Line
from ..engine.align import Align

import time

class MainMenuGame(YuGame):
	DELTA = 200
	def __init__(self):
		super(MainMenuGame, self).__init__("MainMenuGame")

	def onP1Collision(self, game_object):
		if game_object.name == 'ball':
			return
		self._p1.getComponent(Transform).position.y -= self._p1.getComponent(Solid).velocity.y * PeriodSync.PERIOD
		self._p1.getComponent(Solid).velocity.y = 0

	def onP2Collision(self, game_object):
		if game_object.name == 'ball':
			return
		self._p2.getComponent(Transform).position.y -= self._p2.getComponent(Solid).velocity.y * PeriodSync.PERIOD
		self._p2.getComponent(Solid).velocity.y = 0

	def setGameInfo(self, texts):
		self._game_info.getComponent(TextBox).setTexts(texts)

	def onP1Score(self, game_object):
		if not game_object.name == 'ball':
			return
		super(MainMenuGame, self).onP1Score()
		self.resetPositions()

	def onP2Score(self, game_object):
		if not game_object.name == 'ball':
			return
		super(MainMenuGame, self).onP2Score()
		self.resetPositions()

	def setup(self):
		super(MainMenuGame, self).setup() 
		EventDispatcher().add_event_listener(KeyEvent.TYPE, self.onKeyEvent)
		#EventDispatcher().add_event_listener(KeyDownEvent.TYPE, self.onKeyDownEvent)
		EventDispatcher().add_event_listener(KeyUpEvent.TYPE, self.onKeyUpEvent)

		thickness = 25

		self._p1 = GameObject("p1")
		self._p1.addComponent(Rectangle)
		self._p1.addComponent(Material)
		self._p1.addComponent(Collider)
		self._p1.getComponent(Rectangle).dimensions = Vector(thickness, 150)
		self._p1.getComponent(Collider).setOnCollisionListener(self.onP1Collision)
		self._p1.addComponent(Line)

		self._p2 = GameObject("p2")
		self._p2.addComponent(Rectangle)
		self._p2.addComponent(Material)
		self._p2.addComponent(Collider)
		self._p2.getComponent(Rectangle).dimensions = Vector(thickness, 150) 
		self._p2.getComponent(Collider).setOnCollisionListener(self.onP2Collision)
		self._p2.addComponent(Line)

		self._ball = GameObject("ball")
		self._ball.addComponent(Circle)
		self._ball.addComponent(Material)
		self._ball.addComponent(Collider)
		self._ball.getComponent(Circle).radius = 25

		self._resolution = self.getResolution()

		def createWall(position, dimensions):
			wall = GameObject("wall")
			wall.addComponent(Rectangle)
			wall.addComponent(Material)
			wall.getComponent(Material).color = Color.BLACK
			wall.addComponent(Collider)
			wall.getComponent(Transform).position = position + self.getOffset()
			wall.getComponent(Rectangle).dimensions = dimensions
			return wall
		createWall(Vector(0, -self._resolution.y / 2), Vector(self._resolution.x, thickness))
		createWall(Vector(0, self._resolution.y / 2), Vector(self._resolution.x, thickness))
		p1_target = createWall(Vector(self._resolution.x / 2, 0), Vector(thickness, self._resolution.y))
		p1_target.getComponent(Collider).setOnCollisionListener(self.onP1Score)
		p2_target = createWall(Vector(-self._resolution.x / 2, 0), Vector(thickness, self._resolution.y))
		p2_target.getComponent(Collider).setOnCollisionListener(self.onP2Score)

		self._game_info = GameObject("main game info")
		self._game_info.addComponent(TextBox)
		self._game_info.getComponent(TextBox).font_size = self._font_size
		self._game_info.getComponent(TextBox).width = 1000
		self._game_info.getComponent(TextBox).height = thickness * 2
		self._game_info.getComponent(TextBox).align = Align.CENTER
		self._game_info.getComponent(Transform).position = Vector(0, -self._resolution.y / 2 + thickness * 2)

		self.reset()

	def update(self):
		super(MainMenuGame, self).update()
		self._p1.getComponent(Line).start = self._p1.getComponent(Transform).position
		self._p1.getComponent(Line).end = self._ball.getComponent(Transform).position
		self._p2.getComponent(Line).start = self._p2.getComponent(Transform).position
		self._p2.getComponent(Line).end = self._ball.getComponent(Transform).position
		self._game_duration = time.time() - self._game_start
		if (self._game_duration < 1.0):
			self.setGameInfo(["3"])
		elif (self._game_duration < 2.0):
			self.setGameInfo(["2"])
		elif (self._game_duration < 3.0):
			self.setGameInfo(["1"])
		elif (self._game_duration < 4.0):
			self.setGameInfo(["FIGHT"])
			if (self._control_lock):
				self._ball.getComponent(Solid).velocity = Vector(400, 0)
			self._control_lock = False
		else:
			self.setGameInfo([""])

	def resetPositions(self):
		start_distance = 500
		self._p1.getComponent(Transform).position = Vector(-start_distance,0) + self.getOffset()
		self._p1.getComponent(Solid).velocity = Vector(0, 0)
		self._p2.getComponent(Transform).position = Vector(start_distance, 0) + self.getOffset()
		self._p2.getComponent(Solid).velocity = Vector(0, 0)
		self._ball.getComponent(Transform).position = Vector() + self.getOffset()
		self._ball.getComponent(Solid).velocity = Vector(0, 0)
		self._game_start = time.time()
		self._control_lock = True

	def reset(self):
		super(MainMenuGame, self).reset()
		self.resetPositions()

	def onKeyEvent(self, event):
		if (self._control_lock):
			return
		if event.data() == Key.W:
			self._p1.getComponent(Solid).velocity.y = -self.DELTA
			return
		elif event.data() == Key.A:
			self._p1.getComponent(Line).color = Color.BLUE
			return
		elif event.data() == Key.S:
			self._p1.getComponent(Solid).velocity.y = self.DELTA
			return
		elif event.data() == Key.D:
			self._p1.getComponent(Line).color = Color.RED
			return
		elif event.data() == Key.I:
			self._p2.getComponent(Solid).velocity.y = -self.DELTA
			return
		elif event.data() == Key.J:
			self._p2.getComponent(Line).color = Color.BLUE
			return
		elif event.data() == Key.K:
			self._p2.getComponent(Solid).velocity.y = self.DELTA
			return
		elif event.data() == Key.L:
			self._p2.getComponent(Line).color = Color.RED
			return
		return

	def onKeyUpEvent(self, event):
		if (self._control_lock):
			return
		if event.data() == Key.W:
			self._p1.getComponent(Solid).velocity.y = 0
			return
		elif event.data() == Key.A:
			self._p1.getComponent(Line).color = Color.WHITE
			return
		elif event.data() == Key.S:
			self._p1.getComponent(Solid).velocity.y = 0
			return
		elif event.data() == Key.D:
			self._p1.getComponent(Line).color = Color.WHITE
			return
		elif event.data() == Key.I:
			self._p2.getComponent(Solid).velocity.y = 0
			return
		elif event.data() == Key.J:
			self._p2.getComponent(Line).color = Color.WHITE
			return
		elif event.data() == Key.K:
			self._p2.getComponent(Solid).velocity.y = 0
			return
		elif event.data() == Key.L:
			self._p2.getComponent(Line).color = Color.WHITE
			return
		return