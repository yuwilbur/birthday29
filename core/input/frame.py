import numpy as np

class Frame(object):
	def __init__(self, resolution=(0,0), bits=0):
		self.timestamp = 0
		self._resolution = resolution
		self._bits = bits
		self.data = self.createData(self._bits)

	def createData(self, scale = 1):
		return np.empty((self._resolution[0], self._resolution[1], self._bits * scale), dtype=np.uint8)

	def scale3(self, output):
		output.timestamp = self.timestamp
		if not output.data.size == self.data.size * 3:
			output.data = self.createData(3)
		output.data[:,:,0] = self.data[:,:,0]
		output.data[:,:,1] = self.data[:,:,0]
		output.data[:,:,2] = self.data[:,:,0]

	def split(self, left, right):
		temp_data = self.data.reshape((160,320,1))
		left.data, right.data = np.hsplit(temp_data, 2)
		left.timestamp = self.timestamp
		right.timestamp = self.timestamp