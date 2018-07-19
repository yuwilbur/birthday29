from ..games.game import Game
from ..renderer.renderer import Renderer
from ..engine.vector import Vector

class YuGame(Game):
	class PlayerInfo(object):
		def __init__(self):
			self.info = None
			self.controls = None
			self.camera = None

	def __init__(self, name):
		super(YuGame, self).__init__(name)
		self._info_width = 160
		self._camera_height = 0
		self._controls_height = 0
		self._text_height = 0

	def setup(self):
		self._resolution = Renderer().getResolution() - Vector(self._info_width * 2, 0)

