import pygame
import ui_tools
import screen_size as ss
import json
from Level import level_list
from platformer_game import platformer_game
from helpful_functions import calculate_current_level, blit_text
from math import ceil

pygame.init()


def level_screen(screen, back_button_func):
    def change_screen(func):
        with open('variables.json', 'w') as wvar:
            json.dump(var, wvar, indent=4)
        func()

    def go_to_next_page(going_to_next_page: dict = {}):
        going_to_next_page = going_to_next_page.get("going_to_next_page", True)
        if going_to_next_page is None:
            going_to_next_page = {}
        checked = False
        for button_level in button_level_list:
            if going_to_next_page:
                button_level.move(-ss.SCREEN_WIDTH)
            else:
                button_level.move(ss.SCREEN_WIDTH)
            if not checked:
                if button_level.rect.x <= -ss.SCREEN_WIDTH * (ceil((len(level_list) + 1) / 3) - 1) + width_image:
                    next_page.state_disabled = True
                else:
                    next_page.state_disabled = False

                if button_level.rect.x >= 0:
                    previous_page.state_disabled = True
                else:
                    previous_page.state_disabled = False
                checked = True

    def set_level(new_level_dic):
        # var["level"] = new_level_dic["new_level"].str
        change_screen(lambda: platformer_game(screen, new_level_dic["new_level"]))

    def make_level():
        show_no_add_page = True
        return show_no_add_page

    with open('variables.json', 'r') as f:
        var = json.load(f)
    clock = pygame.time.Clock()
    background = pygame.image.load("images/Menu_page/menu_bg.png").convert()
    next_button = pygame.transform.scale(pygame.image.load("images/Menu_page/i02_next_button.png").convert_alpha(),
                                         (ss.SCREEN_WIDTH / 14.3, ss.SCREEN_WIDTH / 9.53))
    disabled_next_button = pygame.transform.scale(
        pygame.image.load("images/Menu_page/i01_next_button.png").convert_alpha(),
        (ss.SCREEN_WIDTH / 14.3, ss.SCREEN_WIDTH / 9.53))
    previous_button = pygame.transform.flip(next_button, True, False)
    disabled_previous_button = pygame.transform.flip(disabled_next_button, True, False)

    disabled = True if len(level_list) + 1 <= 3 else False
    next_page = ui_tools.Button(
        (ss.SCREEN_WIDTH - 20 - next_button.get_width(), ss.SCREEN_HEIGHT / 2 - next_button.get_height() / 2,
         next_button.get_width(), next_button.get_height()), (0, 0, 0), go_to_next_page,
        state_disabled=disabled,
        image=next_button, fill_bg=False, disabled_image=disabled_next_button)
    previous_page = ui_tools.Button(
        (ss.SCREEN_WIDTH / 71.5, ss.SCREEN_HEIGHT / 2 - next_button.get_height() / 2, next_button.get_width(), next_button.get_height()),
        (0, 0, 0), go_to_next_page, image=previous_button, fill_bg=False,
        disabled_image=disabled_previous_button, state_disabled=True, going_to_next_page=False)

    back_image = pygame.transform.scale(pygame.image.load("images/back_button.png").convert_alpha(),
                                        (ss.SCREEN_WIDTH / 14.3, ss.SCREEN_HEIGHT / 8.4))  # 75, 75
    back_button = ui_tools.Button((ss.SCREEN_WIDTH / 71.5, ss.SCREEN_WIDTH / 71.5, ss.SCREEN_WIDTH / 19.1, ss.SCREEN_HEIGHT / 10.4), (0, 0, 0),
                                  lambda: change_screen(lambda: back_button_func(screen)), image=back_image,
                                  fill_bg=False)

    font = pygame.font.Font(None, int(ss.SCREEN_WIDTH / 9.17))
    level_txt = font.render("Choose your Level", True, (255, 255, 255))
    font = pygame.font.Font(None, int(ss.SCREEN_WIDTH / 39.72))

    button_level_list = []
    current_level = calculate_current_level(var)

    width_image = ((ss.SCREEN_WIDTH - 2 * previous_page.rect.right) / 2 - 40) / 1.5
    lock_original = pygame.image.load("images/Menu_page/lock_bg.png").convert_alpha()
    lock = pygame.transform.scale(lock_original, (width_image, ss.SCREEN_WIDTH / 7.15))
    # This makes the width enough for 3 levels to be in it
    for index, level in enumerate(level_list):
        different_page_difference = 0
        if index % 3 == 0 and index != 0:
            different_page_difference = ss.SCREEN_WIDTH / 71.5 + previous_page.rect.right + (ss.SCREEN_WIDTH * (index // 3 - 1)) + (
                        ss.SCREEN_WIDTH - button.rect.right)
        image = pygame.transform.scale(level.bg_display, (width_image, width_image / level.bg_display.get_width() *
                                                          level.bg_display.get_height()))
        x_value = ss.SCREEN_WIDTH / 71.5 + previous_page.rect.right if index == 0 else button.rect.right + ss.SCREEN_WIDTH / 71.5 + different_page_difference
        border_thickness = 0
        if index > level_list.index(current_level):
            image = [image, pygame.transform.scale(
                lock_original, (width_image, width_image / level.bg_display.get_width() *
                                level.bg_display.get_height() + ss.SCREEN_WIDTH / 40.86))]
            button = ui_tools.Button(
                (x_value,
                 ss.SCREEN_HEIGHT / 3, width_image, width_image / level.bg_display.get_width() *
                 level.bg_display.get_height() + ss.SCREEN_WIDTH / 40.86),
                (0, 0, 0), set_level, text=level.str.upper(),
                image=image, border_radius=1, border_color=(255, 255, 255), border_thickness=border_thickness,
                image_position=[(0, width_image / level.bg_display.get_width() *
                                 level.bg_display.get_height() + ss.SCREEN_WIDTH / 40.86 - image[0].get_height()), (0, 0)],
                state_disabled=True, new_level=level)
            button.text_position = ((button.rect.w - button.text.get_width()) / 2, 5)
        else:
            button = ui_tools.Button(
                (x_value,
                 ss.SCREEN_HEIGHT / 3, width_image, width_image / level.bg_display.get_width() *
                 level.bg_display.get_height() + ss.SCREEN_WIDTH / 40.86),
                (0, 0, 0), set_level, text=level.str.upper(),
                image=image, border_radius=1, border_color=(255, 255, 255), border_thickness=border_thickness,
                image_align="bottom", new_level=level)
        button_level_list.append(button)
    different_page_difference = 0
    if len(level_list) % 3 == 0 and len(level_list) != 0:
        different_page_difference = 20 + previous_page.rect.right + (ss.SCREEN_WIDTH - button.rect.right)
    x_value = button.rect.right + ss.SCREEN_WIDTH / 71.5 + different_page_difference
    add_level = ui_tools.Button((
        x_value, ss.SCREEN_HEIGHT / 2 - ss.SCREEN_WIDTH / 7.15 / 2,
        width_image, ss.SCREEN_WIDTH / 7.15), (152, 152, 152), make_level, text="Add Level", border_radius=15,
        border_color=(152, 152, 152), font=pygame.font.Font(None, 72),
        hover_color=(80, 80, 80), image=lock, image_position=(0, 0))
    add_level.text_position = (add_level.rect.w / 2 - add_level.text.get_width() / 2,
                               add_level.rect.h / 2 - add_level.text.get_height() / 2)
    button_level_list.append(add_level)
    button_lis = [back_button, next_page, previous_page] + button_level_list
    alpha = 0
    while True:
        show_no_add_page = add_level.value_from_function
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

        if show_no_add_page:
            blit_text(screen, "Add Level would be added in the next update",
                      (add_level.rect.centerx, add_level.rect.y - font.render(" ", False, (0, 0, 0)).get_height() * 2),
                      font, add_level.rect.right, color=(255, 255, 255), alpha=min(alpha, ss.SCREEN_WIDTH / 5.6))
            if alpha <= ss.SCREEN_WIDTH / 4.77:
                alpha += 0.5

        for i in button_lis:
            i.update(screen)
        pygame.display.update()
        clock.tick()


if __name__ == "__main__":
    from menu import menu

    root = pygame.display.set_mode((ss.SCREEN_WIDTH, ss.SCREEN_HEIGHT))
    level_screen(root, menu)
