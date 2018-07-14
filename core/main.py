from .common import config
from .common.event import EventDispatcher
from .common.events import InputEvent
from .engine.game_engine import GameEngine
from .games.game_manager import GameManager
from .input.input_thread import InputThread
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

        self._inputThread = InputThread()
        self._inputThread.setDaemon(True)
        self._inputThread.start()

        gameEngine = GameEngine()

        self._renderer = Renderer()
        self._renderer.setDaemon(True)
        self._renderer.start()

        self._gameManager = GameManager()

        self._running = True
        period_sync = PeriodSync()
        while self._running:
            period_sync.Start()
            gameEngine.update(period_sync.getPeriod())
            period_sync.End()
            period_sync.Sync()

        self._inputThread.join()
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
            self._inputThread.stop()
            self._renderer.stop()
