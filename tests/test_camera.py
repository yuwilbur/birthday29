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

data = np.empty((WIDTH,HEIGHT,3),dtype=np.uint8)

while(True):
    total_start = time.time()

    camera_start = time.time()
    data = np.empty((WIDTH,HEIGHT,3),dtype=np.uint8)
    camera.capture(data, use_video_port=True, format='yuv')
    data.resize((WIDTH,HEIGHT))
    camera_end = time.time()

    process_start = time.time()
    testProcess(data)
    process_end = time.time()

    display_start = time.time()
    surface = pygame.image.frombuffer(y2rgb(data), (WIDTH, HEIGHT), 'RGB')
    screen.blit(surface, (0,0))
    pygame.display.update()
    display_end = time.time()

    total_end = time.time()
    
    total_time = total_end - total_start
    camera_time = camera_end - camera_start
    process_time = process_end - process_start
    display_time = display_end - display_start
    print("Total: %.3f, Camera: %.3f, Process: %.3f, Display: %.3f" % (total_time, camera_time, process_time, display_time))
