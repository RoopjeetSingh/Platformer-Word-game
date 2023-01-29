from player import *
from Level import *
import screen_size as ss
import json
from helpful_functions import calculate_current_level

pygame.init()


def platformer_game(screen, current_level=None):
    pressed = False
    with open('variables.json', 'r') as f:
        var = json.load(f)

    current_level = current_level or calculate_current_level(var)
    clock = pygame.time.Clock()
    player = Player(ss.tile_size, ss.tile_size*2, var["users"][var["current_user"][0]][2])
    while True:
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

        pressed = player.update_player(screen, current_level, pressed)
        pygame.display.update()
        clock.tick(90)


if __name__ == "__main__":
    root = pygame.display.set_mode((ss.SCREEN_WIDTH, ss.SCREEN_HEIGHT))
    platformer_game(root, level5)
