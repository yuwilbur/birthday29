import copy
import numpy as np
import sys
try:
    import picamera
except ImportError:
    pass

class Image(object):
    def __init__(self, resolution, bits):
        self.resolution = resolution
        self.bits = bits
        self.data = np.empty(resolution[0] * resolution[1] * bits, dtype=np.uint8)

class Camera(object):
    RESOLUTION_LO = (320, 160)
    RESOLUTION_MI = (640, 320)
    RESOLUTION_HI = (1280, 640)

    FILENAME = './testcamera.npy'

    def __init__(self, resolution):
        self._resolution = resolution
        self._raw = Image(self._resolution, 3)
        if 'picamera' in sys.modules:
            self._camera = picamera.PiCamera()
            self._camera.resolution = resolution
            self._camera.shutter_speed = 500
            self._camera.awb_mode = 'off'
            self._camera.awb_gains = 1.0

    def capture(self):
        if 'picamera' in sys.modules:
            self._camera.capture(self._raw, use_video_port=True, format='yuv')
        else:
            self._raw = np.load(Camera.FILENAME)
        return self._raw

    def close(self):
        if 'picamera' in sys.modules:
            self._camera.close()

    @staticmethod
    def rawToGrayscale(raw, grayscale):
        grayscale.data[0::3] = raw.data[0:raw.data.size / 3]
        grayscale.data[1::3] = raw.data[0:raw.data.size / 3]
        grayscale.data[2::3] = raw.data[0:raw.data.size / 3]

    @staticmethod
    def rawToY(raw, Y):
        Y.data[0::1] = raw.data[0:raw.data.size / 3]

    @staticmethod
    def YToGrayscale(Y, grayscale):
        grayscale.data[0::3] = Y.data
        grayscale.data[1::3] = Y.data
        grayscale.data[2::3] = Y.data

    @staticmethod
    def monoToStereo(mono, stereo):
        stereo = np.split(mono, 2)
