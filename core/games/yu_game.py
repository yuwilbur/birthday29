from ..common.event import EventDispatcher
from ..common.events import GrayscaleImageEvent
from ..games.game import Game
from ..renderer.renderer import Renderer
from ..engine.vector import Vector

class YuGame(Game):
	class PlayerInfo(object):
		def __init__(self):
			self.info = None
			self.controls = None
			self.camera = None

	def processGrayscaleImageEvent(self, event):
		resolution = (event.data()[0].shape[0], event.data()[0].shape[1])

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
		EventDispatcher().add_event_listener(GrayscaleImageEvent.TYPE, self.processGrayscaleImageEvent)
        

