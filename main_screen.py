from menu import menu
from opening_page import opening_page
import json
import pygame
import screen_size as ss

root = pygame.display.set_mode((ss.SCREEN_WIDTH, ss.SCREEN_HEIGHT))
with open('variables.json', 'r') as f:
    var = json.load(f)
if var["1_time"] == "True":
    opening_page(root)
else:
    menu(root)