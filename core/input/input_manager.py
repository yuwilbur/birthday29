from ..common.event import EventDispatcher
from ..common.events import *
from ..input.camera_process import CameraProcess
from ..input.image_process import ImageProcess
from ..sync.manager import Manager

import pygame

class InputManager(Manager):
    def __init__(self):
        super(InputManager, self).__init__()
        self._event_dispatcher = EventDispatcher()
        self._camera_process = CameraProcess(self._event_dispatcher)
        self._image_process = ImageProcess(self._event_dispatcher)
        
        self._key_map = {
            pygame.K_ESCAPE : Key.ESCAPE,
            pygame.K_q : Key.Q,
            pygame.K_UP : Key.UP,
            pygame.K_DOWN : Key.DOWN,
            pygame.K_RIGHT : Key.RIGHT,
            pygame.K_LEFT : Key.LEFT,
            pygame.K_RETURN : Key.ENTER,
            pygame.K_w : Key.W,
            pygame.K_a : Key.A,
            pygame.K_s : Key.S,
            pygame.K_d : Key.D,
            pygame.K_i : Key.I,
            pygame.K_j : Key.J,
            pygame.K_k : Key.K,
            pygame.K_l : Key.L,
            pygame.K_1 : Key.NUM_1,
        }

    def setup(self):
        interval = 10
        pygame.key.set_repeat(interval, interval)

    def stop(self):
        self._image_process.stop()
        self._camera_process.stop()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in self._key_map:
                    self._event_dispatcher.dispatch_event(KeyDownEvent(self._key_map[event.key]))
                    print self._key_map[event.key] + " down"
            elif event.type == pygame.KEYUP:
                if event.key in self._key_map:
                    self._event_dispatcher.dispatch_event(KeyUpEvent(self._key_map[event.key]))
                    print self._key_map[event.key] + " up"
        self._camera_process.update()
        self._image_process.update()
