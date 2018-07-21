from ..common.event import EventDispatcher
from ..common.events import GrayscaleImageEvent
from ..games.game import Game
from ..renderer.renderer import Renderer
from ..engine.vector import Vector
from ..engine.game_object import GameObject
from ..engine.ui import Image
from ..engine.transform import Transform

class YuGame(Game):
	class PlayerInfo(object):
		def __init__(self):
			self.info = GameObject("info")
			self.controls = GameObject("controls")
			self.camera = GameObject("camera")
			self.camera.addComponent(Image)

	def processGrayscaleImageEvent(self, event):
		self._p1_info.camera.getComponent(Image).fromNumpy(event.data()[0])

	def __init__(self, name):
		super(YuGame, self).__init__(name)
		self._info_width = 160
		self._camera_height = 160
		self._controls_height = 160
		self._text_height = 0

	def setup(self):
		full_resolution = Renderer().getResolution()
		self._text_height = full_resolution.y - self._camera_height - self._controls_height
		self._resolution = full_resolution - Vector(self._info_width * 2, 0)
		text_position = Vector(self._info_width / 2, self._text_height / 2)
		controls_position = Vector(self._info_width / 2, self._text_height + self._controls_height / 2)
		camera_position = Vector(self._info_width / 2, self._text_height + self._controls_height + self._camera_height / 2)
		self._p1_info = YuGame.PlayerInfo()
		self._p1_info.camera.getComponent(Transform).position = camera_position
		EventDispatcher().add_event_listener(GrayscaleImageEvent.TYPE, self.processGrayscaleImageEvent)
        

