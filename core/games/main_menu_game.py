from ..engine.vector import Vector
from ..games.yu_game import YuGame
from ..engine.ui import TextBox
from ..engine.solid import Solid
from ..engine.primitive import Rectangle
from ..engine.primitive import Circle
from ..engine.material import *
from ..common.event import EventDispatcher
from ..common.events import *
from ..engine.game_object import GameObject
from ..engine.collider import Collider
from ..engine.transform import Transform
from ..engine.magnet import Magnet
from ..renderer.color import Color
from ..sync.period_sync import PeriodSync
from ..engine.line import *
from ..engine.gradient_rectangle import GradientRectangle
from ..engine.align import Align
from ..engine.gradient_circle import GradientCircle

import time
import random
import pygame
import os, sys

class MainMenuGame(YuGame):
	ASSETS_PATH = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), "core", "assets")
	HIT_SOUND_PATH = os.path.join(ASSETS_PATH, "boop.wav")
	BOOM_SOUND_PATH = os.path.join(ASSETS_PATH, "boom2.wav")
	HUM_SOUND_PATH = os.path.join(ASSETS_PATH, "hum.wav")
	#MUSIC_PATH = os.path.join(ASSETS_PATH, "music2.ogg")
	MUSIC_PATH = os.path.join(ASSETS_PATH, "music.mp3")
	score_width = 600
	score_delay = 0.8
	def __init__(self):
		super(MainMenuGame, self).__init__("MainMenuGame")

	def setSpeeds(self, delta):
		delta = min(800, delta)
		self.delta = delta
		self.acc = delta * 4
		self.vel = delta
		self.ball_speed = delta * 1.5
		self.ball_acceleration = delta * 3
		self.max_ball_speed = self.ball_speed * 3
		self.gradience_speed = delta / 2

	def diffSpeeds(self, delta):
		self.delta += delta
		self.setSpeeds(self.delta)

	def onP1Collision(self, game_object):
		if game_object.name == 'ball':
			return
		self._p1.getComponent(Transform).position.y -= self._p1.getComponent(Solid).velocity.y * PeriodSync().period
		self._p1.getComponent(Solid).velocity.y = 0

	def onP2Collision(self, game_object):
		if game_object.name == 'ball':
			return
		self._p2.getComponent(Transform).position.y -= self._p2.getComponent(Solid).velocity.y * PeriodSync().period
		self._p2.getComponent(Solid).velocity.y = 0

	def onBallCollision(self, game_object):
		self._hit_sound.play()

	def setGameInfo(self, texts):
		self._game_info.getComponent(TextBox).setTexts(texts)

	def onP1Score(self, game_object):
		if not game_object.name == 'ball':
			return
		super(MainMenuGame, self).onP1Score()
		self._boom_sound.play()
		self.resetPositions()
		self._p1_score.getComponent(GradientRectangle).dimensions = Vector(self._resolution.x, self._resolution.y)
		width = int(self._p1_score.getComponent(GradientRectangle).dimensions.x * self.score_delay)
		self._p1_score.getComponent(Transform).position = Vector(self._resolution.x / 2 - width / 2 + self.wall_thickness / 2,0) + self.getOffset()

	def onP2Score(self, game_object):
		if not game_object.name == 'ball':
			return
		super(MainMenuGame, self).onP2Score()
		self._boom_sound.play()
		self.resetPositions()
		self._p2_score.getComponent(GradientRectangle).dimensions = Vector(self._resolution.x, self._resolution.y)
		width = int(self._p2_score.getComponent(GradientRectangle).dimensions.x * self.score_delay)
		self._p2_score.getComponent(Transform).position = Vector(-self._resolution.x / 2 + width / 2 - self.wall_thickness / 2,0) + self.getOffset()

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

		thickness = 40

		self._p1 = GameObject("p1")
		self._p1.addComponent(Rectangle)
		self._p1.addComponent(LateMaterial)
		self._p1.addComponent(Collider)
		self._p1.getComponent(Rectangle).dimensions = Vector(thickness, 150)
		self._p1.getComponent(Collider).setOnCollisionListener(self.onP1Collision)
		#self._p1.addComponent(DashedLine)
		#self._p1.getComponent(DashedLine).color = Color.WHITE
		self._p1.addComponent(GradientCircle)
		self._p1.getComponent(GradientCircle).offset = Vector(50,0)
		self._p1.getComponent(GradientCircle).start_color = Color.RED
		self._p1.getComponent(GradientCircle).step = 0
		self._p1_push = False
		self._p1_pull = False
		self._p1_score = GameObject("p1 score")
		self._p1_score.addComponent(GradientRectangle)
		self._p1_score.getComponent(GradientRectangle).start_color = Color.BLACK
		self._p1_score.getComponent(GradientRectangle).end_color = Color.BLUE

		self._p2 = GameObject("p2")
		self._p2.addComponent(Rectangle)
		self._p2.addComponent(LateMaterial)
		self._p2.addComponent(Collider)
		self._p2.getComponent(Rectangle).dimensions = Vector(thickness, 150) 
		self._p2.getComponent(Collider).setOnCollisionListener(self.onP2Collision)
		self._p2.addComponent(GradientCircle)
		self._p2.getComponent(GradientCircle).offset = Vector(-50,0)
		self._p2.getComponent(GradientCircle).start_color = Color.BLUE
		self._p2.getComponent(GradientCircle).step = 0
		#self._p2.addComponent(DashedLine)
		#self._p2.getComponent(DashedLine).color = Color.WHITE
		self._p2_push = False
		self._p2_pull = False
		self._p2_score = GameObject("p2 score")
		self._p2_score.addComponent(GradientRectangle)
		self._p2_score.getComponent(GradientRectangle).start_color = Color.RED
		self._p2_score.getComponent(GradientRectangle).end_color = Color.BLACK

		self._ball = GameObject("ball")
		self._ball.addComponent(Circle)
		self._ball.addComponent(Material)
		self._ball.addComponent(Collider)
		self._ball.getComponent(Circle).radius = 25
		self._ball.getComponent(Collider).setOnCollisionListener(self.onBallCollision)

		self._stage = 1

		self._resolution = self.getResolution()

		self._hit_sound = pygame.mixer.Sound(self.HIT_SOUND_PATH)
		self._hit_sound.set_volume(1.0)
		self._boom_sound = pygame.mixer.Sound(self.BOOM_SOUND_PATH)
		self._boom_sound.set_volume(1.0)
		self._hum_sound = pygame.mixer.Sound(self.HUM_SOUND_PATH)
		self._hum_sound.set_volume(1.0)
		self._is_hum_playing = False
		pygame.mixer.music.load(self.MUSIC_PATH)
		pygame.mixer.music.set_volume(0.25)
		pygame.mixer.music.play(-1)

		self.setSpeeds(50)

		def createWall(position, dimensions, color):
			wall = GameObject("wall")
			wall.addComponent(Rectangle)
			wall.addComponent(Material)
			wall.getComponent(Material).color = color
			wall.addComponent(Collider)
			wall.getComponent(Transform).position = position + self.getOffset()
			wall.getComponent(Rectangle).dimensions = dimensions
			return wall
		self.wall_thickness = 100
		wall_thickness = self.wall_thickness
		createWall(Vector(0, -self._resolution.y / 2 - (wall_thickness / 2 - thickness)), Vector(self._resolution.x, wall_thickness), Color.WHITE)
		createWall(Vector(0, self._resolution.y / 2 + (wall_thickness / 2 - thickness)), Vector(self._resolution.x, wall_thickness), Color.WHITE)
		p1_target = createWall(Vector(self._resolution.x / 2 - (wall_thickness / 2 - thickness), 0), Vector(wall_thickness, self._resolution.y - thickness * 2), Color.BLUE)
		p1_target.getComponent(Collider).setOnCollisionListener(self.onP1Score)
		p2_target = createWall(Vector(-self._resolution.x / 2 + (wall_thickness / 2 - thickness), 0), Vector(wall_thickness, self._resolution.y - thickness * 2), Color.RED)
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
		if (self._p1_score.getComponent(GradientRectangle).dimensions.x > 0):
			width = int(self._p1_score.getComponent(GradientRectangle).dimensions.x * self.score_delay)
			self._p1_score.getComponent(GradientRectangle).dimensions.x = width
			self._p1_score.getComponent(Transform).position = Vector(self._resolution.x / 2 - width / 2 + self.wall_thickness / 2,0) + self.getOffset()
		if (self._p2_score.getComponent(GradientRectangle).dimensions.x > 0):
			width = int(self._p2_score.getComponent(GradientRectangle).dimensions.x * self.score_delay)
			self._p2_score.getComponent(GradientRectangle).dimensions.x = width
			self._p2_score.getComponent(Transform).position = Vector(-self._resolution.x / 2 + width / 2 - self.wall_thickness / 2,0) + self.getOffset()
		if (self._game_lock):
			self._game_start = time.time()
		self._game_duration = time.time() - self._game_start
		if (self._game_duration < 2.0):
			self.setGameInfo(["READY?"])
		elif (self._game_duration < 3.0):
			self.setGameInfo(["3"])
		elif (self._game_duration < 4.0):
			self.setGameInfo(["2"])
		elif (self._game_duration < 5.0):
			self.setGameInfo(["1"])
		elif (self._game_duration < 6.0):
			self.setGameInfo(["GO"])
			if (self._control_lock):
				direction = random.randint(0,1)
				if (direction == 0):
					direction = -1
				self._ball.getComponent(Solid).velocity = Vector(direction * self.ball_speed, 0)
			self._control_lock = False
		else:
			self.setGameInfo([""])
		

		#self._p1.getComponent(DashedLine).dash_length = -1
		#self._p2.getComponent(DashedLine).dash_length = -1
		if (self._stage >= 3):
			#self._p1.getComponent(DashedLine).start = self._p1.getComponent(Transform).position + self._p1.getComponent(Magnet).offset
			#self._p1.getComponent(DashedLine).end = self._ball.getComponent(Transform).position
			#p1_vector = (self._p1.getComponent(DashedLine).end - self._p1.getComponent(DashedLine).start).toUnitVector()
			#self._p2.getComponent(DashedLine).start = self._p2.getComponent(Transform).position + self._p2.getComponent(Magnet).offset
			#self._p2.getComponent(DashedLine).end = self._ball.getComponent(Transform).position
			#p2_vector = (self._p2.getComponent(DashedLine).end - self._p2.getComponent(DashedLine).start).toUnitVector()
			p1_position = self._p1.getComponent(Transform).position + self._p1.getComponent(GradientCircle).offset
			p2_position = self._p2.getComponent(Transform).position + self._p2.getComponent(GradientCircle).offset
			ball_position = self._ball.getComponent(Transform).position
			p1_vector = (ball_position - p1_position).toUnitVector()
			p2_vector = (ball_position - p2_position).toUnitVector()
			#self._p1.getComponent(DashedLine).dash_length = 0
			#self._p2.getComponent(DashedLine).dash_length = 0
			#pull_offset = 5.0
			#pull_length = 10.0
			#push_offset = 2.5
			#push_length = 5.0
			self._ball.getComponent(Solid).acceleration = Vector(0, 0)

			max_distance = self._resolution.x * 3 / 4

			p1_acceleration = 0
			if self._p1_pull:
				#self._p1.getComponent(DashedLine).offset -= pull_offset
				#self._p1.getComponent(DashedLine).dash_length = pull_length
				self._p1.getComponent(GradientCircle).radius -= self.gradience_speed
				if (self._p1.getComponent(GradientCircle).radius < 0):
					self._p1.getComponent(GradientCircle).radius = max_distance
				p1_acceleration = -self.ball_acceleration
			elif self._p1_push:
				self._p1.getComponent(GradientCircle).radius += self.gradience_speed
				if (self._p1.getComponent(GradientCircle).radius > max_distance):
					self._p1.getComponent(GradientCircle).radius = 0
				#self._p1.getComponent(DashedLine).offset += push_offset
				#self._p1.getComponent(DashedLine).dash_length = push_length
				p1_acceleration = self.ball_acceleration
			else:
				self._p1.getComponent(GradientCircle).radius = 0

			p1_strength = max(0.0, (max_distance - Vector.Distance(self._ball.getComponent(Transform).position, self._p1.getComponent(Transform).position)) / max_distance)
			p1_acceleration *= p1_strength

			self._ball.getComponent(Solid).acceleration += p1_vector * p1_acceleration
			
			p2_acceleration = 0
			if self._p2_pull:
				self._p2.getComponent(GradientCircle).radius -= self.gradience_speed
				if (self._p2.getComponent(GradientCircle).radius < 0):
					self._p2.getComponent(GradientCircle).radius = max_distance
				#self._p2.getComponent(DashedLine).offset -= pull_offset
				#self._p2.getComponent(DashedLine).dash_length = pull_length
				p2_acceleration = -self.ball_acceleration
			elif self._p2_push:
				self._p2.getComponent(GradientCircle).radius += self.gradience_speed
				if (self._p2.getComponent(GradientCircle).radius > max_distance):
					self._p2.getComponent(GradientCircle).radius = 0
				#self._p2.getComponent(DashedLine).offset += push_offset
				#self._p2.getComponent(DashedLine).dash_length = push_length
				p2_acceleration = self.ball_acceleration
			else:
				self._p2.getComponent(GradientCircle).radius = 0
			p2_strength = max(0.0, (max_distance - Vector.Distance(self._ball.getComponent(Transform).position, self._p2.getComponent(Transform).position)) / max_distance)
			p2_acceleration *= p2_strength

			self._ball.getComponent(Solid).acceleration += p2_vector * p2_acceleration

			if self._p1_pull:
				if self._p1_hold or Vector.DistanceSqu(self._ball.getComponent(Transform).position, p1_position) <= self.delta * 2:
					self._ball.getComponent(Transform).position = p1_position
					self._ball.getComponent(Solid).velocity = Vector()
					self._ball.getComponent(Solid).acceleration = Vector()
					self._p1_hold = True
					if not self._is_hum_playing:
						self._is_hum_playing = True
						self._hum_sound.play(-1)
			elif self._p1_hold:
				self._boom_sound.play()
				self._ball.getComponent(Solid).velocity = Vector(self.max_ball_speed / 2, 0) + self._p1.getComponent(Solid).velocity * 2
				self._p1_hold = False
				self._hum_sound.stop()
				self._is_hum_playing = False

			if self._p2_pull:
				if self._p2_hold or Vector.DistanceSqu(self._ball.getComponent(Transform).position, p2_position) <= self.delta * 2:
					self._ball.getComponent(Transform).position = p2_position
					self._ball.getComponent(Solid).velocity = Vector()
					self._ball.getComponent(Solid).acceleration = Vector()
					self._p2_hold = True
					if not self._is_hum_playing:
						self._is_hum_playing = True
						self._hum_sound.play(-1)
			elif self._p2_hold:
				self._boom_sound.play()
				self._ball.getComponent(Solid).velocity = - Vector(self.max_ball_speed / 2, 0) + self._p2.getComponent(Solid).velocity * 2
				self._p2_hold = False
				self._hum_sound.stop()
				self._is_hum_playing = False

		if (self._ball.getComponent(Solid).velocity.magnitude() > self.max_ball_speed):
			self._ball.getComponent(Solid).velocity = self._ball.getComponent(Solid).velocity.toUnitVector() * self.max_ball_speed

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
		self._p1.getComponent(GradientCircle).radius = 0
		self._p2.getComponent(GradientCircle).radius = 0
		self._p1_push = False
		self._p1_pull = False
		self._p1_hold = False
		self._p2_push = False
		self._p2_pull = False
		self._p2_hold = False
		self._game_start = time.time()
		self._control_lock = True

	def reset(self):
		super(MainMenuGame, self).reset()
		self.resetPositions()

	def onKeyEvent(self, event):
		if event.data() == Key.NUM_1:
			self._stage = 1
			return
		elif event.data() == Key.NUM_2:
			self._stage = 2
			return
		elif event.data() == Key.NUM_3:
			self._stage = 3
			return
		elif event.data() == Key.NUM_5:
			self.diffSpeeds(-10)
			return
		elif event.data() == Key.NUM_6:
			self.diffSpeeds(10)
			return
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
