from inputEvent import InputEvent
import pygame
import sys

class Input():
    def __init__(self, event_dispatcher):
        self.event_dispatcher = event_dispatcher

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.event_dispatcher.dispatch_event(InputEvent.ESCAPE)
                if event.key == pygame.K_t:
                    print 'Test'
