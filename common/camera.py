import picamera
import numpy as np

class BdCamera:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.camera = picamera.PiCamera()
        self.camera.resolution = (width, height)
        self.camera.shutter_speed = 250

    def createEmptyData(self):
        return np.empty(self.width * self.height * 3, dtype=np.uint8)

    def capture(self, data):
        self.camera.capture(data, use_video_port=True, format='yuv')
