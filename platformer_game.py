import pygame

from player import *
from Level import *
import screen_size as ss
import json
from helpful_functions import calculate_current_level
import time
from wordconnect import game_Loop_Wordle
from datetime import time as time_str

pygame.init()


def platformer_game(screen, current_level=None):
    def empty_screen():
        start_color = 150
        while start_color >= 0:
            screen.fill((start_color, start_color, start_color))
            start_color -= 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    exit()
            clock.tick()
            pygame.display.flip()
        game_Loop_Wordle(screen, [letter_obj.letter for letter_obj in player.letter_lis],
                         len(player.mystery_letter_lis))

    pressed = False
    with open('variables.json', 'r') as f:
        var = json.load(f)

    current_level = current_level or calculate_current_level(var)
    show_time = current_level.time
    show_time_actual = time.time()
    clock = pygame.time.Clock()
    player = Player(ss.tile_size, ss.tile_size * 2, var["users"][var["current_user"][0]][2])
    font = pygame.font.SysFont("images/Menu_page/SnowtopCaps.ttf", 75, bold=True)
    while True:
        show_time -= round(time.time() - show_time_actual)
        show_time_actual = time.time()
        current_level.draw(screen)
        current_level.obstruct_group.draw(screen)
        current_level.platform_group.draw(screen)
        current_level.letter_group.draw(screen)
        current_level.power_up_group.draw(screen)
        for i in current_level.letter_group:
            i.bounce_brighten()

        for i in current_level.power_up_group:
            i.bounce_brighten()

        screen.blit(player.image, player.rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                exit()

        pressed, killed = player.update_player(screen, current_level, pressed)
        if killed:
            empty_screen()

        print(show_time)
        time_as_str = time_str(minute=show_time // 60, second=show_time % 60)
        time_surface = font.render(str(time_as_str), True, (20, 20, 20))
        time_surface.set_alpha(200)
        screen.blit(time_surface, (ss.SCREEN_WIDTH - time_surface.get_width() - ss.tile_size, ss.tile_size))
        pygame.display.update()
        clock.tick(90)


if __name__ == "__main__":
    root = pygame.display.set_mode((ss.SCREEN_WIDTH, ss.SCREEN_HEIGHT))
    platformer_game(root, level3)
