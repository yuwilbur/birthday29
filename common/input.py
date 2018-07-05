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
                if event.key == pygame.K_q:
                    self.event_dispatcher.dispatch_event(InputEvent.Q)
                if event.key == pygame.K_UP:
                    self.event_dispatcher.dispatch_event(InputEvent.UP)
                if event.key == pygame.K_DOWN:
                    self.event_dispatcher.dispatch_event(InputEvent.DOWN)
                if event.key == pygame.K_RIGHT:
                    self.event_dispatcher.dispatch_event(InputEvent.RIGHT)
                if event.key == pygame.K_LEFT:
                    self.event_dispatcher.dispatch_event(InputEvent.LEFT)
