import pygame
import ui_tools as pgb
import screen_size as ss
import json

pygame.init()


def skins(screen, back_button_func):
    def change_skin(skin: dict):
        var["users"][var["current_user"][0]][2] = skin["skin"]

    def change_screen(func):
        with open('variables.json', 'w') as wvar:
            json.dump(var, wvar, indent=4)
        func()

    with open('variables.json', 'r') as f:
        var = json.load(f)
    clock = pygame.time.Clock()
    background = pygame.image.load("images/Menu_page/menu_bg.png").convert()
    back_image = pygame.transform.scale(pygame.image.load("images/back_button.png").convert_alpha(),
                                        (ss.SCREEN_WIDTH / 14.3, ss.SCREEN_HEIGHT / 8.4))  # 75, 75

    font = pygame.font.Font(None, 156)
    skins_txt = font.render("Choose your Avatar", True, (255, 255, 255))

    back_button = pgb.Button((20, 20, ss.SCREEN_WIDTH / 19.1, ss.SCREEN_HEIGHT / 10.4), (0, 0, 0),
                             lambda: change_screen(lambda: back_button_func(screen)), image=back_image, fill_bg=False,
                             border_color=(255, 255, 255))
    button_lis = [back_button]
    skins_btn = []
    # Add more skins as well as scroll button that moves the button for which we also need to reduce the gap
    list_skins = ["Santa", "Boy", "Female_zombie", "Male_zombie"]
    for index, skin in enumerate(list_skins):
        idle_image = pygame.image.load(f"images/{skin}/Idle (1).png").convert()
        idle_image = pygame.transform.scale(idle_image,
                                            (ss.SCREEN_WIDTH / 5,
                                             ss.SCREEN_WIDTH / 5 / idle_image.get_width() * idle_image.get_height()))
        idle_image.set_colorkey((0, 0, 0))
        skin_btn = pgb.Button(
            ((index * 2 + 1) * ss.SCREEN_WIDTH / 8 - idle_image.get_width() / 2,
             ss.SCREEN_HEIGHT / 2 - idle_image.get_height() / 2,
             idle_image.get_width(), idle_image.get_height()), (0, 0, 0), change_skin,
            image=idle_image, border_color=(255, 255, 255), border_radius=1, skin=skin.lower())
        button_lis.append(skin_btn)
        skins_btn.append(skin_btn)

    while True:
        santa_border = boy_border = female_zombie_border = male_zombie_border = 0
        match var["users"][var["current_user"][0]][2]:
            case "santa":
                santa_border = 25
            case "boy":
                boy_border = 25
            case "male_zombie":
                male_zombie_border = 25
            case "female_zombie":
                female_zombie_border = 25
        border_lis = [santa_border, boy_border, female_zombie_border, male_zombie_border]
        for index, skin in enumerate(skins_btn):
            skin.border_thickness = border_lis[index]
        # santa_btn.border_thickness = santa_border
        # boy_btn.border_thickness = boy_border
        # female_zombie_btn.border_thickness = female_zombie_border
        # male_zombie_btn.border_thickness = male_zombie_border
        screen.blit(background, (0, 0))
        screen.blit(skins_txt, (
            ss.SCREEN_WIDTH / 2 - skins_txt.get_width() / 2, ss.SCREEN_HEIGHT / 12 - skins_txt.get_height() / 2))
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
