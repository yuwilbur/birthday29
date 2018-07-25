from ..common.event import EventDispatcher
from ..common.events import *
from ..games.game import Game
from ..renderer.renderer import Renderer
from ..engine.vector import Vector
from ..engine.primitive import Circle
from ..engine.primitive import Rectangle
from ..engine.material import Material
from ..engine.game_object import GameObject
from ..engine.ui import Image
from ..engine.ui import TextBox
from ..engine.transform import Transform
from ..input.frame import Frame

import time

class YuGame(Game):
	class PlayerInfo(object):
		def __init__(self):
			self.text = GameObject("text")
			self.text.addComponent(TextBox)
			self.camera = GameObject("camera")
			self.camera.addComponent(Image)
			self.processed = []
			radius = 25
			self.up = GameObject("up")
			self.up.addComponent(Circle)
			self.up.addComponent(Material)
			self.up.getComponent(Circle).radius = 25
			self.down = GameObject("down")
			self.down.addComponent(Circle)
			self.down.addComponent(Material)
			self.down.getComponent(Circle).radius = radius
			self.left = GameObject("left")
			self.left.addComponent(Circle)
			self.left.addComponent(Material)
			self.left.getComponent(Circle).radius = radius
			self.right = GameObject("right")
			self.right.addComponent(Circle)
			self.right.addComponent(Material)
			self.right.getComponent(Circle).radius = radius
			self.background = GameObject("background")
			self.background.addComponent(Rectangle)
			self.background.addComponent(Material)

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
		if not self._p1_info == None:
			for pixel in self._p1_info.processed:
				stereo[0].data[pixel[0]][pixel[1]][0] = 0
			self._p1_info.camera.getComponent(Image).fromNumpy(stereo[0].data)
		if not self._p2_info == None:
			for pixel in self._p2_info.processed:
				stereo[1].data[pixel[0]][pixel[1]][1] = 0
			self._p2_info.camera.getComponent(Image).fromNumpy(stereo[1].data)
		
	def getFullResolution(self):
		return self._full_resolution

	def getResolution(self):
		return self._resolution

	def __init__(self, name):
		super(YuGame, self).__init__(name)
		self._info_width = 160
		self._camera_height = 160
		self._controls_height = 160
		self._text_height = 0
		self._p1_info = None

	def createPlayer(self, top):
		text_y = self._text_height / 2
		controls_y = self._text_height + self._controls_height / 2
		camera_y = self._text_height + self._controls_height + self._camera_height / 2
		player = YuGame.PlayerInfo()
		#player.background.getComponent(Transform).position = top
		#player.background.getComponent(Rectangle).dimensions = Vector(self._info_width, 1000)
		player.camera.getComponent(Transform).position = top + Vector(0, camera_y)
		player.text.getComponent(Transform).position = top + Vector(0, text_y)
		player.text.getComponent(TextBox).width = self._info_width
		player.text.getComponent(TextBox).height = self._text_height
		player.up.getComponent(Transform).position = top + Vector(0, controls_y)
		return player

	def setup(self):
		self._full_resolution = Renderer().getResolution()
		self._resolution = self._full_resolution - Vector(self._info_width * 2, 0)
		self._text_height = self._full_resolution.y - self._camera_height - self._controls_height
		p1_x = - (self._info_width / 2 + self._resolution.x / 2)
		p2_x = self._info_width / 2 + self._resolution.x / 2
		top_y = - self._resolution.y / 2
		self._p1_info = self.createPlayer(Vector(p1_x, top_y))
		self._p2_info = self.createPlayer(Vector(p2_x, top_y))
		
		EventDispatcher().add_event_listener(YImageEvent.TYPE, self.processYImageEvent)
		EventDispatcher().add_event_listener(LatencyEvent.TYPE, self.processLatencyEvent)
		EventDispatcher().add_event_listener(CameraResultEvent.TYPE, self.processCameraResultEvent)

