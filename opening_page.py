import pygame
import ui_tools
import screen_size as ss
import json_storer
from Level import level_list, level_generator
from helpful_functions import blit_text
from player import Player
from opening_file_word import opening_screen_word
from decode_file import decode_file
import other_small_images
from skins import list_skins, idle_images_list
import extra_images

pygame.init()


def opening_page(screen):
    pygame.mixer.music.load('images/Menu_page/Joshua McLean - Mountain Trials.mp3')
    pygame.mixer.music.play(-1)

    def get_name(name_user=""):
        name_user = name_user or name.text
        if name_user:
            var["users"] = [[name_user, [], "boy"]]
            # [["Roopjeet", [["level1", 3, 256, time],
            # ...], current skin, unlocked skins], ...]
            # Users is a list of people, a dictionary would have been more suitable, but it can not be
            # used because it is not sorted. Later a list of the name and a list that would store another list of
            # level, stars, score and time
            var["current_user"] = [0, name_user]
            with open('json_storer.py', 'w') as wvar:
                wvar.write("var=" + str(var))
            # pygame.mixer.music.stop()
            # Current_user is a list with two values, the index of the current user and the actual name
            show_level(screen)

    def check_length(entered_text):
        if len(name.text) + 1 < 10 and entered_text != " ":
            name.text += entered_text

    var = json_storer.var

    # if var["1_time"] == "True" and len(var["users"]) == 0:
    clock = pygame.time.Clock()
    background = pygame.transform.scale(pygame.image.load(decode_file(other_small_images.opening_page_bg)),
                                        (ss.SCREEN_WIDTH,
                                         ss.SCREEN_HEIGHT))
    name_surface = pygame.Surface((ss.SCREEN_WIDTH / 2, ss.SCREEN_HEIGHT / 2), pygame.SRCALPHA)
    name = ui_tools.InputBox(int(name_surface.get_width() / 9.5) + ss.SCREEN_WIDTH / 2 - name_surface.get_width() / 2,
                             int(name_surface.get_height() / 3.75) + ss.SCREEN_HEIGHT / 2 - name_surface.get_height() / 2,
                             name_surface.get_width() - 2 * int(name_surface.get_width() / 9.5),
                             int(ss.SCREEN_WIDTH / 28.6),
                             (255, 255, 255),
                             color_hover=(255, 255, 255), color_active=(255, 255, 255),
                             border_radius=int(ss.SCREEN_WIDTH / 95.33), font_color=(0, 0, 0), active=True,
                             remove_active=True, function=get_name, function_every_user_press=check_length)
    font = pygame.font.SysFont("copperplate", int(ss.SCREEN_WIDTH / 44.6875))
    ask_name = font.render("What is your name? (Max 10 letters)", True, (255, 255, 255))
    font_text = pygame.font.SysFont("copperplate", int(ss.SCREEN_WIDTH / 59.583), bold=True)
    ok_button = ui_tools.Button((ss.SCREEN_WIDTH / 2 - int(ss.SCREEN_WIDTH / 8.17) / 2,
                                 2.6 * name_surface.get_height() / 4 + ss.SCREEN_HEIGHT / 2 - name_surface.get_height() / 2,
                                 int(ss.SCREEN_WIDTH / 8.17), int(ss.SCREEN_WIDTH / 14.3)), (5, 176, 254), get_name,
                                disabled_color=(156, 153, 157), border_radius=int(ss.SCREEN_WIDTH / 95.33),
                                hover_color=(8, 143, 254), clicked_color=(2, 92, 177),
                                text="OK", border_color=(8, 143, 254), state_disabled=True,
                                font=pygame.font.Font(None, int(ss.SCREEN_WIDTH / 29.79)),
                                disabled_border_color=(70, 67, 72))
    button_lis = [ok_button]
    input_lis = [name]
    while True:
        screen.blit(background, (0, 0))
        pygame.draw.rect(name_surface, (100, 103, 127), name_surface.get_rect(),
                         border_radius=int(ss.SCREEN_WIDTH / 95.33))
        pygame.draw.rect(name_surface, (222, 234, 244),
                         (int(ss.SCREEN_WIDTH / 57.2), int(ss.SCREEN_WIDTH / 28.6) + ask_name.get_height(),
                          name_surface.get_width() - int(ss.SCREEN_WIDTH / 28.6),
                          name_surface.get_height() - int(ss.SCREEN_WIDTH / 19.067) - ask_name.get_height()),
                         border_radius=int(ss.SCREEN_WIDTH / 95.33))
        name_surface.blit(ask_name,
                          (name_surface.get_width() / 2 - ask_name.get_width() / 2, int(ss.SCREEN_WIDTH / 57.2)))
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
                with open('json_storer.py', 'w') as wvar:
                    wvar.write("var=" + str(var))
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


death_bg = pygame.image.load(decode_file(other_small_images.death_screen)).convert_alpha()
death_bg = pygame.transform.scale(death_bg, (
    ss.SCREEN_WIDTH, ss.SCREEN_WIDTH / death_bg.get_width() * death_bg.get_height()))
clock = pygame.time.Clock()
font = pygame.font.SysFont("applesdgothicneo", int(ss.SCREEN_WIDTH / 19.067), bold=True)
retry_img = pygame.transform.scale(pygame.image.load(decode_file(other_small_images.retry)).convert_alpha(), (50, 50))


def show_level(screen):
    text_show = 0

    def killed_screen(alpha):
        blit_text(death_bg, "YOU DIED", (ss.SCREEN_WIDTH / 2, death_bg.get_height() / 5),
                  pygame.font.Font(decode_file(extra_images.font_new), 100), 1000)
        death_bg.set_alpha(alpha)
        screen.blit(death_bg, (0, ss.SCREEN_HEIGHT / 2 - death_bg.get_height() / 2))
        retry_button = ui_tools.Button((
            ss.SCREEN_WIDTH / 2 - ss.SCREEN_WIDTH / 16,
            ss.SCREEN_HEIGHT / 2 + death_bg.get_height() / 2 - 100, ss.SCREEN_WIDTH / 8, 50),
            (59, 83, 121), lambda: show_level(screen), image=retry_img, hover_color=(35, 53, 78),
            clicked_color=(15, 20, 35),
            border_radius=10, border_color=(35, 53, 78))
        if not num:
            button_lis.append(retry_button)

    def show_word_connect():
        start_color = 150
        while start_color >= 0:
            screen.fill((start_color, start_color, start_color))
            start_color -= 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    exit()
            clock.tick()
            pygame.display.flip()

        from platformer_game import platformer_game
        opening_screen_word(
            screen, [letter_obj.letter for letter_obj in player.letter_lis],
            len(player.mystery_letter_lis), time_display, current_level.stars, platformer_game, opening_page,
            current_level)

    def change_text(text_show):
        return text_show["text_show"] + 1

    def skip_instructions():
        show_instructions = False
        return show_instructions

    pressed = False
    var = json_storer.var

    current_level = level_list[0]
    current_level.clear()
    current_level.letter_list = level_generator(current_level.no_of_letter)
    current_level.start = 0
    current_level.make_platforms_objects()
    current_level.make_letters()
    current_level.make_power_ups()
    player = Player(ss.tile_size, ss.SCREEN_HEIGHT - 7 * ss.tile_size, var["users"][var["current_user"][0]][2])
    arrow_img = pygame.image.load(decode_file(other_small_images.arrow)).convert_alpha()
    arrow_img = pygame.transform.scale(arrow_img, (int(ss.SCREEN_WIDTH / 19.067), int(ss.SCREEN_WIDTH / 28.6)))
    button_lis_clear = []
    button_lis = []
    surface_text = pygame.Surface((ss.SCREEN_WIDTH - int(ss.SCREEN_WIDTH / 9.533), int(ss.SCREEN_WIDTH / 4.77)))
    arrow_button = ui_tools.Button((ss.SCREEN_WIDTH - int(ss.SCREEN_WIDTH / 9.533), int(ss.SCREEN_WIDTH / 6.3556),
                                    int(ss.SCREEN_WIDTH / 19.067), int(ss.SCREEN_WIDTH / 28.6)), (0, 0, 0), change_text,
                                   fill_bg=False, image=arrow_img, call_on_release=False)
    skip_button = ui_tools.Button((ss.SCREEN_WIDTH - int(ss.SCREEN_WIDTH / 9.226), int(ss.SCREEN_WIDTH / 5.07), 75, 30),
                                  (80, 80, 80), skip_instructions,
                                  border_radius=int(ss.SCREEN_WIDTH / 95.33), call_on_release=False, text="Skip")
    current_skin = var["users"][var["current_user"][0]][2]
    for index, skin in enumerate(list_skins):
        if skin == current_skin:
            image = idle_images_list[index]
    current_image = pygame.image.load(decode_file(image)).convert()
    current_image = pygame.transform.scale(
        current_image,
        (
            int(ss.SCREEN_WIDTH / 4.0857) / current_image.get_height() * current_image.get_width(),
            int(ss.SCREEN_WIDTH / 4.0857)))
    current_image.set_colorkey((0, 0, 0))
    stop = False
    surface_text.fill((20, 20, 20))
    surface_text.set_alpha(200)
    time_display = current_level.time
    # time_display_current = time.time()
    timer_event = pygame.USEREVENT
    pygame.time.set_timer(timer_event, 1000)
    alpha = 0
    num = False
    while True:
        # if time.time() - show_time_actual >= 1:
        #     show_time -= round(time.time() - show_time_actual)
        #     show_time_actual = time.time()
        arrow_button.kwargs["text_show"] = text_show
        text_show = max(arrow_button.value_from_function, text_show) if arrow_button.value_from_function is not None \
            else text_show
        button_lis_clear.clear()
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
        if killed or time_display == 0:
            killed_screen(alpha)
            num = True
            alpha += 6
        if player.completed:
            show_word_connect()
        time_as_str = f"{time_display // 60: 003d}: {time_display % 60: 003d}"
        # print(time_as_str)
        time_surface = font.render(time_as_str, True, (20, 255, 255))
        screen.blit(time_surface, (ss.SCREEN_WIDTH - time_surface.get_width() - ss.tile_size * 2, ss.tile_size))
        stop = False
        if skip_button.value_from_function is None:
            show_instructions = True
        else:
            show_instructions = False
        # show_instructions = skip_button.value_from_function or True

        if text_show == 0 and show_instructions:
            # screen.blit(surface_text, (75, ss.SCREEN_HEIGHT - 300))
            screen.blit(surface_text, (int(ss.SCREEN_WIDTH / 19.067), int(ss.SCREEN_WIDTH / 57.2)))
            button_lis_clear.append(arrow_button)
            button_lis_clear.append(skip_button)
            screen.blit(current_image, (int(ss.SCREEN_WIDTH / 11.44), 0))
            blit_text(screen, f"Hi there, Hello!!! I'm the game speaking. Let us learn how to play this game. Collect "
                              f"the letters in the runner game and use those letters to create words in the next part. "
                              f"For your help though "
                              f"we also have mystery letters which you can collect and later convert into any "
                              f"letter. For example, if you collected \"h\" and \"t\", you can use the mystery "
                              f"letter and convert it into a \"u\" which would allow you to make \"hut\". But keep "
                              f"track"
                              f"of the time, the more time you use here the less time you would have for the next part "
                              f"where you make the words"
                              f"Cool right, let's get started...",
                      (int(ss.SCREEN_WIDTH / 9.533) + current_image.get_width(), int(ss.SCREEN_WIDTH / 31.78)),
                      pygame.font.SysFont("copperplate", int(ss.SCREEN_WIDTH / 57.2)),
                      arrow_button.rect.x - int(ss.SCREEN_WIDTH / 28.6), (255, 255, 255),
                      alignment="left")
            stop = True
        elif text_show == 1 and show_instructions:
            screen.blit(surface_text, (int(ss.SCREEN_WIDTH / 19.067), int(ss.SCREEN_WIDTH / 57.2)))
            button_lis_clear.append(arrow_button)
            button_lis_clear.append(skip_button)
            screen.blit(current_image, (int(ss.SCREEN_WIDTH / 11.44), 0))
            arrow_keys = pygame.image.load(
                decode_file(other_small_images.arrow_keys)).convert_alpha()
            arrow_keys = pygame.transform.scale(arrow_keys,
                                                (int(ss.SCREEN_WIDTH / 11.92), int(ss.SCREEN_WIDTH / 17.875)))
            right_pos = blit_text(screen, "Use the arrow keys to move",
                                  (int(ss.SCREEN_WIDTH / 9.533) + current_image.get_width(),
                                   int(ss.SCREEN_WIDTH / 31.78)),
                                  pygame.font.SysFont("copperplate", int(ss.SCREEN_WIDTH / 47.67)),
                                  arrow_button.rect.x - int(ss.SCREEN_WIDTH / 28.6), (255, 255, 255),
                                  alignment="left")
            screen.blit(arrow_keys, (right_pos + 5, int(ss.SCREEN_WIDTH / 31.78)))
            stop = True
        elif text_show == 2 and player.rect.right - current_level.start > 5 * ss.tile_size and show_instructions:
            screen.blit(surface_text, (int(ss.SCREEN_WIDTH / 19.067), int(ss.SCREEN_WIDTH / 57.2)))
            button_lis_clear.append(arrow_button)
            button_lis_clear.append(skip_button)
            screen.blit(current_image, (int(ss.SCREEN_WIDTH / 11.44), 0))
            arrow_keys = pygame.image.load(
                decode_file(other_small_images.arrow_keys)).convert_alpha()
            arrow_keys = pygame.transform.scale(arrow_keys,
                                                (int(ss.SCREEN_WIDTH / 11.92), int(ss.SCREEN_WIDTH / 17.875)))
            right_pos = blit_text(screen, "Use the arrow up button or the space bar to jump",
                                  (int(ss.SCREEN_WIDTH / 9.533) + current_image.get_width(),
                                   int(ss.SCREEN_WIDTH / 31.78)),
                                  pygame.font.SysFont("copperplate", int(ss.SCREEN_WIDTH / 47.67)),
                                  arrow_button.rect.x - int(ss.SCREEN_WIDTH / 28.6), (255, 255, 255),
                                  alignment="left")
            screen.blit(arrow_keys, (right_pos + 5, int(ss.SCREEN_WIDTH / 31.78)))
            stop = True
        elif text_show == 3 and player.rect.right - current_level.start > 7 * ss.tile_size and show_instructions:
            screen.blit(surface_text, (int(ss.SCREEN_WIDTH / 19.067), int(ss.SCREEN_WIDTH / 57.2)))
            button_lis_clear.append(arrow_button)
            button_lis_clear.append(skip_button)
            screen.blit(current_image, (int(ss.SCREEN_WIDTH / 11.44), 0))
            blit_text(screen, "Collect these letters!",
                      (int(ss.SCREEN_WIDTH / 9.533) + current_image.get_width(), int(ss.SCREEN_WIDTH / 31.78)),
                      pygame.font.SysFont("copperplate", int(ss.SCREEN_WIDTH / 47.67)),
                      arrow_button.rect.x - int(ss.SCREEN_WIDTH / 28.6), (255, 255, 255),
                      alignment="left")
            stop = True
        elif text_show == 4 and player.rect.right - current_level.start > 15 * ss.tile_size and show_instructions:
            screen.blit(surface_text, (int(ss.SCREEN_WIDTH / 19.067), int(ss.SCREEN_WIDTH / 57.2)))
            button_lis_clear.append(arrow_button)
            button_lis_clear.append(skip_button)
            screen.blit(current_image, (int(ss.SCREEN_WIDTH / 11.44), 0))
            blit_text(screen, "Caution: there is an obstacle. Obstacles look like spikes, snowman or even a christmas "
                              "tree; avoid them or else you would have to make the words from the limited letters you "
                              "have right now.",
                      (int(ss.SCREEN_WIDTH / 9.533) + current_image.get_width(), int(ss.SCREEN_WIDTH / 31.78)),
                      pygame.font.SysFont("copperplate", int(ss.SCREEN_WIDTH / 47.67)),
                      arrow_button.rect.x - int(ss.SCREEN_WIDTH / 28.6), (255, 255, 255),
                      alignment="left")
            stop = True
        elif text_show == 5 and player.rect.right - current_level.start > 23 * ss.tile_size and show_instructions:
            screen.blit(surface_text, (int(ss.SCREEN_WIDTH / 19.067), int(ss.SCREEN_WIDTH / 57.2)))
            button_lis_clear.append(arrow_button)
            button_lis_clear.append(skip_button)
            screen.blit(current_image, (int(ss.SCREEN_WIDTH / 11.44), 0))
            blit_text(screen, "Look there is a mystery letter we talked about. It is precious and allows you to convert"
                              " it into any letter from a through z.",
                      (int(ss.SCREEN_WIDTH / 9.533) + current_image.get_width(), int(ss.SCREEN_WIDTH / 31.78)),
                      pygame.font.SysFont("copperplate", int(ss.SCREEN_WIDTH / 47.67)),
                      arrow_button.rect.x - int(ss.SCREEN_WIDTH / 28.6), (255, 255, 255),
                      alignment="left")
            stop = True

        elif text_show == 6 and player.rect.right - current_level.start > 49 * ss.tile_size and show_instructions:
            screen.blit(surface_text, (int(ss.SCREEN_WIDTH / 19.067), int(ss.SCREEN_WIDTH / 57.2)))
            button_lis_clear.append(arrow_button)
            button_lis_clear.append(skip_button)
            screen.blit(current_image, (int(ss.SCREEN_WIDTH / 11.44), 0))
            blit_text(screen, "The jumping beautiful object is a super jump power up. When you "
                              "collect this power up, you would be able to jump a higher distance but for a limited "
                              "period of time.",
                      (int(ss.SCREEN_WIDTH / 9.533) + current_image.get_width(), int(ss.SCREEN_WIDTH / 31.78)),
                      pygame.font.SysFont("copperplate", int(ss.SCREEN_WIDTH / 47.67)),
                      arrow_button.rect.x - int(ss.SCREEN_WIDTH / 28.6), (255, 255, 255),
                      alignment="left")
            stop = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and stop:
                text_show = change_text({"text_show": text_show})
            if event.type == timer_event and not killed and time_display != 0 and not stop:
                time_display -= 1
            for i in button_lis_clear:
                i.check_event(event)
            for i in button_lis:
                i.check_event(event)

        for i in button_lis_clear:
            i.update(screen)
        for i in button_lis:
            i.update(screen)
        pygame.display.update()
        clock.tick(90)


if __name__ == "__main__":
    root = pygame.display.set_mode((ss.SCREEN_WIDTH, ss.SCREEN_HEIGHT))
    opening_page(root)
