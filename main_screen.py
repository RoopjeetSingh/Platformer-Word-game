from menu import menu
from opening_page import opening_page
import json_storer
import pygame
import screen_size as ss
from decode_file import decode_file
import smaller_store
import extra_images
import mp3file_storer
alpha = 0
root = pygame.display.set_mode((ss.SCREEN_WIDTH, ss.SCREEN_HEIGHT))
fbla_img = pygame.image.load(decode_file(smaller_store.fbla_logo)).convert_alpha()
fbla_img = pygame.transform.scale(fbla_img, (600/fbla_img.get_height()*fbla_img.get_width(), 600))
logo_img = pygame.image.load(decode_file(extra_images.var)).convert_alpha()
logo_img = pygame.transform.scale(logo_img, (400/logo_img.get_height()*logo_img.get_width(), 400))

clock = pygame.time.Clock()
pygame.mixer.music.load(decode_file(mp3file_storer.music))
pygame.mixer.music.set_volume(0.01)
pygame.mixer.music.play(-1)
show = True
while alpha >= 0:
    root.fill((0, 0, 0))
    fbla_img.set_alpha(alpha)
    root.blit(fbla_img, (ss.SCREEN_WIDTH/2 - fbla_img.get_width()/2, ss.SCREEN_HEIGHT/2 - fbla_img.get_height()/2))
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            exit()
    if alpha >= 255:
        show = False
    if show:
        alpha += 3
    else:
        alpha -= 3
    pygame.display.flip()
    clock.tick(60)

# root.fill((0, 0, 0))
pygame.display.flip()
alpha = 0
show = True
while alpha >= 0:
    root.fill((0, 0, 0))
    logo_img.set_alpha(alpha)
    root.blit(logo_img, (ss.SCREEN_WIDTH/2 - logo_img.get_width()/2, ss.SCREEN_HEIGHT/2 - logo_img.get_height()/2))
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            exit()
    if alpha >= 255:
        show = False
    if show:
        alpha += 3
    else:
        alpha -= 3
    pygame.display.flip()
    clock.tick(60)

# pygame.mixer.music.stop()
# pygame.mixer.music.load('images/Menu_page/Joshua McLean - Mountain Trials.mp3')
# pygame.mixer.music.play(-1)

var = json_storer.var
    
if var["1_time"] == "True":
    opening_page(root)
else:
    menu(root)
