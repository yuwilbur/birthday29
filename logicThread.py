from common.input import Input
from common.cameraProcess import CameraProcess
from common.periodSync import PeriodSync
import threading

class LogicThread(threading.Thread):
    def __init__(self, event_dispatcher):
        super(LogicThread, self).__init__()
        self._stop_event = threading.Event()
        self.input = Input(event_dispatcher)
        self.cameraProcess = CameraProcess(event_dispatcher)

    def stop(self):
        self._stop_event.set()

    def run(self):
        period_sync = PeriodSync()
        while(not self._stop_event.is_set()):
            period_sync.Start()
            self.input.update()
            self.cameraProcess.update()
            period_sync.End()
            period_sync.Sync()
