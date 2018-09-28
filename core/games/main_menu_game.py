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
from ..engine.line import *
from ..engine.gradient_rectangle import GradientRectangle
from ..engine.align import Align

import time
import random

class MainMenuGame(YuGame):
	DELTA = 100
	acc = DELTA * 4
	vel = DELTA
	ball_speed = DELTA * 2
	ball_acceleration = DELTA / 2
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

	def start(self):
		super(MainMenuGame, self).start()
		self._game_lock = False

	def stop(self):
		super(MainMenuGame, self).stop()
		self._game_lock = True

	def setup(self):
		super(MainMenuGame, self).setup() 
		EventDispatcher().add_event_listener(KeyEvent.TYPE, self.onKeyEvent)
		EventDispatcher().add_event_listener(KeyUpEvent.TYPE, self.onKeyUpEvent)

		thickness = 25

		self._p1 = GameObject("p1")
		self._p1.addComponent(Rectangle)
		self._p1.addComponent(Material)
		self._p1.addComponent(Collider)
		self._p1.getComponent(Rectangle).dimensions = Vector(thickness, 150)
		self._p1.getComponent(Collider).setOnCollisionListener(self.onP1Collision)
		self._p1.addComponent(DashedLine)
		self._p1.getComponent(DashedLine).color = Color.WHITE
		self._p1_push = False
		self._p1_pull = False
		self._p1_score = GameObject("p1 score")
		self._p1_score.addComponent(GradientRectangle)
		self._p1_score.getComponent(GradientRectangle).dimensions = Vector(100,100)

		self._p2 = GameObject("p2")
		self._p2.addComponent(Rectangle)
		self._p2.addComponent(Material)
		self._p2.addComponent(Collider)
		self._p2.getComponent(Rectangle).dimensions = Vector(thickness, 150) 
		self._p2.getComponent(Collider).setOnCollisionListener(self.onP2Collision)
		self._p2.addComponent(DashedLine)
		self._p2.getComponent(DashedLine).color = Color.WHITE
		self._p2_push = False
		self._p2_pull = False

		self._ball = GameObject("ball")
		self._ball.addComponent(Circle)
		self._ball.addComponent(Material)
		self._ball.addComponent(Collider)
		self._ball.getComponent(Circle).radius = 25

		self._stage = 1

		self._resolution = self.getResolution()

		def createWall(position, dimensions, color):
			wall = GameObject("wall")
			wall.addComponent(Rectangle)
			wall.addComponent(Material)
			wall.getComponent(Material).color = color
			wall.addComponent(Collider)
			wall.getComponent(Transform).position = position + self.getOffset()
			wall.getComponent(Rectangle).dimensions = dimensions
			return wall
		createWall(Vector(0, -self._resolution.y / 2), Vector(self._resolution.x, thickness), Color.WHITE)
		createWall(Vector(0, self._resolution.y / 2), Vector(self._resolution.x, thickness), Color.WHITE)
		p1_target = createWall(Vector(self._resolution.x / 2, 0), Vector(thickness, self._resolution.y), Color.BLUE)
		p1_target.getComponent(Collider).setOnCollisionListener(self.onP1Score)
		p2_target = createWall(Vector(-self._resolution.x / 2, 0), Vector(thickness, self._resolution.y), Color.RED)
		p2_target.getComponent(Collider).setOnCollisionListener(self.onP2Score)

		self._game_info = GameObject("main game info")
		self._game_info.addComponent(TextBox)
		self._game_info.getComponent(TextBox).font_size = self._font_size
		self._game_info.getComponent(TextBox).width = 1000
		self._game_info.getComponent(TextBox).height = thickness * 2
		self._game_info.getComponent(TextBox).align = Align.CENTER
		self._game_info.getComponent(Transform).position = Vector(0, -self._resolution.y / 2 + thickness * 2)

		self._game_lock = True

		self.reset()

	def update(self):
		super(MainMenuGame, self).update()
		if (self._game_lock):
			self._game_start = time.time()
		self._game_duration = time.time() - self._game_start
		if (self._game_duration < 1.0):
			self.setGameInfo(["READY?"])
		elif (self._game_duration < 2.0):
			self.setGameInfo(["3"])
		elif (self._game_duration < 3.0):
			self.setGameInfo(["2"])
		elif (self._game_duration < 4.0):
			self.setGameInfo(["1"])
		elif (self._game_duration < 5.0):
			self.setGameInfo(["FIGHT"])
			if (self._control_lock):
				direction = random.randint(0,1)
				if (direction == 0):
					direction = -1
				self._ball.getComponent(Solid).velocity = Vector(direction * self.ball_speed, 0)
			self._control_lock = False
		else:
			self.setGameInfo([""])

		if (self._stage >= 3):
			self._p1.getComponent(DashedLine).start = self._p1.getComponent(Transform).position
			self._p1.getComponent(DashedLine).end = self._ball.getComponent(Transform).position
			p1_vector = (self._p1.getComponent(DashedLine).end - self._p1.getComponent(DashedLine).start).toUnitVector()
			self._p2.getComponent(DashedLine).start = self._p2.getComponent(Transform).position
			self._p2.getComponent(DashedLine).end = self._ball.getComponent(Transform).position
			p2_vector = (self._p2.getComponent(DashedLine).end - self._p2.getComponent(DashedLine).start).toUnitVector()
			self._p1.getComponent(DashedLine).dash_length = 0
			self._p2.getComponent(DashedLine).dash_length = 0
			pull_offset = 5.0
			pull_length = 10.0
			push_offset = 2.5
			push_length = 5.0
			self._ball.getComponent(Solid).acceleration = Vector(0, 0)
			if self._p1_pull and not self._p1_push:
				self._p1.getComponent(DashedLine).offset -= pull_offset
				self._p1.getComponent(DashedLine).dash_length = pull_length
				self._ball.getComponent(Solid).acceleration -= p1_vector * self.ball_acceleration
			elif self._p1_push and not self._p1_pull:
				self._p1.getComponent(DashedLine).offset += push_offset
				self._p1.getComponent(DashedLine).dash_length = push_length
				self._ball.getComponent(Solid).acceleration += p1_vector * self.ball_acceleration
			else:
				pass
			if self._p2_pull and not self._p2_push:
				self._p2.getComponent(DashedLine).offset -= pull_offset
				self._p2.getComponent(DashedLine).dash_length = pull_length
				self._ball.getComponent(Solid).acceleration -= p2_vector * self.ball_acceleration
			elif self._p2_push and not self._p2_pull:
				self._p2.getComponent(DashedLine).offset += push_offset
				self._p2.getComponent(DashedLine).dash_length = push_length
				self._ball.getComponent(Solid).acceleration += p2_vector * self.ball_acceleration
			else:
				pass
		else:
			self._p1.getComponent(DashedLine).dash_length = -1
			self._p2.getComponent(DashedLine).dash_length = -1

	def resetPositions(self):
		start_distance = 500
		self._p1.getComponent(Transform).position = Vector(-start_distance,0) + self.getOffset()
		self._p1.getComponent(Solid).velocity = Vector(0, 0)
		self._p1.getComponent(Solid).acceleration = Vector(0, 0)
		self._p2.getComponent(Transform).position = Vector(start_distance, 0) + self.getOffset()
		self._p2.getComponent(Solid).velocity = Vector(0, 0)
		self._p2.getComponent(Solid).acceleration = Vector(0, 0)
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
			if (self._stage >= 2):
				self._p1.getComponent(Solid).acceleration.y = -self.acc
			else:
				self._p1.getComponent(Solid).velocity.y = -self.vel
			return
		elif event.data() == Key.A:
			self._p1_pull = True
			return
		elif event.data() == Key.S:
			if (self._stage >= 2):
				self._p1.getComponent(Solid).acceleration.y = self.acc
			else:
				self._p1.getComponent(Solid).velocity.y = self.vel
			return
		elif event.data() == Key.D:
			self._p1_push = True
			return
		elif event.data() == Key.I:
			if (self._stage >= 2):
				self._p2.getComponent(Solid).acceleration.y = -self.acc
			else:
				self._p2.getComponent(Solid).velocity.y = -self.vel
			return
		elif event.data() == Key.J:
			self._p2_push = True
			return
		elif event.data() == Key.K:
			if (self._stage >= 2):
				self._p2.getComponent(Solid).acceleration.y = self.acc
			else:
				self._p2.getComponent(Solid).velocity.y = self.vel
			return
		elif event.data() == Key.L:
			self._p2_pull = True
			return
		elif event.data() == Key.NUM_1:
			self._stage = 1
			return
		elif event.data() == Key.NUM_2:
			self._stage = 2
			return
		elif event.data() == Key.NUM_3:
			self._stage = 3
			return
		return

	def onKeyUpEvent(self, event):
		if (self._control_lock):
			return
		if event.data() == Key.W:
			if (self._stage >= 2):
				self._p1.getComponent(Solid).acceleration.y = 0
			else:
				self._p1.getComponent(Solid).velocity.y = 0
			return
		elif event.data() == Key.A:
			self._p1_pull = False
			return
		elif event.data() == Key.S:
			if (self._stage >= 2):
				self._p1.getComponent(Solid).acceleration.y = 0
			else:
				self._p1.getComponent(Solid).velocity.y = 0
			return
		elif event.data() == Key.D:
			self._p1_push = False
			return
		elif event.data() == Key.I:
			if (self._stage >= 2):
				self._p2.getComponent(Solid).acceleration.y = 0
			else:
				self._p2.getComponent(Solid).velocity.y = 0
			return
		elif event.data() == Key.J:
			self._p2_push = False
			return
		elif event.data() == Key.K:
			if (self._stage >= 2):
				self._p2.getComponent(Solid).acceleration.y = 0
			else:
				self._p2.getComponent(Solid).velocity.y = 0
			return
		elif event.data() == Key.L:
			self._p2_pull = False
			return
		return