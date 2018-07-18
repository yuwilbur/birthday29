import copy
import numpy as np
import sys
try:
    import picamera
except ImportError:
    pass

class Camera(object):
    RESOLUTION_LO = (320, 160)
    RESOLUTION_MI = (640, 320)
    RESOLUTION_HI = (1280, 640)
    TEST = True

    FILENAME = './testcamera.npy'

    def __init__(self, resolution):
        self._resolution = resolution
        self._raw = self.createImage(self._resolution, 3)
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
        return self._raw.flatten()[0:self._raw.size/3].reshape((self._resolution[0], self._resolution[1], 1))

    def close(self):
        if 'picamera' in sys.modules:
            self._camera.close()

    @staticmethod
    def createImage(resolution, bits):
        return np.empty((resolution[0], resolution[1], bits), dtype=np.uint8)

    @staticmethod
    def yToGrayscale(y, grayscale):
        grayscale[:,:,0] = y[:,:,0]
        grayscale[:,:,1] = y[:,:,0]
        grayscale[:,:,2] = y[:,:,0]

    @staticmethod
    def monoToStereo(mono, stereo):
        mono = mono.reshape((160,320,1))
        stereo[0], stereo[1] = np.hsplit(mono, 2)
