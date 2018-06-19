import io
import picamera
import pygame
import time
import numpy

WIDTH = 960
HEIGHT = 480

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))

camera = picamera.PiCamera()
camera.resolution = (WIDTH,HEIGHT)
camera.framerate = 30
camera.shutter_speed = 1000
camera.crop = (0.0, 0.0, 1.0, 1.0)

x = (screen.get_width() - camera.resolution[0]) / 2
y = (screen.get_height() - camera.resolution[1]) / 2

data = numpy.empty((WIDTH, HEIGHT, 3), dtype=numpy.uint8);

while(True):
    start = time.time()
    camera.capture(data, use_video_port=True, format='rgb')
    screen.blit(pygame.image.frombuffer(data, (WIDTH, HEIGHT), 'RGB'), (x,y))
    pygame.display.update()
    finish = time.time()
    print("Time: %.2f" % (finish - start))
