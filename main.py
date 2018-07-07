from inputThread import InputThread
from cameraThread import CameraThread
from common.event import EventDispatcher
from common.events import InputEvent
from common.periodSync import PeriodSync
from common.renderer import PygameRenderer
import sys

class Birthday29():
    def run(self):
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

if (__name__ == "__main__"):
    Birthday29().run()
