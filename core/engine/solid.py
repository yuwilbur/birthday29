class Solid(object):
	def __init__(self):
		self._friction = 0

	def setFriction(self, friction):
		self._friction = friction

	def getFriction(self):
		return self._friction