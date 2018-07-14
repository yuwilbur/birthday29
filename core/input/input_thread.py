from ..common.event import EventDispatcher
from ..common.events import InputEvent
from ..input.camera_process import CameraProcess
from ..input.image_process import ImageProcess
from ..sync.period_sync import PeriodSync

import threading
import pygame

class InputThread(threading.Thread):
    def __init__(self):
        super(InputThread, self).__init__()
        self._stop_event = threading.Event()
        self._event_dispatcher = EventDispatcher()
        self._camera_process = CameraProcess(self._event_dispatcher)
        self._image_process = ImageProcess(self._event_dispatcher)
        self._key_map = {
            pygame.K_ESCAPE : InputEvent.ESCAPE,
            pygame.K_q : InputEvent.Q,
            pygame.K_UP : InputEvent.UP,
            pygame.K_DOWN : InputEvent.DOWN,
            pygame.K_RIGHT : InputEvent.RIGHT,
            pygame.K_LEFT : InputEvent.LEFT,
            pygame.K_RETURN : InputEvent.ENTER,
            pygame.K_w : InputEvent.W,
            pygame.K_a : InputEvent.A,
            pygame.K_s : InputEvent.S,
            pygame.K_d : InputEvent.D,
            pygame.K_i : InputEvent.I,
            pygame.K_j : InputEvent.J,
            pygame.K_k : InputEvent.K,
            pygame.K_l : InputEvent.L,
            pygame.K_1 : InputEvent.ONE,
        }

    def stop(self):
        self._stop_event.set()

    def run(self):
        period_sync = PeriodSync()
        while not self._stop_event.is_set():
            period_sync.Start()
            self._camera_process.update()
            self._image_process.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if  event.key in self._key_map:
                        self._event_dispatcher.dispatch_event(self._key_map[event.key])
                        print self._key_map[event.key].data()
            period_sync.End()
            period_sync.Sync()
        self._image_process.stop()
        self._camera_process.stop()
