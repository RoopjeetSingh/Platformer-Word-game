import pygame
import screen_size as ss
import pygame_button as pgb
from settings_file import settings

pygame.init()
screen = pygame.display.set_mode((ss.SCREEN_WIDTH, ss.SCREEN_HEIGHT))


def menu():
    clock = pygame.time.Clock()
    background = pygame.image.load("images/fblaGameBg.jpg").convert()
    background = pygame.transform.scale(background, (ss.SCREEN_WIDTH, ss.SCREEN_HEIGHT))
    single_player = pgb.Button((0, 0, 3*ss.SCREEN_WIDTH/16, 3*ss.SCREEN_HEIGHT/16), (80, 80, 80), settings, text="Settings",
                               hover_color=(0, 0, 0))
    while True:
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                exit()
            single_player.check_event(event)

        single_player.update(screen)
        pygame.display.update()
        clock.tick(75)


if __name__ == "__main__":
    menu()
