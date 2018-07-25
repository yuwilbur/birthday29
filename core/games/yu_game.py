from ..common.event import EventDispatcher
from ..common.events import *
from ..games.game import Game
from ..renderer.renderer import Renderer
from ..engine.vector import Vector
from ..engine.primitive import Circle
from ..engine.primitive import Rectangle
from ..engine.material import LateMaterial
from ..engine.game_object import GameObject
from ..engine.ui import Image
from ..engine.ui import TextBox
from ..engine.transform import Transform
from ..input.frame import Frame

from pygame.color import Color
import time

class YuGame(Game):
	class PlayerInfo(object):
		def __init__(self):
			self.background = GameObject("background")
			self.background.addComponent(Rectangle)
			self.background.addComponent(LateMaterial)
			self.background.getComponent(LateMaterial).color = Color(0,0,0)
			self.text = GameObject("text")
			self.text.addComponent(TextBox)
			self.camera = GameObject("camera")
			self.camera.addComponent(Image)
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

	def processLatencyEvent(self, event):
		data = event.data()
		latency = str(int((time.time() - data[1]) * 1000))
		latency_type = data[0]
		if latency_type == LatencyEvent.P1_PROCESSING:
			self._p1_info.text.getComponent(TextBox).text = latency
		elif latency_type == LatencyEvent.P2_PROCESSING:
			self._p2_info.text.getComponent(TextBox).text = latency

	def processCameraResultEvent(self, event):
		result_type = event.data()[0]
		result = event.data()[1]
		if result_type == CameraResultEvent.P1:
			self._p1_info.processed = result
		elif result_type == CameraResultEvent.P2:
			self._p2_info.processed = result

	def processYImageEvent(self, event):
		p1_raw = event.data()[0]
		p2_raw = event.data()[1]
		stereo = [Frame(), Frame()]
		p1_raw.scale3(stereo[0])
		p2_raw.scale3(stereo[1])
		for pixel in self._p1_info.processed:
			stereo[0].data[pixel[0]][pixel[1]][0] = 0
		self._p1_info.camera.getComponent(Image).fromNumpy(stereo[0].data)
		for pixel in self._p2_info.processed:
			stereo[1].data[pixel[0]][pixel[1]][1] = 0
		self._p2_info.camera.getComponent(Image).fromNumpy(stereo[1].data)

	def getResolution(self):
		return self._resolution

	def processInputDownEvent(self):
		pass

	def __init__(self, name):
		super(YuGame, self).__init__(name)
		self._info_width = 160
		self._camera_height = 160
		self._controls_height = 160

	def createPlayer(self, center, size):
		text_height = size.y - self._camera_height - self._controls_height
		text_y = - size.y / 2 + text_height / 2
		controls_y = text_y + text_height / 2 + self._controls_height / 2
		camera_y = controls_y + self._controls_height / 2 + self._camera_height / 2
		player = YuGame.PlayerInfo()
		player.background.getComponent(Transform).position = center
		player.background.getComponent(Rectangle).dimensions = size
		player.text.getComponent(Transform).position = center + Vector(0, text_y)
		player.text.getComponent(TextBox).width = self._info_width
		player.text.getComponent(TextBox).height = text_height
		controls_center = Vector(center.x, controls_y)
		controls_diff = 50
		player.up.getComponent(Transform).position = controls_center - Vector(0, controls_diff)
		player.down.getComponent(Transform).position = controls_center + Vector(0, controls_diff)
		player.right.getComponent(Transform).position = controls_center + Vector(controls_diff, 0)
		player.left.getComponent(Transform).position = controls_center - Vector(controls_diff, 0)
		player.camera.getComponent(Transform).position = center + Vector(0, camera_y)
		return player

	def setup(self):
		self._resolution = Renderer().getResolution() - Vector(self._info_width * 2, 0)
		p1_x = - (self._resolution.x / 2 + self._info_width / 2)
		p2_x = self._resolution.x / 2 + self._info_width / 2
		size = Vector(self._info_width, self._resolution.y)
		self._p1_info = self.createPlayer(Vector(p1_x, 0), size)
		self._p2_info = self.createPlayer(Vector(p2_x, 0), size)
		EventDispatcher().add_event_listener(InputDownEvent.TYPE, self.processInputDownEvent)
		EventDispatcher().add_event_listener(YImageEvent.TYPE, self.processYImageEvent)
		EventDispatcher().add_event_listener(LatencyEvent.TYPE, self.processLatencyEvent)
		EventDispatcher().add_event_listener(CameraResultEvent.TYPE, self.processCameraResultEvent)

