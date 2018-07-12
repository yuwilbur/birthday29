from .common import config
from .common.event import EventDispatcher
from .common.events import InputEvent
from .input.input_thread import InputThread
from .renderer.renderer import PygameRenderer
from .sync.period_sync import PeriodSync

import os
import signal
import time

class Main():
    def __init__(self):
        self.run()

    def run(self):
        config.STILL_PHOTO = True
        event_dispatcher = EventDispatcher()
        event_dispatcher.add_event_listener(InputEvent.TYPE, self.processInputEvent)

        renderer = PygameRenderer(event_dispatcher)

        inputThread = InputThread(event_dispatcher)
        inputThread.setDaemon(True)
        inputThread.start()
        
        period_sync = PeriodSync()
        self._running = True
        while(self._running):
            period_sync.Start()

            renderer.update()

            period_sync.End()
            period_sync.Sync()

        inputThread.stop()
        inputThread.join()
    
    def processInputEvent(self, event):
        if event == InputEvent.ESCAPE:
            while True:
                os.kill(os.getpid(), signal.SIGINT)
                time.sleep(0.5)
        if event == InputEvent.Q:
            self._running = False
