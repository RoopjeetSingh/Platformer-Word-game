import pygame
import ui_tools as pgb
import screen_size as ss
import json

pygame.init()


def opening_page(screen):
    with open('variables.json', 'r') as f:
        var = json.load(f)
    if var["1_time"] == "True" and len(var["users"]) == 0:
        clock = pygame.time.Clock()
        background = pygame.transform.scale(pygame.image.load("images/Menu_page/fblaGameBg.jpg"), (ss.SCREEN_WIDTH,
                                                                                                   ss.SCREEN_HEIGHT))
        name = pgb.InputBox(ss.SCREEN_WIDTH / 2 - 500 / 2, ss.SCREEN_HEIGHT / 2 - 50 / 2, 500, 50, (255, 255, 255),
                            color_hover=(9, 228, 232), color_active=(10, 137, 247), text="Enter your username",
                            active=True)
        name_surface = pygame.Surface((ss.SCREEN_WIDTH/3, ss.SCREEN_HEIGHT/3))
        button_lis = []
        input_lis = [name]
        while True:
            screen.blit(background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    with open('variables.json', 'w') as wvar:
                        json.dump(var, wvar, indent=4)
                    pygame.quit()
                    exit()
                for i in button_lis + input_lis:
                    i.check_event(event)

            for i in button_lis + input_lis:
                i.update(screen)

            pygame.display.update()
            clock.tick(75)


if __name__ == "__main__":
    root = pygame.display.set_mode((ss.SCREEN_WIDTH, ss.SCREEN_HEIGHT))
    opening_page(root)