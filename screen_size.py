import os
import pygame

os.environ['SDL_VIDEO_CENTERED'] = '1'  # You have to call this before pygame.init()

pygame.init()

info = pygame.display.Info()  # You have to call this before pygame.display.set_mode()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w - 10, info.current_h - 120
tile_size = 50
