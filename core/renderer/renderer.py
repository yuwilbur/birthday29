from ..common.events import RGBImageEvent

import pygame

class PygameRenderer():
    def __init__(self, event_dispatcher):
        self._event_dispatcher = event_dispatcher
        pygame.init()
        #screen_attributes = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
        screen_attributes = 0
        display_info = pygame.display.Info()
        self._resolution = (display_info.current_w, display_info.current_h)
        self._screen = pygame.display.set_mode(self._resolution, screen_attributes)
        self._event_dispatcher.add_event_listener(RGBImageEvent.TYPE, self.processRGBImageEvent)
        self._surface = None

    def __del__(self):
        pygame.quit()

    def update(self):
        if not self._surface == None:
            self._screen.blit(self._surface, (0,0), (0,0,self._surface.get_width(),self._surface.get_height()))
        pygame.display.update()

    def processRGBImageEvent(self, event):
            self._surface = pygame.image.frombuffer(event.data()[0], event.data()[1], 'RGB')

    
        
