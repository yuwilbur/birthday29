from ..common.events import RGBImageEvent
from ..sync.period_sync import PeriodSync

import pygame
import threading

class Renderer(threading.Thread):
    __instance = None

    @staticmethod
    def getInstance():
        return Renderer.__instance

    def __init__(self, event_dispatcher):
        super(Renderer, self).__init__()
        if Renderer.__instance != None:
            raise Exception("This class is a singleton")
        Renderer.__instance = self

        self._stop_event = threading.Event()
        self._event_dispatcher = event_dispatcher

    def stop(self):
        self._stop_event.set()

    def run(self):
        #screen_attributes = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
        screen_attributes = 0
        display_info = pygame.display.Info()
        self._resolution = (display_info.current_w, display_info.current_h)
        self._screen = pygame.display.set_mode(self._resolution, screen_attributes)
        self._event_dispatcher.add_event_listener(RGBImageEvent.TYPE, self.processRGBImageEvent)
        self._surface = None

        period_sync = PeriodSync()
        while not self._stop_event.is_set():
            period_sync.Start()
            if not self._surface == None:
                self._screen.blit(self._surface, (0,0), (0,0,self._surface.get_width(),self._surface.get_height()))
            pygame.display.update()
            period_sync.End()
            period_sync.Sync()

    def processRGBImageEvent(self, event):
            self._surface = pygame.image.frombuffer(event.data()[0], event.data()[1], 'RGB')

    
        
