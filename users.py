import pygame
import ui_tools
import screen_size as ss
import json
from Level import level_list

pygame.init()


def users(screen, back_button_func):
    def change_screen(func):
        with open('variables.json', 'w') as wvar:
            json.dump(var, wvar, indent=4)
        func()

    def set_user(index_name):
        """
        Set user is setting to last position
        :param index_name:
        :return:
        """
        print(index_name)
        var["current_user"] = [index_name, var["users"][index_name][0]]
        print(var["current_user"])

    def create_user():
        image = pygame.transform.scale(
            pygame.image.load(r"images/Boy/Idle (1).png").convert(), (100, 160))
        image.set_colorkey((0, 0, 0))
        users_button = ui_tools.Button((300, (len(users_button_list)) * 175 + 150, 800, 150), (34, 54, 75),
                                       lambda: set_user(len(users_button_list)),
                                       text="", image=image, image_position=(30, -5),
                                       text_position=(60 + image.get_width(), 30), border_radius=20,
                                       border_color=(255, 255, 255), font=font, state_disabled=True)
        input_lis.append(ui_tools.InputBox(
            users_button.rect.x + 60 + image.get_width(), users_button.rect.y + 30, 300, 53, (32, 84, 101),
            (14, 31, 47),
            (28, 48, 65), add_user_with_name, text="What is the user's name?", active=True,
            cursor_color=(255, 255, 255)))
        button_lis.append(users_button)
        users_button_list.append(users_button)
        add_user.move(y_add=175)
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
            users_button_list.clear()
            for index, value in enumerate(var["users"]):
                image = pygame.transform.scale(
                    pygame.image.load(rf"images/{value[2].capitalize()}/Idle (1).png").convert(), (100, 160))
                image.set_colorkey((0, 0, 0))
                font = pygame.font.Font(None, 48)
                users_button = ui_tools.Button((300, index * 175 + 150, 800, 150), (34, 54, 75),
                                               lambda: set_user(index),
                                               text=value[0], image=image, image_position=(30, -5),
                                               text_position=(60 + image.get_width(), 30), border_radius=20,
                                               border_color=(255, 255, 255), font=font, state_disabled=True)
                button_lis.append(users_button)
                users_button_list.append(users_button)
                button_lis.append(
                    ui_tools.Button((users_button.rect.right - 200, users_button.rect.bottom - 50, 200, 50),
                                    (32, 84, 101), lambda: set_user(index),
                                    text="Set User", clicked_color=(14, 31, 47), hover_color=(28, 48, 65),
                                    border_color=(255, 255, 255), border_radius=20))
                current_level = "Completed"
                for level in level_list:
                    for i in value[1]:
                        if i and level.str == i[0]:
                            break
                    else:
                        current_level = level.str
                        break
                level_font.append(font.render("Current level: " + current_level.upper(), True, (255, 255, 255)))
            print(add_user.rect.y)
            add_user.rect.y = users_button_list[-1].rect.bottom + 16
            print(add_user.rect.y)
            add_user.state_disabled = False
            button_lis.append(add_user)
            button_lis.append(scroll_down)
            button_lis.append(scroll_up)

    def scroll(up=True):
        pass

    with open('variables.json', 'r') as f:
        var = json.load(f)
    clock = pygame.time.Clock()
    background = pygame.image.load("images/Menu_page/menu_bg.png").convert()
    back_image = pygame.transform.scale(pygame.image.load("images/back_button.png").convert_alpha(),
                                        (ss.SCREEN_WIDTH / 14.3, ss.SCREEN_HEIGHT / 8.4))  # 75, 75
    back_button = ui_tools.Button((20, 20, ss.SCREEN_WIDTH / 19.1, ss.SCREEN_HEIGHT / 10.4), (0, 0, 0),
                                  lambda: change_screen(lambda: back_button_func(screen)), image=back_image,
                                  fill_bg=False)

    button_lis = [back_button]
    level_font = []
    users_button_list = []
    for index, value in enumerate(var["users"]):
        image = pygame.transform.scale(
            pygame.image.load(rf"images/{value[2].capitalize()}/Idle (1).png").convert(), (100, 160))
        image.set_colorkey((0, 0, 0))
        font = pygame.font.Font(None, 48)
        users_button = ui_tools.Button((300, index * 175 + 150, 800, 150), (34, 54, 75), lambda: set_user(index),
                                       text=value[0], image=image, image_position=(30, -5),
                                       text_position=(60 + image.get_width(), 30), border_radius=20,
                                       border_color=(255, 255, 255), font=font, state_disabled=True)
        button_lis.append(users_button)
        users_button_list.append(users_button)
        button_lis.append(ui_tools.Button((users_button.rect.right - 200, users_button.rect.bottom - 50, 200, 50),
                                          (32, 84, 101), lambda: set_user(index),
                                          text="Set User", clicked_color=(14, 31, 47), hover_color=(28, 48, 65),
                                          border_color=(255, 255, 255), border_radius=20))
        current_level = "Completed"
        for level in level_list:
            for i in value[1]:
                if i and level.str == i[0]:
                    break
            else:
                current_level = level.str
                break
        level_font.append(font.render("Current level: " + current_level.upper(), True, (255, 255, 255)))

    add_user = ui_tools.Button(
        (users_button_list[-1].rect.centerx - 120, users_button_list[-1].rect.bottom + 16, 240, 50),
        (34, 54, 75), create_user,
        text="Add User", clicked_color=(14, 31, 47), hover_color=(28, 48, 65),
        border_color=(255, 255, 255), border_radius=20)
    button_lis.append(add_user)
    input_lis = []
    circle_pos = []

    # scrolling
    go_down = pygame.transform.scale(pygame.image.load("images/Menu_page/i02_next_button.png").convert_alpha(),
                                     (100, 150))
    disabled_go_down = pygame.transform.scale(
        pygame.image.load("images/Menu_page/i01_next_button.png").convert_alpha(),
        (100, 150))
    go_down = pygame.transform.rotate(go_down, -90)
    disabled_go_down = pygame.transform.rotate(disabled_go_down, -90)
    go_up = pygame.transform.flip(go_down, False, True)
    disabled_go_up = pygame.transform.flip(disabled_go_down, False, True)
    # Add rect positions for scroll_up and down
    scroll_up = ui_tools.Button(
        (1340 - go_up.get_width()/2, 40, go_up.get_width(), go_up.get_height()),
        (0, 0, 0), lambda: scroll(), image=go_up, fill_bg=False, disabled_image=disabled_go_up, state_disabled=True)
    scroll_down = ui_tools.Button(
        (1340 - go_down.get_width()/2, 740 - go_down.get_height(), go_down.get_width(), go_down.get_height()),
        (0, 0, 0), lambda: scroll(False), image=go_down, fill_bg=False,
        disabled_image=disabled_go_down, state_disabled=True)
    button_lis.append(scroll_down)
    button_lis.append(scroll_up)

    font = pygame.font.Font(None, 128)
    users_text = font.render("Choose or add your User", True, (255, 255, 255))
    while True:
        if add_user.rect.bottom > ss.SCREEN_HEIGHT:
            scroll_down.state_disabled = False
        else:
            scroll_down.state_disabled = True
        screen.blit(background, (0, 0))
        screen.blit(users_text, (
            ss.SCREEN_WIDTH / 2 - users_text.get_width() / 2, ss.SCREEN_HEIGHT / 8 - users_text.get_height() / 2))
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                with open('variables.json', 'w') as wvar:
                    json.dump(var, wvar, indent=4)
                pygame.quit()
                exit()
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     circle_pos.append(event.pos)
            #     print(event.pos)
            for i in button_lis:
                i.check_event(event)
            for i in input_lis:
                i.check_event(event)

        for i in button_lis:
            i.update(screen)
        for i in input_lis:
            i.update(screen)

        for index, value in enumerate(level_font):
            screen.blit(value, (users_button_list[-1].rect.x + users_button_list[-1].image.get_width() + 60,
                                index * 175 + 190 + 36))

        for i in circle_pos:
            pygame.draw.circle(screen, (255, 0, 0), i, 7)
        pygame.display.update()
        clock.tick()


if __name__ == "__main__":
    from menu import menu

    root = pygame.display.set_mode((ss.SCREEN_WIDTH, ss.SCREEN_HEIGHT))
    users(root, menu)
