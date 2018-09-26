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

    FILENAME = './testcamera2.npy'

    def __init__(self, resolution):
        self._resolution = resolution
        self._raw = np.empty((resolution[0] * resolution[1] * 3), dtype=np.uint8)
        self._y_shape = (self._resolution[0], self._resolution[1], 1)
        if 'picamera' in sys.modules:
            self._camera = picamera.PiCamera()
            self._camera.resolution = resolution
            self._camera.shutter_speed = 2500
            self._camera.awb_mode = 'off'
            self._camera.awb_gains = 1.0
            self._camera.vflip = True

    def capture(self):
        if 'picamera' in sys.modules:
            self._camera.capture(self._raw, use_video_port=True, format='yuv')
            return self._raw[0:self._raw.size/3].reshape(self._y_shape)
        else:
            return np.load(Camera.FILENAME)

    def close(self):
        if 'picamera' in sys.modules:
            self._camera.close()
