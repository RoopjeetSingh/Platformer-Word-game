import pygame

import ui_tools
import ui_tools as pgb
import screen_size as ss
import json
from Level import level1
from helpful_functions import blit_text
from player import Player
from wordconnect import game_Loop_Wordle

pygame.init()


def opening_page(screen):
    def get_name(name_user=""):
        name_user = name_user or name.text
        if name_user:
            # var["users"].append([name_user, [], "boy", ["boy", "santa"]])  # [["Roopjeet", [["level1", 3, 256, time],
            # ...], current skin, unlocked skins], ...]
            # Users is a list of people, a dictionary would have been more suitable, but it can not be
            # used because it is not sorted. Later a list of the name and a list that would store another list of
            # level, stars, score and time
            # var["current_user"] = [len(var["users"]) - 1, name_user]
            with open('variables.json', 'w') as wvar:
                json.dump(var, wvar, indent=4)
            # Current_user is a list with two values, the index of the current user and the actual name
            show_level(screen)

    with open('variables.json', 'r') as f:
        var = json.load(f)
    # if var["1_time"] == "True" and len(var["users"]) == 0:
    clock = pygame.time.Clock()
    background = pygame.transform.scale(pygame.image.load("images/Menu_page/fblaGameBg.jpg"), (ss.SCREEN_WIDTH,
                                                                                               ss.SCREEN_HEIGHT))
    name_surface = pygame.Surface((ss.SCREEN_WIDTH / 2, ss.SCREEN_HEIGHT / 2), pygame.SRCALPHA)
    name = pgb.InputBox(int(name_surface.get_width() / 9.5) + ss.SCREEN_WIDTH / 2 - name_surface.get_width() / 2,
                        int(name_surface.get_height() / 3.75) + ss.SCREEN_HEIGHT / 2 - name_surface.get_height() / 2,
                        name_surface.get_width() - 2 * int(name_surface.get_width() / 9.5), ss.SCREEN_WIDTH // 28.6, (255, 255, 255),
                        color_hover=(255, 255, 255), color_active=(255, 255, 255), text="What is your name?",
                        border_radius=ss.SCREEN_WIDTH // 95.33, font_color=(0, 0, 0), active=True, remove_active=True, function=get_name)
    font = pygame.font.SysFont("copperplate", ss.SCREEN_WIDTH // 44.6875)
    ask_name = font.render("What is your name?", True, (255, 255, 255))
    font_text = pygame.font.SysFont("copperplate", ss.SCREEN_WIDTH // 59.583, bold=True)
    ok_button = pgb.Button((ss.SCREEN_WIDTH / 2 - ss.SCREEN_WIDTH // 8.17 / 2,
                            2.6 * name_surface.get_height() / 4 + ss.SCREEN_HEIGHT / 2 - name_surface.get_height() / 2,
                            ss.SCREEN_WIDTH // 8.17, ss.SCREEN_WIDTH // 14.3), (5, 176, 254), get_name, disabled_color=(156, 153, 157), border_radius=ss.SCREEN_WIDTH // 95.33,
                           hover_color=(8, 143, 254), clicked_color=(2, 92, 177),
                           text="OK", border_color=(8, 143, 254), state_disabled=True,
                           font=pygame.font.Font(None, ss.SCREEN_WIDTH // 29.79), disabled_border_color=(70, 67, 72))
    button_lis = [ok_button]
    input_lis = [name]
    while True:
        screen.blit(background, (0, 0))
        pygame.draw.rect(name_surface, (100, 103, 127), name_surface.get_rect(), border_radius=ss.SCREEN_WIDTH // 95.33)
        pygame.draw.rect(name_surface, (222, 234, 244),
                         (ss.SCREEN_WIDTH // 57.2, ss.SCREEN_WIDTH // 28.6 + ask_name.get_height(), name_surface.get_width() - ss.SCREEN_WIDTH // 28.6,
                          name_surface.get_height() - ss.SCREEN_WIDTH // 19.067 - ask_name.get_height()),
                         border_radius=ss.SCREEN_WIDTH // 95.33)
        name_surface.blit(ask_name, (name_surface.get_width() / 2 - ask_name.get_width() / 2, ss.SCREEN_WIDTH // 57.2))
        blit_text(name_surface, "Pick a name you'd like other users to know you by",
                  (name_surface.get_width() / 2, name_surface.get_height() / 2), font_text,
                  name_surface.get_width() - name_surface.get_width() / 7.91, (95, 99, 110))
        screen.blit(name_surface, (
            ss.SCREEN_WIDTH / 2 - name_surface.get_width() / 2, ss.SCREEN_HEIGHT / 2 - name_surface.get_height() / 2))
        if name.text:
            ok_button.state_disabled = False
        else:
            ok_button.state_disabled = True
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
        for i in button_lis:
            i.update(screen)
        for i in input_lis:
            i.update(screen)

        pygame.display.update()
        clock.tick()


# text_show = 0
# show_instructions = True


def show_level(screen):
    text_show = 0

    def show_word_connect():
        start_color = ss.SCREEN_WIDTH // 9.533
        while start_color >= 0:
            screen.fill((start_color, start_color, start_color))
            start_color -= 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    exit()
            clock.tick()
            pygame.display.flip()
        game_Loop_Wordle(screen, [letter_obj.letter for letter_obj in player.letter_lis],
                         len(player.mystery_letter_lis))

    def change_text(text_show):
        text_show = text_show["text_show"]
        text_show += 1
        return text_show

    def skip_instructions():
        show_instructions = False
        return show_instructions

    pressed = False
    with open('variables.json', 'r') as f:
        var = json.load(f)

    current_level = level1
    clock = pygame.time.Clock()
    player = Player(ss.tile_size, ss.SCREEN_HEIGHT - 7 * ss.tile_size, var["users"][var["current_user"][0]][2])
    arrow_img = pygame.image.load("images/arrow1.png").convert_alpha()
    arrow_img = pygame.transform.scale(arrow_img, (ss.SCREEN_WIDTH // 19.067, ss.SCREEN_WIDTH // 28.6))
    button_lis = []
    surface_text = pygame.Surface((ss.SCREEN_WIDTH - 150, ss.SCREEN_WIDTH // 4.77))
    arrow_button = ui_tools.Button((ss.SCREEN_WIDTH - 150, ss.SCREEN_WIDTH // 6.3556, ss.SCREEN_WIDTH // 19.067, ss.SCREEN_WIDTH // 28.6), (0, 0, 0), change_text,
                                   fill_bg=False, image=arrow_img, call_on_release=False)
    skip_button = ui_tools.Button((ss.SCREEN_WIDTH - 155, ss.SCREEN_WIDTH // 5.07, 75, 30), (80, 80, 80), skip_instructions,
                                  border_radius=15, call_on_release=False, text="Skip")
    current_skin = var["users"][var["current_user"][0]][2]
    current_image = pygame.image.load(f"images/{current_skin.capitalize()}/Idle (1).png").convert()
    current_image = pygame.transform.scale(current_image,
                                           (350 / current_image.get_height() * current_image.get_width(), 350))
    current_image.set_colorkey((0, 0, 0))
    stop = False
    surface_text.fill((20, 20, 20))
    surface_text.set_alpha(200)
    while True:
        arrow_button.kwargs["text_show"] = text_show
        text_show = arrow_button.value_from_function if arrow_button.value_from_function is not None else text_show
        button_lis.clear()
        current_level.draw(screen)
        current_level.obstruct_group.draw(screen)
        current_level.platform_group.draw(screen)
        current_level.letter_group.draw(screen)
        current_level.power_up_group.draw(screen)

        for i in current_level.letter_group:
            i.bounce_brighten()

        for i in current_level.power_up_group:
            i.bounce_brighten()
        screen.blit(player.image, player.rect)
        pressed, killed = player.update_player(screen, current_level, pressed, stop_working=stop)
        if killed:
            show_word_connect()
        stop = False
        if skip_button.value_from_function is None:
            show_instructions = True
        else:
            show_instructions = False
        # show_instructions = skip_button.value_from_function or True

        if text_show == 0 and show_instructions:
            # screen.blit(surface_text, (75, ss.SCREEN_HEIGHT - 300))
            screen.blit(surface_text, (75, 25))
            button_lis.append(arrow_button)
            button_lis.append(skip_button)
            screen.blit(current_image, (125, 0))
            blit_text(screen, f"Hi there, Hello!!! I'm the game speaking. The instructions are clear. Collect the "
                              f"letters so that you can use those letters to make new words. Sounds complicated, well "
                              f"it isn't. For your help though "
                              f"we also have mystery letters which you can collect and later convert into any "
                              f"letter. For example, if you collected \"h\" and \"t\", you can use the mystery "
                              f"letter and convert it into a \"u\" which would allow you to make \"hut\". "
                              f"Cool right, let's get started...",
                      (150 + current_image.get_width(), 45),
                      pygame.font.SysFont("copperplate", 25), arrow_button.rect.x - 50, (255, 255, 255),
                      alignment="left")
            stop = True
        elif text_show == 1 and show_instructions:
            screen.blit(surface_text, (75, 25))
            button_lis.append(arrow_button)
            button_lis.append(skip_button)
            screen.blit(current_image, (125, 0))
            arrow_keys = pygame.image.load(
                "images/Menu_page/arrow_keys.png").convert_alpha()
            arrow_keys = pygame.transform.scale(arrow_keys, (120, 80))
            right_pos = blit_text(screen, "Use the arrow keys to move",
                                  (150 + current_image.get_width(), 45),
                                  pygame.font.SysFont("copperplate", 30), arrow_button.rect.x - 50, (255, 255, 255),
                                  alignment="left")
            screen.blit(arrow_keys, (right_pos + 5, 45))
            stop = True
        elif text_show == 2 and player.rect.right - current_level.start > 5 * ss.tile_size and show_instructions:
            screen.blit(surface_text, (75, 25))
            button_lis.append(arrow_button)
            button_lis.append(skip_button)
            screen.blit(current_image, (125, 0))
            arrow_keys = pygame.image.load(
                "images/Menu_page/arrow_keys.png").convert_alpha()
            arrow_keys = pygame.transform.scale(arrow_keys, (120, 80))
            right_pos = blit_text(screen, "Use the arrow up button or the space bar to jump",
                                  (150 + current_image.get_width(), 45),
                                  pygame.font.SysFont("copperplate", 30), arrow_button.rect.x - 50, (255, 255, 255),
                                  alignment="left")
            screen.blit(arrow_keys, (right_pos + 5, 45))
            stop = True
        elif text_show == 3 and player.rect.right - current_level.start > 7 * ss.tile_size and show_instructions:
            screen.blit(surface_text, (75, 25))
            button_lis.append(arrow_button)
            button_lis.append(skip_button)
            screen.blit(current_image, (125, 0))
            blit_text(screen, "Collect these letters!",
                      (150 + current_image.get_width(), 45),
                      pygame.font.SysFont("copperplate", 30), arrow_button.rect.x - 50, (255, 255, 255),
                      alignment="left")
            stop = True
        elif text_show == 4 and player.rect.right - current_level.start > 15 * ss.tile_size and show_instructions:
            screen.blit(surface_text, (75, 25))
            button_lis.append(arrow_button)
            button_lis.append(skip_button)
            screen.blit(current_image, (125, 0))
            blit_text(screen, "Caution: there is an obstacle. Obstacles look like spikes, snowman or even a christmas "
                              "tree; avoid them or else you would have to make the words from the limited letters you "
                              "have right now.",
                      (150 + current_image.get_width(), 45),
                      pygame.font.SysFont("copperplate", 30), arrow_button.rect.x - 50, (255, 255, 255),
                      alignment="left")
            stop = True
        elif text_show == 5 and player.rect.right - current_level.start > 23 * ss.tile_size and show_instructions:
            screen.blit(surface_text, (75, 25))
            button_lis.append(arrow_button)
            button_lis.append(skip_button)
            screen.blit(current_image, (125, 0))
            blit_text(screen, "Look there is a mystery letter we talked about. It is precious and allows you to convert"
                              " it into any letter from a through z.",
                      (150 + current_image.get_width(), 45),
                      pygame.font.SysFont("copperplate", 30), arrow_button.rect.x - 50, (255, 255, 255),
                      alignment="left")
            stop = True

        elif text_show == 6 and player.rect.right - current_level.start > 49 * ss.tile_size and show_instructions:
            screen.blit(surface_text, (75, 25))
            button_lis.append(arrow_button)
            button_lis.append(skip_button)
            screen.blit(current_image, (125, 0))
            blit_text(screen, "The jumping beautiful object is a super jump power up. When you "
                              "collect this power up, you would be able to jump a higher distance but for a limited "
                              "period of time.",
                      (150 + current_image.get_width(), 45),
                      pygame.font.SysFont("copperplate", 30), arrow_button.rect.x - 50, (255, 255, 255),
                      alignment="left")
            stop = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and stop:
                text_show = change_text({"text_show": text_show})
            for i in button_lis:
                i.check_event(event)

        for i in button_lis:
            i.update(screen)
        pygame.display.update()
        clock.tick(90)


if __name__ == "__main__":
    root = pygame.display.set_mode((ss.SCREEN_WIDTH, ss.SCREEN_HEIGHT))
    opening_page(root)
