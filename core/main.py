from .common import config
from .common.event import EventDispatcher
from .common.events import InputEvent
from .engine.game_engine import GameEngine
from .input.input_thread import InputThread
from .renderer.renderer import Renderer
from .sync.period_sync import PeriodSync

import os
import pygame
import signal
import time

class Main():
    def __init__(self):
        self.run()

    def setupConfig(self):
        config.STILL_PHOTO = False

    def run(self):
        self.setupConfig()
        pygame.init()

        event_dispatcher = EventDispatcher()
        event_dispatcher.add_event_listener(InputEvent.TYPE, self.processInputEvent)

        self._inputThread = InputThread(event_dispatcher)
        self._inputThread.setDaemon(True)
        self._inputThread.start()

        self._gameEngine = GameEngine(event_dispatcher)
        self._gameEngine.setDaemon(True)
        self._gameEngine.start()

        self._renderer = Renderer(event_dispatcher)
        self._renderer.setDaemon(True)
        self._renderer.start()

        self._inputThread.join()
        self._gameEngine.join()
        self._renderer.join()

        pygame.quit()
    
    def processInputEvent(self, event):
        if event == InputEvent.ESCAPE:
            while True:
                os.kill(os.getpid(), signal.SIGINT)
                time.sleep(0.5)
        if event == InputEvent.Q:
            self._inputThread.stop()
            self._gameEngine.stop()
            self._renderer.stop()
