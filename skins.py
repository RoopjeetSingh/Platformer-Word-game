import pygame
import pygame_button as pgb
import screen_size as ss
import json

pygame.init()


def skins(screen, back_button_func):
    def change_skin(skin: str):
        var["skins"] = skin

    with open('variables.json', 'r') as f:
        var = json.load(f)
    clock = pygame.time.Clock()
    background = pygame.image.load("images/Menu_page/menu_bg.png").convert()
    santa = pygame.image.load("images/Santa/Idle (1).png").convert_alpha()
    boy = pygame.image.load("images/Boy/Idle (1).png").convert_alpha()
    female_zombie = pygame.image.load("images/Female_zombie/Idle (1).png").convert_alpha()
    male_zombie = pygame.image.load("images/Male_zombie/Idle (1).png").convert_alpha()
    for i in [santa, boy, female_zombie, male_zombie]:
        i = pygame.transform.scale(i, (ss.SCREEN_WIDTH / 8, ss.SCREEN_WIDTH / 8 / i.get_width() * i.get_height()))
    back_image = pygame.transform.scale(pygame.image.load("images/back_button.png").convert_alpha(),
                                        (ss.SCREEN_WIDTH / 14.3, ss.SCREEN_HEIGHT / 8.4))  # 75, 75
    back_button = pgb.Button((20, 20, ss.SCREEN_WIDTH / 19.1, ss.SCREEN_HEIGHT / 10.4), (0, 0, 0),
                             lambda: back_button_func(screen), image=back_image,
                             border_radius=int(ss.SCREEN_HEIGHT / 10.4 / 2))
    santa_btn = pgb.Button((ss.SCREEN_WIDTH / 8 - santa.get_width() / 2, ss.SCREEN_HEIGHT / 2 - santa.get_height() / 2,
                            santa.get_width(), santa.get_height()), (0, 0, 0), lambda: change_skin("santa"),
                           image=santa)
    boy_btn = pgb.Button((3 * ss.SCREEN_WIDTH / 8 - boy.get_width() / 2, ss.SCREEN_HEIGHT / 2 - boy.get_height() / 2,
                          boy.get_width(), boy.get_height()), (0, 0, 0), lambda: change_skin("boy"), image=boy)
    female_zombie_btn = pgb.Button(
        (5 * ss.SCREEN_WIDTH / 8 - female_zombie.get_width() / 2, ss.SCREEN_HEIGHT / 2 - female_zombie.get_height() / 2,
         female_zombie.get_width(), female_zombie.get_height()), (0, 0, 0), lambda: change_skin("female_zombie"),
    image=female_zombie)
    male_zombie_btn = pgb.Button(
        (7 * ss.SCREEN_WIDTH / 8 - santa.get_width() / 2, ss.SCREEN_HEIGHT / 2 - santa.get_height() / 2,
         santa.get_width(), santa.get_height()), (0, 0, 0), lambda: change_skin("male_zombie"), image=male_zombie)
    button_lis = [back_button, santa_btn, boy_btn, female_zombie_btn, male_zombie_btn]
    while True:
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                with open('variables.json', 'w') as wvar:
                    json.dump(var, wvar, indent=4)
                pygame.quit()
                exit()
            for i in button_lis:
                i.check_event(event)

        for i in button_lis:
            i.update(screen)
        pygame.display.update()
        clock.tick(75)


if __name__ == "__main__":
    from menu import menu

    root = pygame.display.set_mode((ss.SCREEN_WIDTH, ss.SCREEN_HEIGHT))
    skins(root, menu)
