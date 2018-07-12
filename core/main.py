from .input.inputThread import InputThread
from .cameraThread import CameraThread
from .common.event import EventDispatcher
from .common.events import InputEvent
from .period_sync import PeriodSync
from .common.renderer import PygameRenderer
from .common import config
import sys

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

        cameraThread = CameraThread(event_dispatcher)
        cameraThread.setDaemon(True)
        cameraThread.start()
        
        period_sync = PeriodSync()
        self._running = True
        while(self._running):
            period_sync.Start()

            renderer.update()

            period_sync.End()
            period_sync.Sync()

        cameraThread.stop()
        cameraThread.join()
        inputThread.stop()
        inputThread.join()
    
    def processInputEvent(self, event):
        if event == InputEvent.ESCAPE:
            sys.exit()
        if event == InputEvent.Q:
            self._running = False
