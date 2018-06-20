import numpy as np
import picamera
import pygame
import pygame.camera
import time

WIDTH = 640
HEIGHT = 480

def y2rgb(y):
    rgb = np.empty((WIDTH,HEIGHT,3),dtype=np.uint8)
    rgb[:,:,2]=rgb[:,:,1]=rgb[:,:,0]=y
    return rgb

def testProcess(data):
    total = 0
    for i in range(0, data.size - 1):
        total += data.item(i)
    print("Test Process Total: %i" % total)

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))

camera = picamera.PiCamera()
camera.resolution = (WIDTH,HEIGHT)
camera.shutter_speed = 1200

camera_start = time.time()
data = np.empty((WIDTH,HEIGHT,3),dtype=np.uint8)
for foo in camera.capture_continuous(data, use_video_port=True, format='yuv'):
    camera_end = time.time()
    data.resize((WIDTH,HEIGHT), refcheck=False)

    process_start = time.time()
    testProcess(data)
    process_end = time.time()

    display_start = time.time()
    surface = pygame.image.frombuffer(y2rgb(data), (WIDTH, HEIGHT), 'RGB')
    screen.blit(surface, (0,0))
    pygame.display.update()
    display_end = time.time()

    camera_time = camera_end - camera_start
    process_time = process_end - process_start
    display_time = display_end - display_start
    print("Camera: %.3f, Process: %.3f, Display: %.3f" % (camera_time, process_time, display_time))
    data.resize((WIDTH,HEIGHT,3), refcheck=False)
    camera_start = time.time()
