from common.events import InputEvent
from common.periodSync import PeriodSync
import threading
import pygame

class InputThread(threading.Thread):
    def __init__(self, event_dispatcher):
        super(InputThread, self).__init__()
        self._stop_event = threading.Event()
        self._event_dispatcher = event_dispatcher

    def run(self):
        period_sync = PeriodSync()
        while not self._stop_event.is_set():
            period_sync.Start()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self._event_dispatcher.dispatch_event(InputEvent.ESCAPE)
                    if event.key == pygame.K_q:
                        self._event_dispatcher.dispatch_event(InputEvent.Q)
                    if event.key == pygame.K_UP:
                        self._event_dispatcher.dispatch_event(InputEvent.UP)
                    if event.key == pygame.K_DOWN:
                        self._event_dispatcher.dispatch_event(InputEvent.DOWN)
                    if event.key == pygame.K_RIGHT:
                        self._event_dispatcher.dispatch_event(InputEvent.RIGHT)
                    if event.key == pygame.K_LEFT:
                        self._event_dispatcher.dispatch_event(InputEvent.LEFT)
            period_sync.End()
            period_sync.Sync()
