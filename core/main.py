from .common import config
from .common.event import EventDispatcher
from .common.events import InputEvent
from .engine.game_engine import GameEngine
from .games.game_manager import GameManager
from .input.input_manager import InputManager
from .renderer.renderer import Renderer
from .sync.period_sync import PeriodSync

import os
import pygame
import signal
import time

class Main(object):
    def __init__(self):
        self.setupConfig()
        self.run()

    def setupConfig(self):
        config.STILL_PHOTO = False

    def run(self):
        pygame.init()

        event_dispatcher = EventDispatcher()
        event_dispatcher.add_event_listener(InputEvent.TYPE, self.processInputEvent)

        managers = [
            InputManager(),
            GameManager(),
            GameEngine(),
            Renderer(),
        ]

        for manager in managers:
            manager.setup()

        self._running = True
        period_sync = PeriodSync()
        while self._running:
            period_sync.Start()
            for manager in managers:
                manager.update()
            period_sync.End()
            period_sync.Sync()

        for manager in managers:
            manager.stop()

        pygame.quit()
    
    def processInputEvent(self, event):
        if event == InputEvent.Q:
            self._running = False
