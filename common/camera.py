import picamera
import numpy as np

class BdCamera:
    def __init__(self, resolution):
        self.resolution = resolution
        self.camera = picamera.PiCamera()
        self.camera.resolution = resolution
        self.camera.shutter_speed = 500
        self.camera.awb_mode = 'off'
        self.camera.awb_gains = 1.0

    def createEmptyData(self):
        return np.empty(self.resolution[0] * self.resolution[1] * 3, dtype=np.uint8)

    def capture(self, data):
        self.camera.capture(data, use_video_port=True, format='yuv')

    def close(self):
        self.camera.close()
