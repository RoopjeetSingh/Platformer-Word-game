import pygame
import ui_tools
import screen_size as ss
import json
from Level import level_list
from platformer_game import platformer_game
from helpful_functions import calculate_current_level
from math import ceil

pygame.init()


def level_screen(screen, back_button_func):
    def change_screen(func):
        with open('variables.json', 'w') as wvar:
            json.dump(var, wvar, indent=4)
        func()

    def go_to_next_page(going_to_next_page: bool = True):
        checked = False
        for button_level in button_level_list:
            if going_to_next_page:
                button_level.move(-ss.SCREEN_WIDTH)
            else:
                button_level.move(ss.SCREEN_WIDTH)
            if not checked:
                if button_level.rect.x <= -ss.SCREEN_WIDTH * (ceil((len(level_list)+1)/3) - 1) + width_image:
                    next_page.state_disabled = True
                else:
                    next_page.state_disabled = False

                if button_level.rect.x >= 0:
                    previous_page.state_disabled = True
                else:
                    print(button_level.rect.x)
                    previous_page.state_disabled = False
                checked = True

    def set_level(new_level):
        var["level"] = new_level.str
        change_screen(lambda: platformer_game(screen))

    with open('variables.json', 'r') as f:
        var = json.load(f)
    clock = pygame.time.Clock()
    background = pygame.image.load("images/Menu_page/menu_bg.png").convert()
    next_button = pygame.transform.scale(pygame.image.load("images/Menu_page/i02_next_button.png").convert_alpha(),
                                         (100, 150))
    disabled_next_button = pygame.transform.scale(
        pygame.image.load("images/Menu_page/i01_next_button.png").convert_alpha(),
        (100, 150))
    previous_button = pygame.transform.flip(next_button, True, False)
    disabled_previous_button = pygame.transform.flip(disabled_next_button, True, False)

    back_image = pygame.transform.scale(pygame.image.load("images/back_button.png").convert_alpha(),
                                        (ss.SCREEN_WIDTH / 14.3, ss.SCREEN_HEIGHT / 8.4))  # 75, 75
    back_button = ui_tools.Button((20, 20, ss.SCREEN_WIDTH / 19.1, ss.SCREEN_HEIGHT / 10.4), (0, 0, 0),
                                  lambda: change_screen(lambda: back_button_func(screen)), image=back_image,
                                  fill_bg=False)

    disabled = True if len(level_list)+1 <= 3 else False
    next_page = ui_tools.Button(
        (ss.SCREEN_WIDTH - 20 - next_button.get_width(), ss.SCREEN_HEIGHT / 2 - next_button.get_height() / 2,
         next_button.get_width(), next_button.get_height()), (0, 0, 0), lambda: go_to_next_page(), state_disabled=disabled,
        image=next_button, fill_bg=False, disabled_image=disabled_next_button)
    previous_page = ui_tools.Button(
        (20, ss.SCREEN_HEIGHT / 2 - next_button.get_height() / 2, next_button.get_width(), next_button.get_height()),
        (0, 0, 0), lambda: go_to_next_page(False), image=previous_button, fill_bg=False,
        disabled_image=disabled_previous_button, state_disabled=True)

    font = pygame.font.Font(None, 156)
    level_txt = font.render("Choose your Level", True, (255, 255, 255))

    button_level_list = []
    current_level = calculate_current_level(var)

    width_image = ((ss.SCREEN_WIDTH - 2 * previous_page.rect.right) / 2 - 40) / 1.5
    # This makes the width enough for 3 levels to be in it
    for index, level in enumerate(level_list):
        # Need to show the current level

        # if level.str == current_level.str:
        #     image = pygame.transform.scale(level.bg_display, (
        #         width_image - 25, (width_image - 25) / level.bg_display.get_width() * level.bg_display.get_height()))
        #     border_thickness = 25
        # else:
        image = pygame.transform.scale(level.bg_display, (width_image, width_image / level.bg_display.get_width() *
                                                          level.bg_display.get_height()))
        border_thickness = 0
        button = ui_tools.Button(
            (index * (width_image + 20) + 20 + previous_page.rect.right,
             ss.SCREEN_HEIGHT / 3, width_image, width_image / level.bg_display.get_width() *
             level.bg_display.get_height() + 35),
            (0, 0, 0), lambda: set_level(level), text=level.str.upper(),
            image=image, border_radius=1, border_color=(255, 255, 255), border_thickness=border_thickness,
            image_align="bottom")
        print(border_thickness)
        button_level_list.append(button)

    add_level = ui_tools.Button(((len(button_level_list) - 1) * (width_image + 20) + 20 + previous_page.rect.right, ))
    button_lis = [back_button, next_page, previous_page] + button_level_list
    while True:
        screen.blit(background, (0, 0))
        screen.blit(level_txt, (
            ss.SCREEN_WIDTH / 2 - level_txt.get_width() / 2, ss.SCREEN_HEIGHT / 8 - level_txt.get_height() / 2))
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
        clock.tick()


if __name__ == "__main__":
    from menu import menu

    root = pygame.display.set_mode((ss.SCREEN_WIDTH, ss.SCREEN_HEIGHT))
    level_screen(root, menu)
