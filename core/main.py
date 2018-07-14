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
        self.run()

    def setupConfig(self):
        config.STILL_PHOTO = False

    def run(self):
        self.setupConfig()
        pygame.init()

        event_dispatcher = EventDispatcher()
        event_dispatcher.add_event_listener(InputEvent.TYPE, self.processInputEvent)

        inputManager = InputManager()
        gameEngine = GameEngine()

        self._renderer = Renderer()
        self._renderer.setDaemon(True)
        self._renderer.start()

        self._gameManager = GameManager()

        self._running = True
        period_sync = PeriodSync()
        while self._running:
            period_sync.Start()
            inputManager.update()
            gameEngine.update()
            period_sync.End()
            period_sync.Sync()

        inputManager.stop()
        self._renderer.join()

        pygame.quit()
    
    def processInputEvent(self, event):
        if event == InputEvent.ESCAPE:
            while True:
                os.kill(os.getpid(), signal.SIGINT)
                time.sleep(0.5)
        if event == InputEvent.Q:
            self._running = False
            self._gameManager.stopGame()
            self._renderer.stop()
