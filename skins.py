import pygame
import ui_tools
import screen_size as ss
import json
from math import ceil
from Level import level_list

pygame.init()
list_skins = ["santa", "boy", "adventure_girl", "female_zombie", "male_zombie", "adventure_boy", "cat",
              "dog", "dinosaur", "knight", "ninja_girl", "ninja_girl2", "pumpkin", "robot"]
stars_required = [0, 2, 3, 5, 5, 7, 8, 8, 9, 10, 11, 11, 12, 12]


def skins(screen, back_button_func):
    def change_skin(current_skin_change: dict):
        var["users"][var["current_user"][0]][2] = current_skin_change["skin"]

    def change_screen(func):
        with open('variables.json', 'w') as wvar:
            json.dump(var, wvar, indent=4)
        func()

    def go_to_next_page(going_to_next_page: dict = {}):
        going_to_next_page = going_to_next_page.get("going_to_next_page", True)
        if going_to_next_page is None:
            going_to_next_page = {}
        checked = False
        for button_skin in skins_btn:
            button_skin = button_skin[1]
            if going_to_next_page:
                button_skin.move(-ss.SCREEN_WIDTH)
            else:
                button_skin.move(ss.SCREEN_WIDTH)
            if not checked:
                if button_skin.rect.x <= -ss.SCREEN_WIDTH * (ceil((len(list_skins)) / 3) - 1) + button_skin.rect.w:
                    next_page.state_disabled = True
                else:
                    next_page.state_disabled = False

                if button_skin.rect.x >= 0:
                    previous_page.state_disabled = True
                else:
                    previous_page.state_disabled = False
                checked = True

    with open('variables.json', 'r') as f:
        var = json.load(f)
    clock = pygame.time.Clock()
    background = pygame.image.load("images/Menu_page/menu_bg.png").convert()
    back_image = pygame.transform.scale(pygame.image.load("images/back_button.png").convert_alpha(),
                                        (ss.SCREEN_WIDTH / 14.3, ss.SCREEN_HEIGHT / 8.4))  # 75, 75

    font = pygame.font.Font(None, 156)
    skins_txt = font.render("Choose your Avatar", True, (255, 255, 255))

    back_button = ui_tools.Button((int(ss.SCREEN_WIDTH / 71.5), int(ss.SCREEN_WIDTH / 71.5), ss.SCREEN_WIDTH / 19.1, ss.SCREEN_HEIGHT / 10.4), (0, 0, 0),
                                  lambda: change_screen(lambda: back_button_func(screen)), image=back_image,
                                  fill_bg=False,
                                  border_color=(255, 255, 255))

    next_button = pygame.transform.scale(pygame.image.load("images/Menu_page/i02_next_button.png").convert_alpha(),
                                         (int(ss.SCREEN_WIDTH / 14.3), int(ss.SCREEN_WIDTH / 9.533)))
    disabled_next_button = pygame.transform.scale(
        pygame.image.load("images/Menu_page/i01_next_button.png").convert_alpha(),
        (int(ss.SCREEN_WIDTH / 14.3), int(ss.SCREEN_WIDTH / 9.533)))
    previous_button = pygame.transform.flip(next_button, True, False)
    disabled_previous_button = pygame.transform.flip(disabled_next_button, True, False)

    games_played = sorted(var["users"][var["current_user"][0]][1], key=lambda x: (x[0], x[1], x[2], x[3]), reverse=True)

    current_stars = 0
    for level in level_list:
        for game in games_played:
            if level.str == game[0]:
                current_stars += game[1]
                break

    disabled = True if len(list_skins) <= 3 else False
    next_page = ui_tools.Button(
        (ss.SCREEN_WIDTH - 20 - next_button.get_width(), ss.SCREEN_HEIGHT / 2 - next_button.get_height() / 2,
         next_button.get_width(), next_button.get_height()), (0, 0, 0), go_to_next_page,
        state_disabled=disabled,
        image=next_button, fill_bg=False, disabled_image=disabled_next_button)
    previous_page = ui_tools.Button(
        (int(ss.SCREEN_WIDTH / 71.5), ss.SCREEN_HEIGHT / 2 - next_button.get_height() / 2, next_button.get_width(),
         next_button.get_height()),
        (0, 0, 0), go_to_next_page, image=previous_button, fill_bg=False,
        disabled_image=disabled_previous_button, state_disabled=True, going_to_next_page=False)

    button_lis = [back_button, previous_page, next_page]
    skins_btn = []
    lock_original = pygame.image.load("images/Menu_page/lock_bg.png").convert_alpha()

    for index, skin in enumerate(list_skins):
        different_page_difference = int(ss.SCREEN_WIDTH / 11.72)
        if index % 3 == 0 and index != 0:
            different_page_difference = int(ss.SCREEN_WIDTH / 47.67) + previous_page.rect.right+(ss.SCREEN_WIDTH*(index//3 - 1)) + \
                                        (ss.SCREEN_WIDTH - skin_btn.rect.right)
        idle_image = pygame.image.load(f"images/{skin.title()}/Idle (1).png").convert()
        idle_image = pygame.transform.scale(idle_image,
                                            (ss.SCREEN_WIDTH / 5,
                                             ss.SCREEN_WIDTH / 5 / idle_image.get_width() * idle_image.get_height()))
        idle_image.set_colorkey((0, 0, 0))
        x_value = int(ss.SCREEN_WIDTH / 47.67) + previous_page.rect.right if index == 0 else skin_btn.rect.right + different_page_difference
        if stars_required[index] <= current_stars:
            skin_btn = ui_tools.Button(
                (x_value,
                 ss.SCREEN_HEIGHT / 2 - idle_image.get_height() / 2,
                 idle_image.get_width(), idle_image.get_height()), (0, 0, 0), change_skin,
                image=idle_image, border_color=(255, 255, 255), border_radius=1, skin=skin.lower())
        else:
            image = [idle_image, pygame.transform.scale(
                lock_original, (skin_btn.rect.w, lock_original.get_height()/lock_original.get_width()*skin_btn.rect.w))]
            skin_btn = ui_tools.Button(
                (x_value,
                 ss.SCREEN_HEIGHT / 2 - idle_image.get_height() / 2,
                 idle_image.get_width(), idle_image.get_height()), (0, 0, 0), change_skin,
                image=image, border_color=(255, 255, 255), border_radius=1, skin=skin.lower(), state_disabled=True,
                image_position=[(0, 0), (0, (idle_image.get_height() - image[1].get_height())/2)])
        button_lis.append(skin_btn)
        skins_btn.append((skin, skin_btn))

    while True:
        current_skin = {var["users"][var["current_user"][0]][2]: 25}
        for index, skin in enumerate(skins_btn):
            skin[1].border_thickness = current_skin.get(skin[0].lower(), 0)
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
