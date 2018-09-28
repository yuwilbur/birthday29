from .common import config
from .common.event import EventDispatcher
from .common.events import *
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
    def setFullScreen(self, enable):
        config.FULL_SCREEN = enable

    def run(self):
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.mixer.init()
        pygame.init()

        EventDispatcher().add_event_listener(KeyDownEvent.TYPE, self.onKeyDownEvent)

        managers1 = [
            InputManager(),
            GameManager(),
            GameEngine(),
        ]
        managers2 = [
            Renderer()
        ]

        for manager in managers1:
            manager.setup()
        for manager in managers2:
            manager.setup()

        self._running = True
        period_sync1 = PeriodSync()
        period_sync2 = PeriodSync()
        while self._running:
            period_sync1.Start()
            for manager in managers1:
                manager.update()
            period_sync1.End()
            period_sync1.Sync()
            period_sync2.Start()
            for manager in managers2:
                manager.update()
            period_sync2.End()
            period_sync2.Sync()

        for manager in managers1:
            manager.stop()
        for manager in managers2:
            manager.stop()

        pygame.quit()
    
    def onKeyDownEvent(self, event):
        if event.data() == Key.Q:
            self._running = False
