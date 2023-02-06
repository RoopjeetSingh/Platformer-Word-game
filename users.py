import pygame
import ui_tools
import screen_size as ss
import json
from Level import level_list
from decode_file import decode_file
import images_store 
import smaller_store
import other_small_images

pygame.init()


def users(screen, back_button_func):
    class Scroller:
        def __init__(self):
            self.y_pos = int(ss.SCREEN_WIDTH / 6.33)

        def scroll(self, params: dict = {}):
            up = params.get("up", True)
            # y_pos = params.get("y_pos", True)

            if up:
                for button in button_lis:  # Can't use user_button_list because it doesn't have set user buttons
                    button.move(y_add=int(ss.SCREEN_WIDTH / 7.15))
                for input in input_lis:
                    input.rect.y += int(ss.SCREEN_WIDTH / 7.15)
                self.y_pos += int(ss.SCREEN_WIDTH / 7.15)
            else:
                for button in button_lis:
                    button.move(y_add=-int(ss.SCREEN_WIDTH / 7.15))
                for input in input_lis:
                    input.rect.y -= int(ss.SCREEN_WIDTH / 7.15)
                self.y_pos -= int(ss.SCREEN_WIDTH / 7.15)

    def change_screen(func):
        with open('variables.json', 'w') as wvar:
            json.dump(var, wvar, indent=4)
        func["func"]()

    def change_name(location, name):
        pass

    def set_user(index_name):
        """
        Set user is setting to last position
        :param index_name:
        :return:
        """
        index_name = index_name["index_name"]
        var["current_user"] = [index_name, var["users"][index_name][0]]

    def create_user():
        image_new_user = pygame.transform.scale(
            pygame.image.load(r"images/Boy/Idle (1).png").convert(), (int(ss.SCREEN_WIDTH / 14.3), int(ss.SCREEN_WIDTH / 8.9375)))
        image_new_user.set_colorkey((0, 0, 0))
        button_with_input = ui_tools.Button(
            (int(ss.SCREEN_WIDTH / 4.77), (len(users_button_list)) * int(ss.SCREEN_WIDTH / 8.17) + users_button_list[0].rect.y, int(ss.SCREEN_WIDTH / 1.7875), int(ss.SCREEN_WIDTH / 9.533)), (34, 54, 75),
            set_user,
            text="", image=image_new_user, image_position=(int(ss.SCREEN_WIDTH / 47.67), -5),
            text_position=(int(ss.SCREEN_WIDTH / 23.83) + image_new_user.get_width(), int(ss.SCREEN_WIDTH / 47.67)), border_radius=int(ss.SCREEN_WIDTH / 71.5),
            border_color=(255, 255, 255), font=font, state_disabled=True)
        input_lis.append(ui_tools.InputBox(
            button_with_input.rect.x + int(ss.SCREEN_WIDTH / 23.833) + image_new_user.get_width(), button_with_input.rect.y + int(ss.SCREEN_WIDTH / 47.67), int(ss.SCREEN_WIDTH / 4.77), int(ss.SCREEN_WIDTH / 26.98),
            (32, 84, 101),
            (14, 31, 47),
            (28, 48, 65), add_user_with_name, active=True,
            cursor_color=(255, 255, 255), remove_active=True))
        button_lis.append(button_with_input)
        users_button_list.append(button_with_input)
        add_user.move(y_add=int(ss.SCREEN_WIDTH / 8.17))
        add_user.state_disabled = True

    def add_user_with_name(text):
        name_available = True
        for value in var["users"]:
            if text == value[0]:
                name_available = False
                break

        if name_available:
            var["users"].append([text, [], "boy"])
            input_lis.pop()
            button_lis.clear()
            button_lis.append(back_button)
            level_font.clear()
            first_button_y_pos = users_button_list[0].rect.y
            users_button_list.clear()
            font = pygame.font.Font(None, int(ss.SCREEN_WIDTH / 29.79))
            for index, value in enumerate(var["users"]):
                image = pygame.transform.scale(
                    pygame.image.load(rf"images/{value[2].capitalize()}/Idle (1).png").convert(), (int(ss.SCREEN_WIDTH / 14.3), int(ss.SCREEN_WIDTH / 8.9375)))
                image.set_colorkey((0, 0, 0))
                users_button = ui_tools.Button((int(ss.SCREEN_WIDTH / 4.77), index * int(ss.SCREEN_WIDTH / 8.17) + first_button_y_pos, int(ss.SCREEN_WIDTH / 1.7875), int(ss.SCREEN_WIDTH / 9.533)), (34, 54, 75),
                                               set_user,
                                               text=value[0], image=image, image_position=(int(ss.SCREEN_WIDTH / 47.67), -5),
                                               text_position=(int(ss.SCREEN_WIDTH / 23.83) + image.get_width(), int(ss.SCREEN_WIDTH / 47.67)), border_radius=int(ss.SCREEN_WIDTH / 71.5),
                                               border_color=(255, 255, 255), font=font, state_disabled=True)
                button_lis.append(users_button)
                users_button_list.append(users_button)
                button_lis.append(
                    ui_tools.Button((users_button.rect.right - int(ss.SCREEN_WIDTH / 7.15), users_button.rect.bottom - int(ss.SCREEN_WIDTH / 28.6), int(ss.SCREEN_WIDTH / 7.15), int(ss.SCREEN_WIDTH / 28.6)),
                                    (32, 84, 101), set_user,
                                    text="Set User", clicked_color=(14, 31, 47), hover_color=(28, 48, 65),
                                    border_color=(255, 255, 255), border_radius=20, index_name=index))
                current_level = "Completed"
                for level in level_list:
                    for i in value[1]:
                        if i and level.str == i[0]:
                            break
                    else:
                        current_level = level.str
                        break
                level_font.append(font.render("Current level: " + current_level.upper(), True, (255, 255, 255)))
            add_user.rect.y = users_button_list[-1].rect.bottom + int(ss.SCREEN_WIDTH / 89.375)
            add_user.state_disabled = False
            button_lis.append(add_user)

    # def scroll(params: dict = {}):
    #     # global y_pos
    #     up = params.get("up", True)
    #     y_pos = params.get("y_pos", True)
    #
    #     if up:
    #         for button in button_lis:  # Can't use user_button_list because it doesn't have set user buttons
    #             button.move(y_add=200)
    #         for input in input_lis:
    #             input.rect.y += 200
    #         y_pos += 200
    #     else:
    #         for button in button_lis:
    #             button.move(y_add=-200)
    #         for input in input_lis:
    #             input.rect.y -= 200
    #         y_pos -= 200
    #     return y_pos

    with open('variables.json', 'r') as f:
        var = json.load(f)
    clock = pygame.time.Clock()
    background = pygame.image.load(decode_file(other_small_images.menu_bg)).convert()
    back_image = pygame.transform.scale(pygame.image.load(decode_file(other_small_images.back_button)).convert_alpha(),
                                        (ss.SCREEN_WIDTH / 14.3, ss.SCREEN_HEIGHT / 8.4))  # 75, 75
    back_button = ui_tools.Button((int(ss.SCREEN_WIDTH / 71.5), int(ss.SCREEN_WIDTH / 71.5), ss.SCREEN_WIDTH / 19.1, ss.SCREEN_HEIGHT / 10.4), (0, 0, 0),
                                  change_screen, image=back_image,
                                  fill_bg=False, func=lambda: back_button_func(screen))

    button_lis = []
    level_font = []
    users_button_list = []
    font = pygame.font.Font(None, int(ss.SCREEN_WIDTH / 29.79))
    for index, value in enumerate(var["users"]):
        image = pygame.transform.scale(
            pygame.image.load(rf"images/{value[2].capitalize()}/Idle (1).png").convert(), (int(ss.SCREEN_WIDTH / 14.3), int(ss.SCREEN_WIDTH / 8.9375)))
        image.set_colorkey((0, 0, 0))
        users_button = ui_tools.Button((int(ss.SCREEN_WIDTH / 4.77), index * int(ss.SCREEN_WIDTH / 8.17) + int(ss.SCREEN_WIDTH / 9.533), int(ss.SCREEN_WIDTH / 1.7875), int(ss.SCREEN_WIDTH / 9.53)), (34, 54, 75), set_user,
                                       text=value[0], image=image, image_position=(int(ss.SCREEN_WIDTH / 47.67), -5),
                                       text_position=(int(ss.SCREEN_WIDTH / 23.833) + image.get_width(), int(ss.SCREEN_WIDTH / 47.67)), border_radius=int(ss.SCREEN_WIDTH / 71.5),
                                       border_color=(255, 255, 255), font=font, state_disabled=True)
        # change_name_button = ui_tools.Button((300, index * 175 + 150, 800, 150))
        button_lis.append(users_button)
        users_button_list.append(users_button)
        button_lis.append(ui_tools.Button((users_button.rect.right - int(ss.SCREEN_WIDTH / 7.15), users_button.rect.bottom - int(ss.SCREEN_WIDTH / 28.6), int(ss.SCREEN_WIDTH / 7.15), int(ss.SCREEN_WIDTH / 28.6)),
                                          (32, 84, 101), set_user,
                                          text="Set User", clicked_color=(14, 31, 47), hover_color=(28, 48, 65),
                                          border_color=(255, 255, 255), border_radius=int(ss.SCREEN_WIDTH / 71.5), index_name=index))
        current_level = "Completed all levels"
        for level in level_list:
            for i in value[1]:
                if i and level.str == i[0]:
                    break
            else:
                current_level = level.str
                break
        level_font.append(font.render("Current level: " + current_level.upper(), True, (255, 255, 255)))

    add_user = ui_tools.Button(
        (users_button_list[-1].rect.centerx - int(ss.SCREEN_WIDTH / 11.92), users_button_list[-1].rect.bottom + int(ss.SCREEN_WIDTH / 89.375), int(ss.SCREEN_WIDTH / 5.96), int(ss.SCREEN_WIDTH / 28.6)),
        (34, 54, 75), create_user,
        text="Add User", clicked_color=(14, 31, 47), hover_color=(28, 48, 65),
        border_color=(255, 255, 255), border_radius=int(ss.SCREEN_WIDTH / 71.5))
    button_lis.append(add_user)
    input_lis = []

    # scrolling
    go_down = pygame.transform.scale(pygame.image.load(decode_file(other_small_images.next_button)).convert_alpha(),
                                     (int(ss.SCREEN_WIDTH / 14.3), int(ss.SCREEN_WIDTH / 9.533)))
    disabled_go_down = pygame.transform.scale(
        pygame.image.load(decode_file(other_small_images.disabled_next_button)).convert_alpha(),
        (int(ss.SCREEN_WIDTH / 14.3), int(ss.SCREEN_WIDTH / 9.533)))
    go_down = pygame.transform.rotate(go_down, -int(90))
    disabled_go_down = pygame.transform.rotate(disabled_go_down, -int(90))
    go_up = pygame.transform.flip(go_down, False, True)
    disabled_go_up = pygame.transform.flip(disabled_go_down, False, True)
    # Add rect positions for scroll_up and down
    scroller = Scroller()
    scroll_up = ui_tools.Button(
        (int(ss.SCREEN_WIDTH / 1.067) - go_up.get_width() / 2, int(ss.SCREEN_WIDTH / 35.75), go_up.get_width(), go_up.get_height()),
        (0, 0, 0), scroller.scroll, image=go_up, fill_bg=False, disabled_image=disabled_go_up, state_disabled=True)
    scroll_down = ui_tools.Button(
        (int(ss.SCREEN_WIDTH / 1.067) - go_down.get_width() / 2, int(ss.SCREEN_WIDTH / 1.93) - go_down.get_height(), go_down.get_width(), go_down.get_height()),
        (0, 0, 0), scroller.scroll, image=go_down, fill_bg=False,
        disabled_image=disabled_go_down, state_disabled=True, up=False)

    font = pygame.font.Font(None, int(ss.SCREEN_WIDTH / 11.17))
    users_text = font.render("Choose or add your User", True, (255, 255, 255))
    surface_font = pygame.Surface((ss.SCREEN_WIDTH, users_button_list[0].rect.y))
    while True:
        if add_user.rect.bottom > ss.SCREEN_HEIGHT:
            scroll_down.state_disabled = False
        else:
            scroll_down.state_disabled = True
        if users_button_list[0].rect.y < surface_font.get_height():
            # print(users_button_list[0].rect.y, surface_font.get_height())
            scroll_up.state_disabled = False
        else:
            scroll_up.state_disabled = True

        for index, value in enumerate(users_button_list):
            if index == var["current_user"][0]:
                value.border_thickness = int(ss.SCREEN_WIDTH / 57.2)
            else:
                value.border_thickness = 7
        screen.blit(background, (0, 0))
        surface_font.blit(background, (0, 0))
        surface_font.blit(users_text, (
            ss.SCREEN_WIDTH / 2 - users_text.get_width() / 2, ss.SCREEN_HEIGHT / 8 - users_text.get_height() / 2))
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                with open('variables.json', 'w') as wvar:
                    json.dump(var, wvar, indent=4)
                pygame.quit()
                exit()

            for i in button_lis:
                i.check_event(event)
            for i in input_lis:
                i.check_event(event)
            back_button.check_event(event)
            scroll_up.check_event(event)
            scroll_down.check_event(event)

        for i in button_lis:
            i.update(screen)
        back_button.update(surface_font)
        scroll_up.update(surface_font)
        scroll_down.update(screen)
        for i in input_lis:
            i.update(screen)

        for index, value in enumerate(level_font):
            screen.blit(value, (users_button_list[-1].rect.x + users_button_list[-1].image.get_width() + int(ss.SCREEN_WIDTH / 23.833),
                                index * int(ss.SCREEN_WIDTH / 8.17) + scroller.y_pos))
            # print(index * 175 + y_pos, y_pos, index)
        screen.blit(surface_font, (0, 0))
        pygame.display.update()
        clock.tick()


if __name__ == "__main__":
    from menu import menu

    root = pygame.display.set_mode((ss.SCREEN_WIDTH, ss.SCREEN_HEIGHT))
    users(root, menu)
