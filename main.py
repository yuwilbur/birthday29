from common.camera import Camera
from common.input import Input
from common.debug import Debugger
from common.debug import PerformanceLogger
from logicThread import LogicThread
from common.event import EventDispatcher
from common.inputEvent import InputEvent
from common.periodSync import PeriodSync
from common.renderer import PygameRenderer
import sys

class Birthday29():
    def run(self):
        event_dispatcher = EventDispatcher()
        event_dispatcher.add_event_listener(InputEvent.TYPE, self.processInputEvent)

        inputProcess = Input(event_dispatcher)
        renderer = PygameRenderer(event_dispatcher, Camera.RESOLUTION_HI)
        logicThread = LogicThread(event_dispatcher)
        logicThread.setDaemon(True)
        logicThread.start()
        
        period_sync = PeriodSync()
        self._running = True
        while(self._running):
            period_sync.Start()

            inputProcess.update()
            renderer.update()

            period_sync.End()
            period_sync.Sync()

        logicThread.stop()
        logicThread.join()
    
    def processInputEvent(self, event):
        if event == InputEvent.ESCAPE:
            sys.exit()
        if event == InputEvent.Q:
            self._running = False

if (__name__ == "__main__"):
    Birthday29().run()
