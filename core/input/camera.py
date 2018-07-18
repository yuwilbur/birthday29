import copy
import numpy as np
import sys
try:
    import picamera
except ImportError:
    pass

class Image(object):
    def __init__(self, resolution, bits):
        super(Image, self).__init__()
        self.resolution = resolution
        self.bits = bits
        self.data = np.empty((resolution[0], resolution[1], bits), dtype=np.uint8)

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
            self._raw.data = self._raw.data.reshape(self._resolution[0] * self._resolution[1] * 3)
            self._camera.capture(self._raw.data, use_video_port=True, format='yuv')
            self._raw.data = self._raw.data.reshape((self._resolution[0], self._resolution[1], 3))
        else:
            self._raw.data = np.load(Camera.FILENAME)
        return self._raw.data

    def close(self):
        if 'picamera' in sys.modules:
            self._camera.close()

    @staticmethod
    def rawToGrayscale(raw, grayscale):
        grayscale.data = grayscale.data.reshape(grayscale.data.size)
        raw.data = raw.data.reshape(raw.data.size)
        grayscale.data[0::3] = raw.data[0:raw.data.size / 3]
        grayscale.data[1::3] = raw.data[0:raw.data.size / 3]
        grayscale.data[2::3] = raw.data[0:raw.data.size / 3]
        grayscale.data = grayscale.data.reshape((grayscale.resolution[0], grayscale.resolution[1], 3))
        raw.data = raw.data.reshape((raw.resolution[0], raw.resolution[1], 3))

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
        (stereo[0].data, stereo[1].data) = np.split(mono.data, 2)
        #stereo[0].data = mono.data[0:mono.data.size / 2]
        #stereo[1].data = mono.data[0:mono.data.size / 2]
