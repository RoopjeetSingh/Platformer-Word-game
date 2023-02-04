from menu import menu
from opening_page import opening_page
import json
import pygame
import screen_size as ss

alpha = 0
root = pygame.display.set_mode((ss.SCREEN_WIDTH, ss.SCREEN_HEIGHT))
fbla_img = pygame.image.load("images/Menu_page/fbla_imagebg.png").convert_alpha()
fbla_img = pygame.transform.scale(fbla_img, (600/fbla_img.get_height()*fbla_img.get_width(), 600))
logo_img = pygame.image.load("images/Menu_page/logo.png").convert_alpha()
logo_img = pygame.transform.scale(logo_img, (400/logo_img.get_height()*logo_img.get_width(), 400))

clock = pygame.time.Clock()
show = True
while alpha >= 0:
    fbla_img.set_alpha(alpha)
    root.blit(fbla_img, (ss.SCREEN_WIDTH/2 - fbla_img.get_width()/2, ss.SCREEN_HEIGHT/2 - fbla_img.get_height()/2))
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            exit()
    if alpha >= 20:
        show = False
    if show:
        alpha += 0.1
    else:
        alpha -= 0.5
    pygame.display.flip()
    clock.tick(60)

root.fill((0, 0, 0))
pygame.display.flip()
alpha = 0
show = True
while alpha >= 0:
    logo_img.set_alpha(alpha)
    root.blit(logo_img, (ss.SCREEN_WIDTH/2 - logo_img.get_width()/2, ss.SCREEN_HEIGHT/2 - logo_img.get_height()/2))
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            exit()
    if alpha >= 20:
        show = False
    if show:
        alpha += 0.1
    else:
        alpha -= 0.5
    pygame.display.flip()
    clock.tick(60)


with open('variables.json', 'r') as f:
    var = json.load(f)
if var["1_time"] == "True":
    opening_page(root)
else:
    menu(root)
