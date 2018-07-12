from .camera_process import CameraProcess
from .period_sync import PeriodSync
from .image_process import ImageProcess
import threading
import time

def captureCamera(pipe):
    main_pipe, worker_pipe = pipe
    main_pipe.close()

class CameraThread(threading.Thread):
    def __init__(self, event_dispatcher):
        super(CameraThread, self).__init__()
        self._stop_event = threading.Event()
        self._event_dispatcher = event_dispatcher
        self._camera_process = CameraProcess(self._event_dispatcher)
        self._image_processor = ImageProcess(self._event_dispatcher)

    def stop(self):
        self._stop_event.set()

    def run(self):
        period_sync = PeriodSync()
        while not self._stop_event.is_set():
            period_sync.Start()
            self._camera_process.update()
            period_sync.End()
            period_sync.Sync()