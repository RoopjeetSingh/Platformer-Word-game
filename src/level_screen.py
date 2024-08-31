import pygame
import ui_tools
import screen_size as ss
import json_storer
from Level import level_list
from platformer_game import platformer_game
from helpful_functions import blit_text
from decode_file import decode_file
from math import ceil
import other_small_images

pygame.init()
stars_required = [0, 1, 5, 6, 11]


def level_screen(screen, back_button_func):

    def change_screen(func):
        with open('json_storer.py', 'w') as wvar:
            wvar.write("var=" + str(var))
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

    def set_level(kwargs):
        # var["level"] = new_level_dic["new_level"].str
        button_level: ui_tools.Button = kwargs["button"]
        if not isinstance(button_level.image, list):
            change_screen(lambda: platformer_game(screen, back_button_func, kwargs["new_level"]))
        else:
            stars = stars_required[level_list.index(kwargs["new_level"])]
            for i in text_list:
                if i[1] == button_level:
                    break
            else:
                text_list.append([f"You need {stars} stars to unlock this level", button_level, 0])

    def make_level():
        show_no_add_page = True
        return show_no_add_page

    var = json_storer.var
        
    clock = pygame.time.Clock()
    background = pygame.image.load(decode_file(other_small_images.menu_bg)).convert()
    next_button = pygame.transform.scale(pygame.image.load(decode_file(other_small_images.next_button)).convert_alpha(),
                                         (int(ss.SCREEN_WIDTH / 14.3), int(ss.SCREEN_WIDTH / 9.53)))
    disabled_next_button = pygame.transform.scale(
        pygame.image.load(decode_file(other_small_images.disabled_next_button)).convert_alpha(),
        (int(ss.SCREEN_WIDTH / 14.3), int(ss.SCREEN_WIDTH / 9.53)))
    previous_button = pygame.transform.flip(next_button, True, False)
    disabled_previous_button = pygame.transform.flip(disabled_next_button, True, False)

    disabled = True if len(level_list) + 1 <= 3 else False
    next_page = ui_tools.Button(
        (ss.SCREEN_WIDTH - 20 - next_button.get_width(), ss.SCREEN_HEIGHT / 2 - next_button.get_height() / 2,
         next_button.get_width(), next_button.get_height()), (0, 0, 0), go_to_next_page,
        state_disabled=disabled,
        image=next_button, fill_bg=False, disabled_image=disabled_next_button)
    previous_page = ui_tools.Button(
        (int(ss.SCREEN_WIDTH / 71.5), ss.SCREEN_HEIGHT / 2 - next_button.get_height() / 2, next_button.get_width(), next_button.get_height()),
        (0, 0, 0), go_to_next_page, image=previous_button, fill_bg=False,
        disabled_image=disabled_previous_button, state_disabled=True, going_to_next_page=False)

    back_image = pygame.transform.scale(pygame.image.load(decode_file(other_small_images.back_button)).convert_alpha(),
                                        (int(ss.SCREEN_WIDTH / 14.3), int(ss.SCREEN_HEIGHT / 8.4)))  # 75, 75
    back_button = ui_tools.Button((int(ss.SCREEN_WIDTH / 71.5), int(ss.SCREEN_WIDTH / 71.5), int(ss.SCREEN_WIDTH / 19.1), int(ss.SCREEN_HEIGHT / 10.4)), (0, 0, 0),
                                  lambda: change_screen(lambda: back_button_func(screen)), image=back_image,
                                  fill_bg=False)

    font = pygame.font.Font(None, int(ss.SCREEN_WIDTH / 9.17))
    level_txt = font.render("Choose your Level", True, (255, 255, 255))
    font = pygame.font.Font(None, 30)

    button_level_list = []
    games_played = sorted(var["users"][var["current_user"][0]][1], key=lambda x: (x[0], x[1], x[2], x[3]), reverse=True)

    current_stars = 0
    for level in level_list:
        for game in games_played:
            if level.str == game[0]:
                current_stars += game[1]
                break

    width_image = ((ss.SCREEN_WIDTH - 2 * previous_page.rect.right) / 2 - 40) / 1.5
    lock_original = pygame.image.load(decode_file(other_small_images.lock_bg)).convert_alpha()
    lock = pygame.transform.scale(lock_original, (width_image, int(ss.SCREEN_WIDTH / 7.15)))
    # This makes the width enough for 3 levels to be in it
    for index, level in enumerate(level_list):
        different_page_difference = 0
        if index % 3 == 0 and index != 0:
            different_page_difference = int(ss.SCREEN_WIDTH / 71.5) + previous_page.rect.right + (ss.SCREEN_WIDTH * (index // 3 - 1)) + (
                        ss.SCREEN_WIDTH - button.rect.right)
        image = pygame.transform.scale(level.bg_display, (width_image, width_image / level.bg_display.get_width() *
                                                          level.bg_display.get_height()))
        x_value = int(ss.SCREEN_WIDTH / 71.5) + previous_page.rect.right if index == 0 else button.rect.right + int(ss.SCREEN_WIDTH / 71.5) + different_page_difference
        border_thickness = 0
        if current_stars < stars_required[index]:
            image = [image, pygame.transform.scale(
                lock_original, (width_image, width_image / level.bg_display.get_width() *
                                level.bg_display.get_height() + int(ss.SCREEN_WIDTH / 40.86)))]
            button = ui_tools.Button(
                (x_value,
                 ss.SCREEN_HEIGHT / 3, width_image, width_image / level.bg_display.get_width() *
                 level.bg_display.get_height() + int(ss.SCREEN_WIDTH / 40.86)),
                (0, 0, 0), set_level, text=level.str.upper(),
                image=image, border_radius=1, border_color=(255, 255, 255), border_thickness=border_thickness,
                image_position=[(0, width_image / level.bg_display.get_width() *
                                 level.bg_display.get_height() + int(ss.SCREEN_WIDTH / 40.86) - image[0].get_height()), (0, 0)],
                new_level=level)
            button.kwargs["button"] = button
            button.text_position = ((button.rect.w - button.text.get_width()) / 2, 5)
        else:
            button = ui_tools.Button(
                (x_value,
                 ss.SCREEN_HEIGHT / 3, width_image, width_image / level.bg_display.get_width() *
                 level.bg_display.get_height() + int(ss.SCREEN_WIDTH / 40.86)),
                (0, 0, 0), set_level, text=level.str.upper(),
                image=image, border_radius=1, border_color=(255, 255, 255), border_thickness=border_thickness,
                image_align="bottom", new_level=level)
            button.kwargs["button"] = button
        button_level_list.append(button)
    different_page_difference = 0
    if len(level_list) % 3 == 0 and len(level_list) != 0:
        different_page_difference = int(ss.SCREEN_WIDTH / 71.5) + previous_page.rect.right + (ss.SCREEN_WIDTH - button.rect.right)
    x_value = button.rect.right + int(ss.SCREEN_WIDTH / 71.5) + different_page_difference
    add_level = ui_tools.Button((
        x_value, ss.SCREEN_HEIGHT / 2 - int(ss.SCREEN_WIDTH / 7.15) / 2,
        width_image, int(ss.SCREEN_WIDTH / 7.15)), (152, 152, 152), make_level, text="Add Level", border_radius=15,
        border_color=(152, 152, 152), font=pygame.font.Font(None, int(ss.SCREEN_WIDTH / 19.86)),
        hover_color=(80, 80, 80), image=lock, image_position=(0, 0))
    add_level.text_position = (add_level.rect.w / 2 - add_level.text.get_width() / 2,
                               add_level.rect.h / 2 - add_level.text.get_height() / 2)
    button_level_list.append(add_level)
    button_lis = [back_button, next_page, previous_page] + button_level_list
    alpha = 0
    text_list = []
    while True:
        show_no_add_page = add_level.value_from_function
        screen.blit(background, (0, 0))
        screen.blit(level_txt, (
            ss.SCREEN_WIDTH / 2 - level_txt.get_width() / 2, ss.SCREEN_HEIGHT / 8 - level_txt.get_height() / 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                with open('json_storer.py', 'w') as wvar:
                    wvar.write("var=" + str(var))
                pygame.quit()
                exit()
            for i in button_lis:
                i.check_event(event)

        if show_no_add_page:
            blit_text(screen, "Add Level would be added in the next update",
                      (add_level.rect.centerx, add_level.rect.y - font.render(" ", False, (0, 0, 0)).get_height() * 2 - 5),
                      font, add_level.rect.right - 30, color=(255, 255, 255), alpha=min(alpha, 255))
            if alpha <= 300:
                alpha += 0.5

        for i in button_lis:
            i.update(screen)
        for text in text_list:
            blit_text(screen, text[0], (text[1].rect.centerx,
                                        text[1].rect.y - font.render(" ", False, (0, 0, 0)).get_height() * 2 - 5),
                      font, text[1].rect.right - 30, [255, 255, 255], text[2])
            if text[2] < 256:
                text[2] += 2
        pygame.display.update()
        clock.tick()


if __name__ == "__main__":
    from menu import menu

    root = pygame.display.set_mode((ss.SCREEN_WIDTH, ss.SCREEN_HEIGHT))
    level_screen(root, menu)
