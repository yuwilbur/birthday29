from ..common.event import EventDispatcher
from ..common.events import *
from ..input.camera_process import CameraProcess
from ..input.image_process import ImageProcess
from ..sync.manager import Manager

import pygame

class InputManager(Manager):
    class Key(object):
        def __init__(self, key):
            self.key = key
            self.pressed = False

    def __init__(self):
        super(InputManager, self).__init__()
        self._event_dispatcher = EventDispatcher()
        self._camera_process = CameraProcess(self._event_dispatcher)
        self._image_process = ImageProcess(self._event_dispatcher)
        
        self._key_map = {
            pygame.K_ESCAPE : InputManager.Key(Key.ESCAPE),
            pygame.K_q : InputManager.Key(Key.Q),
            pygame.K_UP : InputManager.Key(Key.UP),
            pygame.K_DOWN : InputManager.Key(Key.DOWN),
            pygame.K_RIGHT : InputManager.Key(Key.RIGHT),
            pygame.K_LEFT : InputManager.Key(Key.LEFT),
            pygame.K_RETURN : InputManager.Key(Key.ENTER),
            pygame.K_w : InputManager.Key(Key.W),
            pygame.K_a : InputManager.Key(Key.A),
            pygame.K_s : InputManager.Key(Key.S),
            pygame.K_d : InputManager.Key(Key.D),
            pygame.K_i : InputManager.Key(Key.I),
            pygame.K_j : InputManager.Key(Key.J),
            pygame.K_k : InputManager.Key(Key.K),
            pygame.K_l : InputManager.Key(Key.L),
            pygame.K_1 : InputManager.Key(Key.NUM_1)
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
                    if not self._key_map[event.key].pressed:
                        self._event_dispatcher.dispatch_event(KeyDownEvent(self._key_map[event.key].key))
                        print self._key_map[event.key].key + " down"
                    self._key_map[event.key].pressed = True
                    self._event_dispatcher.dispatch_event(KeyEvent(self._key_map[event.key].key))
                    print self._key_map[event.key].key
            elif event.type == pygame.KEYUP:
                if event.key in self._key_map:
                    self._event_dispatcher.dispatch_event(KeyUpEvent(self._key_map[event.key].key))
                    self._key_map[event.key].pressed = False
                    print self._key_map[event.key].key + " up"
        self._camera_process.update()
        self._image_process.update()
