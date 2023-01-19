from player import *
# from Level import *
import screen_size as ss
import json
from helpful_functions import calculate_current_level

pygame.init()


def platformer_game(screen):
    pressed = False
    with open('variables.json', 'r') as f:
        var = json.load(f)

    current_level = calculate_current_level(var)
    clock = pygame.time.Clock()
    player = Player(ss.tile_size, ss.tile_size, var["users"][var["current_user"][0]][2])
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

        player.kill_self()
        player.gravity(current_level)
        player.collect_letter(current_level)
        player.collect_power_up(current_level)

        if not player.kill_player:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player.move_right(current_level, "right")
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player.move_right(current_level, "left")
            else:
                player.move_right(current_level, "")

            if keys[pygame.K_UP] or keys[pygame.K_SPACE] or keys[pygame.K_w]:
                if player.on_ground or pressed:
                    player.jumping = True
                    pressed = True
            else:
                pressed = False
        player.jump(current_level)
        for i in player.letter_lis:
            i.collect_self(player, current_level)
            screen.blit(i.image, i.rect)
        for i in player.mystery_letter_lis:
            i.collect_self(player, current_level)
            screen.blit(i.image, i.rect)
        for i in player.power_up_lis:
            i.collect_self(player, current_level)
            screen.blit(i.image, i.rect)
            i.time_bar(screen, player, current_level)
        pygame.display.update()
        clock.tick(75)


if __name__ == "__main__":
    root = pygame.display.set_mode((ss.SCREEN_WIDTH, ss.SCREEN_HEIGHT))
    platformer_game(root)
