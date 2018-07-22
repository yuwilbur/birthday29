import numpy as np

class Frame(object):
	def __init__(self, resolution=(0,0), bits=0):
		self.timestamp = 0
		self.data = None
		self.init(resolution, bits)

	def init(self, resolution, bits):
		self.data = np.empty((resolution[0], resolution[1], bits), dtype=np.uint8)

	def scale(self, output, scale = 3):
		output.timestamp = self.timestamp
		for i in range(scale):
			output.data[:,:,i] = self.data[:,:,0]

	def split(self, left, right):
		temp_data = self.data.reshape((160,320,1))
		left.data, right.data = np.hsplit(temp_data, 2)
		left.timestamp = self.timestamp
		right.timestamp = self.timestamp