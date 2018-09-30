from ..common.event import EventDispatcher
from ..common.events import *
from ..games.game import Game
from ..renderer.renderer import Renderer
from ..engine.vector import Vector
from ..engine.primitive import Circle
from ..engine.primitive import Rectangle
from ..engine.material import *
from ..engine.game_object import GameObject
from ..engine.align import Align
from ..engine.line import Line
from ..engine.ui import Image
from ..engine.ui import TextBox
from ..engine.transform import Transform
from ..input.frame import Frame
from ..renderer.color import Color
from ..common import config

import time

class YuGame(Game):
	TROLL_INDEX = 0
	TROLL = [
		"THIS IS NOT PLAY TESTED",
		"HAPPY BIRTHDAY TO YU",
		"HAPPY BIRTHDAY TO YU!",
		"HAPPY BIRTHDAY TO WILBUR",
		"HAPPY BIRTHDAY TO YU!!",
		"",
		"Never gonna give you up",
		"Never gonna let you down",
		"Never gonna run around and desert you",
		"Never gonna make you cry",
		"Never gonna say goodbye",
		"Never gonna tell a lie and hurt you",
		"",
		"...",
		"Really?",
		"Are you still playing?",
		"Are you actually enjoying my game?",
		"If so, you're crazier than me",
		"...",
		"LEAVE ME ALONE!",
		"Ain't nobody got time for this",
		"BYE",
		"",
		"penis",
		"</end>",
		""
	]
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
			self.latency_text.getComponent(TextBox).align = Align.RIGHT
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
			self.up_key = up
			self.down_key = down
			self.left_key = left
			self.right_key = right
			self.up_pressed = False
			self.down_pressed = False
			self.left_pressed = False
			self.right_pressed = False
			self.controls = {
				self.up_key : (self.up, Color.LIGHT_BLUE, Color.DARK_BLUE),
				self.down_key : (self.down, Color.LIGHT_YELLOW, Color.DARK_YELLOW),
				self.left_key : (self.left, Color.LIGHT_GREEN, Color.DARK_GREEN),
				self.right_key : (self.right, Color.LIGHT_RED, Color.DARK_RED)
			}
			self.up.getComponent(LateMaterial).color = self.controls[up][2]
			self.down.getComponent(LateMaterial).color = self.controls[down][2]
			self.left.getComponent(LateMaterial).color = self.controls[left][2]
			self.right.getComponent(LateMaterial).color = self.controls[right][2]
			self.score = 0
			self.borders = []
			for x in range(0,100):
				border = GameObject("border")
				border.addComponent(Rectangle)
				border.addComponent(PostUIMaterial)
				border.getComponent(PostUIMaterial).color = Color.WHITE
				border.getComponent(PostUIMaterial).width = 2
				border.getComponent(Rectangle).dimensions = Vector(100,100)
				self.borders.append(border)


	def updatePlayer1Score(self):
		self._p1_info.game_text.getComponent(TextBox).setTexts([str(self._p1_info.score) + " "])

	def updatePlayer2Score(self):
		self._p2_info.game_text.getComponent(TextBox).setTexts([" " + str(self._p2_info.score)])

	def setGameTitle(self, texts):
		self._game_title.getComponent(TextBox).setTexts(texts)

	def onLatencyEvent(self, event):
		data = event.data()
		latency = str(int((time.time() - data[1]) * 1000))
		latency_type = data[0]
		if latency_type == LatencyEvent.P1_PROCESSING:
			self._p1_info.latency_text.getComponent(TextBox).setTexts([latency])
		elif latency_type == LatencyEvent.P2_PROCESSING:
			self._p2_info.latency_text.getComponent(TextBox).setTexts([latency])

	def onCameraResultEvent(self, event):
		result_type = event.data()[0]
		result = event.data()[1]
		if result_type == CameraResultEvent.P1:
			self._p1_info.processed = result
		elif result_type == CameraResultEvent.P2:
			self._p2_info.processed = result

	def onYImageEvent(self, event):
		def processPlayer(player, img):
			latency_text_transform = player.latency_text.getComponent(Transform)
			latency_text_textbox = player.latency_text.getComponent(TextBox)
			border_offset = latency_text_transform.position - Vector(latency_text_textbox.width, latency_text_textbox.height) / 2
			width = 2
			up_count = 0
			down_count = 0
			left_count = 0
			right_count = 0
			pixels = player.processed
			index = 0
			for index in range(index, len(player.borders)):
				if index < len(pixels):
					pixel = pixels[index]
					color = Color.RED
					if pixel.direction == Key.UP:
						up_count += 1
						color = Color.BLUE
					elif pixel.direction == Key.DOWN:
						down_count += 1
						color = Color.YELLOW
					elif pixel.direction == Key.LEFT:
						left_count += 1
						color = Color.GREEN
					elif pixel.direction == Key.RIGHT:
						right_count += 1
						color = Color.RED
					elif pixel.direction == Key.DEBUG:
						color = Color.ORANGE
					player.borders[index].getComponent(PostUIMaterial).color = color
					player.borders[index].getComponent(Transform).position = pixel.position + border_offset
					player.borders[index].getComponent(Rectangle).dimensions = pixel.size
				else:
					player.borders[index].getComponent(Rectangle).dimensions = Vector()
			if config.USE_CAMERA:
                                was_up_pressed = player.up_pressed
                                was_down_pressed = player.down_pressed
                                was_left_pressed = player.left_pressed
                                was_right_pressed = player.right_pressed
				if (up_count > down_count):
                                        player.up_pressed = True
                                        player.down_pressed = False
				elif (down_count > up_count):
                                        player.down_pressed = True
                                        player.up_pressed = False
				else:
                                        player.up_pressed = False
					player.down_pressed = False

				if (right_count > left_count):
                                        player.right_pressed = True
                                        player.left_pressed = False
				elif(left_count > right_count):
                                        player.left_pressed = True
                                        player.right_pressed = False
                                else:
                                        player.left_pressed = False
                                        player.right_pressed = False

                                def processKeyEvent(key_event, is_pressed, was_pressed):
                                        if is_pressed:
                                                if not was_pressed:
                                                        EventDispatcher().dispatch_event(KeyDownEvent(key_event))
                                                EventDispatcher().dispatch_event(KeyEvent(key_event))
                                        else:
                                                if was_pressed:
                                                        EventDispatcher().dispatch_event(KeyUpEvent(key_event))                                                

                                processKeyEvent(player.up_key, player.up_pressed, was_up_pressed)
                                processKeyEvent(player.down_key, player.down_pressed, was_down_pressed)
                                processKeyEvent(player.left_key, player.left_pressed, was_left_pressed)
                                processKeyEvent(player.right_key, player.right_pressed, was_right_pressed)
		
		p1_raw = event.data()[0]
		p2_raw = event.data()[1]
		stereo = [Frame(), Frame()]
		p1_raw.scale3(stereo[0])
		p2_raw.scale3(stereo[1])
		processPlayer(self._p1_info, stereo[0].data)
		self._p1_info.camera.getComponent(Image).fromNumpy(stereo[0].data)
		processPlayer(self._p2_info, stereo[1].data)
		self._p2_info.camera.getComponent(Image).fromNumpy(stereo[1].data)

	def updateTroll(self):
		self.TROLL_INDEX += 1
		if self.TROLL_INDEX == len(self.TROLL):
			return
		self.setGameTitle(["|",self.TROLL[self.TROLL_INDEX]])

	def onP1Score(self):
		self.updateTroll()
		self._p1_info.score += 1
		self.updatePlayer1Score()

	def onP2Score(self):
		self.updateTroll()
		self._p2_info.score += 1
		self.updatePlayer2Score()

	def getResolution(self):
		return self._resolution

	def getOffset(self):
		return self._offset

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
		game_text_height = self._info_width * 3 / 4
		latency_text_length = camera_length
		latency_text_width = latency_text_length
		latency_text_height = self._info_width
		if align == Align.RIGHT:
			camera_position = start + Vector(camera_length / 2, 0)
			controls_position = camera_position + Vector(camera_length / 2, 0) + Vector(controls_length / 2, 0)
			game_text_position = controls_position + Vector(controls_length / 2, 0) + Vector(game_text_length / 2, 0)
			latency_text_position = camera_position
			background_position = start + Vector((camera_length + controls_length + game_text_length) / 2, 0)
			text_align = Align.LEFT
		else:
			camera_position = start - Vector(camera_length / 2, 0)
			controls_position = camera_position - Vector(camera_length / 2, 0) - Vector(controls_length / 2, 0)
			game_text_position = controls_position - Vector(controls_length / 2, 0) - Vector(game_text_length / 2, 0)
			latency_text_position = camera_position
			background_position = start - Vector((camera_length + controls_length + game_text_length) / 2, 0)
			text_align = Align.RIGHT
		player = YuGame.PlayerInfo(up, down, left, right)
		player.background.getComponent(Transform).position = background_position
		player.background.getComponent(Rectangle).dimensions = Vector(length, self._info_width)
		player.latency_text.getComponent(Transform).position = latency_text_position
		player.latency_text.getComponent(TextBox).width = latency_text_width
		player.latency_text.getComponent(TextBox).height = latency_text_height
		player.latency_text.getComponent(TextBox).color = Color.GREY
		player.game_text.getComponent(Transform).position = game_text_position
		player.game_text.getComponent(TextBox).width = game_text_width
		player.game_text.getComponent(TextBox).height = game_text_height
		player.game_text.getComponent(TextBox).align = text_align
		player.game_text.getComponent(TextBox).font_size = self._font_size
		controls_diff = 50
		player.up.getComponent(Transform).position = controls_position - Vector(0, controls_diff)
		player.down.getComponent(Transform).position = controls_position + Vector(0, controls_diff)
		player.right.getComponent(Transform).position = controls_position + Vector(controls_diff, 0)
		player.left.getComponent(Transform).position = controls_position - Vector(controls_diff, 0)
		player.camera.getComponent(Transform).position = camera_position
		return player

	def start(self):
		pass

	def setup(self):
		self._font_size = 54
		self._offset = Vector(0, -self._info_width / 2)
		self._resolution = Renderer().getResolution() - Vector(0, self._info_width)
		p1_x = - self._resolution.x / 2
		p1_y = self._resolution.y / 2
		p2_x = self._resolution.x / 2
		p2_y = self._resolution.y / 2
		length = self._resolution.x / 2
		self._p1_info = self.createPlayer(Vector(p1_x, p1_y), Align.RIGHT, length, Key.W, Key.S, Key.A, Key.D)
		self._p2_info = self.createPlayer(Vector(p2_x, p2_y), Align.LEFT, length, Key.I, Key.K, Key.J, Key.L)
		EventDispatcher().add_event_listener(KeyEvent.TYPE, self.onMainKeyEvent)
		EventDispatcher().add_event_listener(KeyUpEvent.TYPE, self.onMainKeyUpEvent)
		EventDispatcher().add_event_listener(YImageEvent.TYPE, self.onYImageEvent)
		EventDispatcher().add_event_listener(LatencyEvent.TYPE, self.onLatencyEvent)
		EventDispatcher().add_event_listener(CameraResultEvent.TYPE, self.onCameraResultEvent)
		self._game_title = GameObject("main game text")
		self._game_title.addComponent(TextBox)
		self._game_title.getComponent(TextBox).font_size = self._font_size
		self._game_title.getComponent(TextBox).width = 1000
		self._game_title.getComponent(TextBox).height = self._info_width * 3 / 4
		self._game_title.getComponent(TextBox).align = Align.CENTER
		self._game_title.getComponent(Transform).position = Vector(0, p1_y)
		self.setGameTitle(["|",self.TROLL[self.TROLL_INDEX]])
		self.resetScore()

	def reset(self):
		pass

	def resetScore(self):
		self._p1_info.score = 0
		self.updatePlayer1Score()
		self._p2_info.score = 0
		self.updatePlayer2Score()

	def update(self):
		pass

	def onMainKeyUpEvent(self, event):
		key = event.data()
		if key in self._p1_info.controls:
			control = self._p1_info.controls[key]
			control[0].getComponent(LateMaterial).color = control[2]
		if key in self._p2_info.controls:
			control = self._p2_info.controls[key]
			control[0].getComponent(LateMaterial).color = control[2]

	def onMainKeyEvent(self, event):
		key = event.data()
		if key in self._p1_info.controls:
			control = self._p1_info.controls[key]
			control[0].getComponent(LateMaterial).color = control[1]
		if key in self._p2_info.controls:
			control = self._p2_info.controls[key]
			control[0].getComponent(LateMaterial).color = control[1]
		if key == Key.C:
			self.resetScore()

