from ..games.game import Game 

class TestGame(Game):
	def __init__(self, event_dispatcher):
		super(TestGame, self).__init__(event_dispatcher, "TestGame")

	def setup(self):
		return

	def update(self):
		print '1'