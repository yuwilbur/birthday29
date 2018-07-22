from ..common.event import EventDispatcher
from ..common.events import *
from ..games.game import Game
from ..renderer.renderer import Renderer
from ..engine.vector import Vector
from ..engine.game_object import GameObject
from ..engine.ui import Image
from ..engine.ui import TextBox
from ..engine.transform import Transform

import time

class YuGame(Game):
	class PlayerInfo(object):
		def __init__(self):
			self.text = GameObject("text")
			self.text.addComponent(TextBox)
			self.controls = GameObject("controls")
			self.camera = GameObject("camera")
			self.camera.addComponent(Image)

	def processGrayscaleImageEvent(self, event):
		self._p1_info.camera.getComponent(Image).fromNumpy(event.data()[0].data)
		self._p2_info.camera.getComponent(Image).fromNumpy(event.data()[1].data)

	def processInputEvent(self, event):
		return

	def processLatencyEvent(self, event):
		data = event.data()
		latency = str((time.time() - data[1]) * 1000)
		if data[0] == LatencyEvent.P1_PROCESSING:
			self._p1_info.text.getComponent(TextBox).text = latency

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

	def setup(self):
		self._full_resolution = Renderer().getResolution()
		self._resolution = self._full_resolution - Vector(self._info_width * 2, 0)
		self._text_height = self._full_resolution.y - self._camera_height - self._controls_height
		text_y = self._text_height / 2
		controls_y = self._text_height + self._controls_height / 2
		camera_y = self._text_height + self._controls_height + self._camera_height / 2
		p1_x = self._info_width / 2
		p2_x = self._full_resolution.x - self._info_width / 2
		self._p1_info = YuGame.PlayerInfo()
		self._p1_info.camera.getComponent(Transform).position = Vector(p1_x, camera_y)
		self._p1_info.text.getComponent(Transform).position = Vector(p1_x, text_y)
		self._p1_info.text.getComponent(TextBox).width = self._info_width
		self._p1_info.text.getComponent(TextBox).height = self._text_height
		self._p2_info = YuGame.PlayerInfo()
		self._p2_info.camera.getComponent(Transform).position = Vector(p2_x, camera_y)
		self._p2_info.text.getComponent(Transform).position = Vector(p2_x, text_y)
		self._p2_info.text.getComponent(TextBox).width = self._info_width
		self._p2_info.text.getComponent(TextBox).height = self._text_height
		self._p2_info.text.getComponent(TextBox).text = "Player 2"
		EventDispatcher().add_event_listener(GrayscaleImageEvent.TYPE, self.processGrayscaleImageEvent)
		EventDispatcher().add_event_listener(InputEvent.TYPE, self.processInputEvent)
		EventDispatcher().add_event_listener(LatencyEvent.TYPE, self.processLatencyEvent)
        

