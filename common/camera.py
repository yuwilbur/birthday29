import config
import numpy as np
import copy
import sys
try:
    import picamera
except ImportError:
    pass

class Camera:
    RESOLUTION_LO = (320, 160)
    RESOLUTION_MI = (640, 320)
    RESOLUTION_HI = (1280, 640)

    FILENAME = 'testcamera.npy'

    def __init__(self, resolution):
        self._resolution = resolution
        self._raw = self.createEmptyFullData()
        if not config.STILL_PHOTO and 'picamera' in sys.modules:
            self._camera = picamera.PiCamera()
            self._camera.resolution = resolution
            self._camera.shutter_speed = 500
            self._camera.awb_mode = 'off'
            self._camera.awb_gains = 1.0

    @staticmethod
    def rawToGrayscale(raw, grayscale):
        grayscale[0::3] = raw[0:raw.size / 3]
        grayscale[1::3] = raw[0:raw.size / 3]
        grayscale[2::3] = raw[0:raw.size / 3]

    @staticmethod
    def rawToY(raw, Y):
        Y[0::1] = raw[0:raw.size / 3]

    @staticmethod
    def YToGrayscale(Y, grayscale):
        grayscale[0::3] = Y
        grayscale[1::3] = Y
        grayscale[2::3] = Y

    def createEmptyYData(self):
        return np.empty(self._resolution[0] * self._resolution[1], dtype=np.uint8)

    def createEmptyFullData(self):
        return np.empty(self._resolution[0] * self._resolution[1] * 3, dtype=np.uint8)

    def capture(self):
        if not config.STILL_PHOTO and 'picamera' in sys.modules:
            self._camera.capture(self._raw, use_video_port=True, format='yuv')
        else:
            self._raw = np.load(Camera.FILENAME)
        return self._raw

    def close(self):
        if not config.STILL_PHOTO and 'picamera' in sys.modules:
            self._camera.close()
