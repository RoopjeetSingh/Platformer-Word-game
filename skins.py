import pygame
import pygame_button as pgb
import screen_size as ss
# from menu import menu
pygame.init()
screen = pygame.display.set_mode((ss.SCREEN_WIDTH, ss.SCREEN_HEIGHT))


def skins():
    clock = pygame.time.Clock()
    back_image = pygame.transform.scale(pygame.image.load("images/back_button.png").convert_alpha(),
                                            (ss.SCREEN_WIDTH / 28.6, ss.SCREEN_HEIGHT / 28.5))
    # pgb.Button((20, 20, ss.SCREEN_WIDTH / 28.6, ss.SCREEN_HEIGHT / 28.5), (0, 0, 0), menu, image=back_image,
    #            border_radius=ss.SCREEN_WIDTH / 28.6/2)
    button_lis = []
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                exit()
            for i in button_lis:
                i.check_event(event)

        for i in button_lis:
            i.update(screen)
        pygame.display.update()
        clock.tick(75)
