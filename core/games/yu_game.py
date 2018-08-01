from ..common.event import EventDispatcher
from ..common.events import *
from ..games.game import Game
from ..renderer.renderer import Renderer
from ..engine.vector import Vector
from ..engine.primitive import Circle
from ..engine.primitive import Rectangle
from ..engine.material import LateMaterial
from ..engine.game_object import GameObject
from ..engine.align import Align
from ..engine.ui import Image
from ..engine.ui import TextBox
from ..engine.transform import Transform
from ..input.frame import Frame
from ..renderer.color import Color

import time

class YuGame(Game):
	class PlayerInfo(object):
		def __init__(self, up, down, left, right):
			self.background = GameObject("background")
			self.background.addComponent(Rectangle)
			self.background.addComponent(LateMaterial)
			self.background.getComponent(LateMaterial).color = Color.BLACK
			self.camera = GameObject("camera")
			self.camera.addComponent(Image)
			self.latency_text = GameObject("text")
			self.latency_text.addComponent(TextBox)
			self.game_text = GameObject("game text")
			self.game_text.addComponent(TextBox)
			self.processed = []
			radius = 25
			self.up = GameObject("up")
			self.up.addComponent(Circle)
			self.up.addComponent(LateMaterial)
			self.up.getComponent(Circle).radius = radius
			self.down = GameObject("down")
			self.down.addComponent(Circle)
			self.down.addComponent(LateMaterial)
			self.down.getComponent(Circle).radius = radius
			self.left = GameObject("left")
			self.left.addComponent(Circle)
			self.left.addComponent(LateMaterial)
			self.left.getComponent(Circle).radius = radius
			self.right = GameObject("right")
			self.right.addComponent(Circle)
			self.right.addComponent(LateMaterial)
			self.right.getComponent(Circle).radius = radius
			self.controls = {
				up : (self.up, Color.LIGHT_BLUE, Color.DARK_BLUE),
				down : (self.down, Color.LIGHT_YELLOW, Color.DARK_YELLOW),
				left : (self.left, Color.LIGHT_GREEN, Color.DARK_GREEN),
				right : (self.right, Color.LIGHT_RED, Color.DARK_RED)
			}
			self.up.getComponent(LateMaterial).color = self.controls[up][2]
			self.down.getComponent(LateMaterial).color = self.controls[down][2]
			self.left.getComponent(LateMaterial).color = self.controls[left][2]
			self.right.getComponent(LateMaterial).color = self.controls[right][2]

	def setPlayer1Text(self, text):
		self._p1_info.game_text = text

	def setPlayer2Text(self, text):
		self._p2_info.game_text = text

	def onLatencyEvent(self, event):
		data = event.data()
		latency = str(int((time.time() - data[1]) * 1000))
		latency_type = data[0]
		if latency_type == LatencyEvent.P1_PROCESSING:
			self._p1_info.latency_text.getComponent(TextBox).texts = []
			self._p1_info.latency_text.getComponent(TextBox).texts.append(latency)
		elif latency_type == LatencyEvent.P2_PROCESSING:
			self._p2_info.latency_text.getComponent(TextBox).texts = []
			self._p2_info.latency_text.getComponent(TextBox).texts.append(latency)

	def onCameraResultEvent(self, event):
		result_type = event.data()[0]
		result = event.data()[1]
		if result_type == CameraResultEvent.P1:
			self._p1_info.processed = result
		elif result_type == CameraResultEvent.P2:
			self._p2_info.processed = result

	def onYImageEvent(self, event):
		p1_raw = event.data()[0]
		p2_raw = event.data()[1]
		stereo = [Frame(), Frame()]
		p1_raw.scale3(stereo[0])
		p2_raw.scale3(stereo[1])
		for pixel in self._p1_info.processed:
			stereo[0].data[pixel[0]][pixel[1]] = Color.GREEN[0:3]
		self._p1_info.camera.getComponent(Image).fromNumpy(stereo[0].data)
		for pixel in self._p2_info.processed:
			stereo[1].data[pixel[0]][pixel[1]] = Color.GREEN[0:3]
		self._p2_info.camera.getComponent(Image).fromNumpy(stereo[1].data)

	def getResolution(self):
		return self._resolution

	def getOffset(self):
		return self._offset

	def onMainKeyUpEvent(self, event):
		key = event.data()
		if key in self._p1_info.controls:
			control = self._p1_info.controls[key]
			control[0].getComponent(LateMaterial).color = control[2]
		if event.data() in self._p2_info.controls:
			control = self._p2_info.controls[key]
			control[0].getComponent(LateMaterial).color = control[2]

	def onMainKeyDownEvent(self, event):
		key = event.data()
		if key in self._p1_info.controls:
			control = self._p1_info.controls[key]
			control[0].getComponent(LateMaterial).color = control[1]
		if event.data() in self._p2_info.controls:
			control = self._p2_info.controls[key]
			control[0].getComponent(LateMaterial).color = control[1]

	def __init__(self, name):
		super(YuGame, self).__init__(name)
		self._info_width = 160
		self._camera_height = 160
		self._controls_height = 160

	def createPlayer(self, start, align, length, up, down, left, right):
		camera_length = self._info_width
		controls_length = self._info_width
		game_text_length = length - camera_length - controls_length
		game_text_width = game_text_length
		game_text_height = self._info_width
		latency_text_length = camera_length
		latency_text_width = latency_text_length
		latency_text_height = self._info_width
		if align == Align.RIGHT:
			camera_position = start + Vector(camera_length / 2, 0)
			controls_position = camera_position + Vector(camera_length / 2, 0) + Vector(controls_length / 2, 0)
			game_text_position = controls_position + Vector(controls_length / 2, 0) + Vector(game_text_length / 2, 0)
			latency_text_position = camera_position
			background_position = start + Vector((camera_length + controls_length + game_text_length) / 2, 0)
		else:
			camera_position = start - Vector(camera_length / 2, 0)
			controls_position = camera_position - Vector(camera_length / 2, 0) - Vector(controls_length / 2, 0)
			game_text_position = controls_position - Vector(controls_length / 2, 0) - Vector(game_text_length / 2, 0)
			latency_text_position = camera_position
			background_position = start - Vector((camera_length + controls_length + game_text_length) / 2, 0)
		player = YuGame.PlayerInfo(up, down, left, right)
		player.background.getComponent(Transform).position = background_position
		player.background.getComponent(Rectangle).dimensions = Vector(length, self._info_width)
		player.latency_text.getComponent(Transform).position = latency_text_position
		player.latency_text.getComponent(TextBox).width = latency_text_width
		player.latency_text.getComponent(TextBox).height = latency_text_height
		player.game_text.getComponent(Transform).position = game_text_position
		player.game_text.getComponent(TextBox).width = game_text_width
		player.game_text.getComponent(TextBox).height = game_text_height
		controls_diff = 50
		player.up.getComponent(Transform).position = controls_position - Vector(0, controls_diff)
		player.down.getComponent(Transform).position = controls_position + Vector(0, controls_diff)
		player.right.getComponent(Transform).position = controls_position + Vector(controls_diff, 0)
		player.left.getComponent(Transform).position = controls_position - Vector(controls_diff, 0)
		player.camera.getComponent(Transform).position = camera_position
		return player

	def setup(self):
		self._offset = Vector(0, -self._info_width / 2)
		self._resolution = Renderer().getResolution() - Vector(0, self._info_width)
		p1_x = - self._resolution.x / 2
		p1_y = self._resolution.y / 2
		p2_x = self._resolution.x / 2
		p2_y = self._resolution.y / 2
		length = self._resolution.x / 2
		self._p1_info = self.createPlayer(Vector(p1_x, p1_y), Align.RIGHT, length, Key.W, Key.S, Key.A, Key.D)
		self._p2_info = self.createPlayer(Vector(p2_x, p2_y), Align.LEFT, length, Key.I, Key.K, Key.J, Key.L)
		EventDispatcher().add_event_listener(KeyDownEvent.TYPE, self.onMainKeyDownEvent)
		EventDispatcher().add_event_listener(KeyUpEvent.TYPE, self.onMainKeyUpEvent)
		EventDispatcher().add_event_listener(YImageEvent.TYPE, self.onYImageEvent)
		EventDispatcher().add_event_listener(LatencyEvent.TYPE, self.onLatencyEvent)
		EventDispatcher().add_event_listener(CameraResultEvent.TYPE, self.onCameraResultEvent)

	def update(self):
		self._p1_info.game_text.getComponent(TextBox).texts = []
		self._p1_info.game_text.getComponent(TextBox).texts.append("Ready Player One")
		self._p2_info.game_text.getComponent(TextBox).texts = []
		self._p2_info.game_text.getComponent(TextBox).texts.append("Ready Player Two")

