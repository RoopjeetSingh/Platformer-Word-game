import pygame.image

import ui_tools as pgb
from instructions import instructions
from score_board import scoreboard
from leaderboard import leaderboard
from skins import skins
import json_storer
from Level import *
from level_screen import level_screen
from platformer_game import platformer_game
from helpful_functions import calculate_current_level, blit_text
from decode_file import decode_file
from users import users
from letter import Letter
import random
import smaller_store
import other_small_images
import extra_images
import mp3file_storer

pygame.init()


def menu(screen):
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load(decode_file(mp3file_storer.music))
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

    def change_screen(func):
        with open('json_storer.py', 'w') as wvar:
            wvar.write("var=" + str(var))
        func["func"]()

    def end_screen():
        with open('json_storer.py', 'w') as wvar:
            wvar.write("var=" + str(var))
        pygame.quit()
        exit()

    class PlayerBig:
        def __init__(self):
            self.current_images = idle_images
            # self.techniques = technique_images
            self.index = 0
            self.image = self.current_images[0]

        def change_skin(self):
            self.image = self.current_images[int(self.index)]
            self.index += 0.035
            if self.index >= len(self.current_images):
                self.index = 0
                if technique_images:
                    self.current_images = random.choice(technique_images + idle_images*10)

    def show_multiplayer():
        show_no_multiplayer_page = True
        return show_no_multiplayer_page

    var = json_storer.var

    clock = pygame.time.Clock()
    # background = pygame.image.load(decode_file(smaller_store.main_menu_bg)).convert()
    background = pygame.image.load("images/Menu_page/letter bg.jpg").convert()
    background = pygame.transform.scale(background, (ss.SCREEN_WIDTH, ss.SCREEN_HEIGHT))
    current_user = var["users"][var["current_user"][0]]
    match current_user[2]:
        case "santa":
            "None"
            head_image = pygame.image.load("images/Santa/logo.png")
            idle_images = []
            technique_images = []
            for i in ["images/Santa/Idle (1).png", "images/Santa/Idle (2).png", "images/Santa/Idle (3).png",
                      "images/Santa/Idle (4).png", "images/Santa/Idle (5).png", "images/Santa/Idle (6).png",
                      "images/Santa/Idle (7).png", "images/Santa/Idle (8).png", "images/Santa/Idle (9).png",
                      "images/Santa/Idle (10).png", "images/Santa/Idle (11).png", "images/Santa/Idle (12).png",
                      "images/Santa/Idle (13).png", "images/Santa/Idle (14).png", "images/Santa/Idle (15).png",
                      "images/Santa/Idle (16).png"]:
                img = pygame.image.load(i).convert_alpha()
                img = pygame.transform.scale(img, (375, 375*img.get_height()/img.get_width()))

                # img = pygame.transform.scale(img, (300, 600))
                # img.set_colorkey((0, 0, 0))
                idle_images.append(img)
        case "boy":
            "Extra life"
            head_image = pygame.image.load("images/Boy/logo.png")
            idle_images = []
            technique_images = []
            for i in ["images/Boy/Idle (1).png", "images/Boy/Idle (2).png", "images/Boy/Idle (3).png",
                      "images/Boy/Idle (4).png", "images/Boy/Idle (5).png", "images/Boy/Idle (6).png",
                      "images/Boy/Idle (7).png", "images/Boy/Idle (8).png", "images/Boy/Idle (9).png",
                      "images/Boy/Idle (10).png"]:
                img = pygame.image.load(i).convert_alpha()
                img = pygame.transform.scale(img, (375, 375*img.get_height()/img.get_width()))
                # img.set_colorkey((0, 0, 0))
                idle_images.append(img)
        case "female_zombie":
            "None"
            head_image = pygame.image.load("images/Female_zombie/logo.png")
            idle_images = []
            technique_images = []
            for i in ["images/Female_zombie/Idle (1).png", "images/Female_zombie/Idle (2).png", "images/Female_zombie/Idle (3).png",
                      "images/Female_zombie/Idle (4).png", "images/Female_zombie/Idle (5).png", "images/Female_zombie/Idle (6).png",
                      "images/Female_zombie/Idle (7).png", "images/Female_zombie/Idle (8).png", "images/Female_zombie/Idle (9).png",
                      "images/Female_zombie/Idle (10).png", "images/Female_zombie/Idle (11).png", "images/Female_zombie/Idle (12).png",
                      "images/Female_zombie/Idle (13).png", "images/Female_zombie/Idle (14).png", "images/Female_zombie/Idle (15).png"]:
                img = pygame.image.load(i).convert()
                img = pygame.transform.scale(img, (375, 375*img.get_height()/img.get_width()))

                # img = pygame.transform.scale(img, (300, 600))
                img.set_colorkey((0, 0, 0))
                idle_images.append(img)
        case "male_zombie":
            "None"
            head_image = pygame.image.load("images/Male_zombie/logo.png")
            idle_images = []
            technique_images = []
            for i in ["images/Male_zombie/Idle (1).png", "images/Male_zombie/Idle (2).png", "images/Male_zombie/Idle (3).png",
                      "images/Male_zombie/Idle (4).png", "images/Male_zombie/Idle (5).png", "images/Male_zombie/Idle (6).png",
                      "images/Male_zombie/Idle (7).png", "images/Male_zombie/Idle (8).png", "images/Male_zombie/Idle (9).png",
                      "images/Male_zombie/Idle (10).png", "images/Male_zombie/Idle (11).png", "images/Male_zombie/Idle (12).png",
                      "images/Male_zombie/Idle (13).png", "images/Male_zombie/Idle (14).png", "images/Male_zombie/Idle (15).png"]:
                img = pygame.image.load(i).convert()
                img = pygame.transform.scale(img, (375, 375*img.get_height()/img.get_width()))

                # img = pygame.transform.scale(img, (300, 600))
                img.set_colorkey((0, 0, 0))
                idle_images.append(img)
        case "adventure_boy":
            "None"
            head_image = pygame.image.load("images/Adventure_boy/logo.png")
            idle_images = []
            technique_images = []
            for i in ["images/Adventure_boy/Idle (1).png", "images/Adventure_boy/Idle (2).png", "images/Adventure_boy/Idle (3).png",
                      "images/Adventure_boy/Idle (4).png", "images/Adventure_boy/Idle (5).png", "images/Adventure_boy/Idle (6).png",
                      "images/Adventure_boy/Idle (7).png", "images/Adventure_boy/Idle (8).png", "images/Adventure_boy/Idle (9).png",
                      "images/Adventure_boy/Idle (10).png"]:
                img = pygame.image.load(i).convert()
                img = pygame.transform.scale(img, (375, 375*img.get_height()/img.get_width()))

                # img = pygame.transform.scale(img, (300, 600))
                img.set_colorkey((0, 0, 0))
                idle_images.append(img)
        case "adventure_girl":
            "None"
            head_image = pygame.image.load("images/Adventure_girl/logo.png")
            idle_images = []
            technique_images = []
            for i in ["images/Adventure_girl/Idle (1).png", "images/Adventure_girl/Idle (2).png", "images/Adventure_girl/Idle (3).png",
                      "images/Adventure_girl/Idle (4).png", "images/Adventure_girl/Idle (5).png", "images/Adventure_girl/Idle (6).png",
                      "images/Adventure_girl/Idle (7).png", "images/Adventure_girl/Idle (8).png", "images/Adventure_girl/Idle (9).png",
                      "images/Adventure_girl/Idle (10).png"]:
                img = pygame.image.load(i).convert()
                img = pygame.transform.scale(img, (375, 375*img.get_height()/img.get_width()))

                # img = pygame.transform.scale(img, (300, 600))
                img.set_colorkey((0, 0, 0))
                idle_images.append(img)
        case "cat":
            "Extra life"
            head_image = pygame.image.load("images/Cat/logo.png")
            idle_images = []
            technique_images = []
            for i in ["images/Cat/Idle (1).png", "images/Cat/Idle (2).png", "images/Cat/Idle (3).png",
                      "images/Cat/Idle (4).png", "images/Cat/Idle (5).png", "images/Cat/Idle (6).png",
                      "images/Cat/Idle (7).png", "images/Cat/Idle (8).png", "images/Cat/Idle (9).png",
                      "images/Cat/Idle (10).png"]:
                img = pygame.image.load(i).convert()
                img = pygame.transform.scale(img, (375, 375*img.get_height()/img.get_width()))

                # img = pygame.transform.scale(img, (300, 600))
                img.set_colorkey((0, 0, 0))
                idle_images.append(img)
        case "dinosaur":
            "None"
            head_image = pygame.image.load("images/Dinosaur/logo.png")
            idle_images = []
            technique_images = []
            for i in ["images/Dinosaur/Idle (1).png", "images/Dinosaur/Idle (2).png", "images/Dinosaur/Idle (3).png",
                      "images/Dinosaur/Idle (4).png", "images/Dinosaur/Idle (5).png", "images/Dinosaur/Idle (6).png",
                      "images/Dinosaur/Idle (7).png", "images/Dinosaur/Idle (8).png", "images/Dinosaur/Idle (9).png",
                      "images/Dinosaur/Idle (10).png"]:
                img = pygame.image.load(i).convert()
                img = pygame.transform.scale(img, (375, 375*img.get_height()/img.get_width()))

                # img = pygame.transform.scale(img, (300, 600))
                img.set_colorkey((0, 0, 0))
                idle_images.append(img)
        case "dog":
            "Extra life"
            head_image = pygame.image.load("images/Dog/logo.png")
            idle_images = []
            technique_images = []
            for i in ["images/Dog/Idle (1).png", "images/Dog/Idle (2).png", "images/Dog/Idle (3).png",
                      "images/Dog/Idle (4).png", "images/Dog/Idle (5).png", "images/Dog/Idle (6).png",
                      "images/Dog/Idle (7).png", "images/Dog/Idle (8).png", "images/Dog/Idle (9).png",
                      "images/Dog/Idle (10).png"]:
                img = pygame.image.load(i).convert()
                img = pygame.transform.scale(img, (375, 375*img.get_height()/img.get_width()))

                # img = pygame.transform.scale(img, (300, 600))
                img.set_colorkey((0, 0, 0))
                idle_images.append(img)
        case "knight":
            "speed"
            head_image = pygame.image.load("images/Knight/logo.png")
            idle_images = []
            technique_images = []
            for i in ["images/Knight/Idle (1).png", "images/Knight/Idle (2).png", "images/Knight/Idle (3).png",
                      "images/Knight/Idle (4).png", "images/Knight/Idle (5).png", "images/Knight/Idle (6).png",
                      "images/Knight/Idle (7).png", "images/Knight/Idle (8).png", "images/Knight/Idle (9).png",
                      "images/Knight/Idle (10).png"]:
                img = pygame.image.load(i).convert()
                img = pygame.transform.scale(img, (375, 375*img.get_height()/img.get_width()))

                # img = pygame.transform.scale(img, (300, 600))
                img.set_colorkey((0, 0, 0))
                idle_images.append(img)
        case "ninja_girl":
            "Glide maybe"
            head_image = pygame.image.load("images/Ninja_girl/logo.png")
            idle_images = []
            technique_images = []
            for i in ["images/Ninja_girl/Idle (1).png", "images/Ninja_girl/Idle (2).png", "images/Ninja_girl/Idle (3).png",
                      "images/Ninja_girl/Idle (4).png", "images/Ninja_girl/Idle (5).png", "images/Ninja_girl/Idle (6).png",
                      "images/Ninja_girl/Idle (7).png", "images/Ninja_girl/Idle (8).png", "images/Ninja_girl/Idle (9).png",
                      "images/Ninja_girl/Idle (10).png"]:
                img = pygame.image.load(i).convert_alpha()
                img = pygame.transform.scale(img, (375, 375*img.get_height()/img.get_width()))

                # img = pygame.transform.scale(img, (300, 600))
                # img.set_colorkey((0, 0, 0))
                idle_images.append(img)
        case "ninja_girl2":
            "Glide maybe"
            head_image = pygame.image.load("images/Ninja_girl2/logo.png")
            idle_images = []
            technique_images = []
            for i in ["images/Ninja_girl2/Idle (1).png", "images/Ninja_girl2/Idle (2).png", "images/Ninja_girl2/Idle (3).png",
                      "images/Ninja_girl2/Idle (4).png", "images/Ninja_girl2/Idle (5).png", "images/Ninja_girl2/Idle (6).png",
                      "images/Ninja_girl2/Idle (7).png", "images/Ninja_girl2/Idle (8).png", "images/Ninja_girl2/Idle (9).png",
                      "images/Ninja_girl2/Idle (10).png"]:
                img = pygame.image.load(i).convert_alpha()
                img = pygame.transform.scale(img, (375, 375*img.get_height()/img.get_width()))

                # img = pygame.transform.scale(img, (300, 600))
                # img.set_colorkey((0, 0, 0))
                idle_images.append(img)
        case "pumpkin":
            "big jump"
            head_image = pygame.image.load("images/Pumpkin/logo.png")
            idle_images = []
            technique_images = []
            for i in ["images/Pumpkin/Idle (1).png", "images/Pumpkin/Idle (2).png", "images/Pumpkin/Idle (3).png",
                      "images/Pumpkin/Idle (4).png", "images/Pumpkin/Idle (5).png", "images/Pumpkin/Idle (6).png",
                      "images/Pumpkin/Idle (7).png", "images/Pumpkin/Idle (8).png", "images/Pumpkin/Idle (9).png",
                      "images/Pumpkin/Idle (10).png"]:
                img = pygame.image.load(i).convert()
                img = pygame.transform.scale(img, (375, 375*img.get_height()/img.get_width()))

                # img = pygame.transform.scale(img, (300, 600))
                img.set_colorkey((0, 0, 0))
                idle_images.append(img)
        case "robot":
            "speed and jump"
            head_image = pygame.image.load("images/Robot/logo.png")
            idle_images = []
            technique_images = []
            for i in ["images/Robot/Idle (1).png", "images/Robot/Idle (2).png", "images/Robot/Idle (3).png",
                      "images/Robot/Idle (4).png", "images/Robot/Idle (5).png", "images/Robot/Idle (6).png",
                      "images/Robot/Idle (7).png", "images/Robot/Idle (8).png", "images/Robot/Idle (9).png",
                      "images/Robot/Idle (10).png"]:
                img = pygame.image.load(i).convert()
                img = pygame.transform.scale(img, (375, 375*img.get_height()/img.get_width()))

                # img = pygame.transform.scale(img, (300, 600))
                img.set_colorkey((0, 0, 0))
                idle_images.append(img)
        case _:
            raise AttributeError

    score_board_img = pygame.transform.scale(
        pygame.image.load(decode_file(smaller_store.scoreboard_bg)).convert_alpha(),
        (75, 50))  # 150, 100
    leader_board_img = pygame.transform.scale(
        pygame.image.load("images/Menu_page/leaderboard.png").convert_alpha(),
        (50, 50))  # 125, 125
    transparent_bg = pygame.transform.scale(
        pygame.image.load("images/Menu_page/transparent_bg.png").convert_alpha(),
        (200, ss.SCREEN_HEIGHT - 630))
    # transparent_bg.set_alpha(100)
    skins_img = pygame.image.load(decode_file(smaller_store.skins_bg)).convert()
    skins_img = pygame.transform.scale(
        skins_img,
        (200, 100))  # 200, 100
    # lock = pygame.transform.scale(
    #     pygame.image.load(decode_file(other_small_images.lock_bg)).convert_alpha(),
    #     (3 * ss.SCREEN_WIDTH / 16, 3 * ss.SCREEN_HEIGHT / 16))

    single_player_bg = pygame.image.load("images/Menu_page/single player bg.jpeg").convert()
    single_player_bg = pygame.transform.scale(single_player_bg, (ss.SCREEN_WIDTH - 1100, 130))

    instruction_button_bg = pygame.image.load("images/Menu_page/instructions button bg.png").convert()
    instruction_button_bg = pygame.transform.scale(instruction_button_bg, (ss.SCREEN_WIDTH - 1100, 130))

    quit_bg = pygame.image.load("images/Menu_page/quit bg.png").convert_alpha()
    quit_bg = pygame.transform.scale(quit_bg, (ss.SCREEN_WIDTH - 1100, 130))

    leader_board_img.set_colorkey((255, 255, 255))

    level_img = calculate_current_level(var)
    level_img = level_img.bg_display
    level_img = pygame.transform.scale(
        level_img,
        (ss.SCREEN_WIDTH - 1100, 130))

    faint_bg = pygame.image.load("images/Menu_page/faint_black_bg.png").convert_alpha()
    faint_bg_change_level = pygame.transform.scale(faint_bg, (175, 30))
    faint_bg_quit = pygame.transform.scale(faint_bg, (65, 30))
    # faint_bg_change_level.set_alpha(200)
    head_image = pygame.transform.scale(head_image, (50, 50))

    quit_button = pgb.Button((0, ss.SCREEN_HEIGHT - 130 - 7, ss.SCREEN_WIDTH - 1100 + 7, 130 + 7),
                             (255, 185, 2),
                             end_screen, hover_color=(254, 158, 2),
                             clicked_color=(187, 99, 5), text="Quit",
                             font=pygame.font.Font(None, 38), image=[quit_bg, faint_bg_quit],
                             image_position=[None, (2.5, 130 - 30)], text_position=(5, 130 - 28),
                             border_radius=int(ss.SCREEN_WIDTH // 143), border_color=(0, 0, 0))
    users_button = pgb.Button(
        (0, 0, 200, 60), (0, 0, 0),
        change_screen, hover_color=(150, 150, 150), clicked_color=(80, 80, 80), text=str(current_user[0]).title(),
        font=pygame.font.Font(None, 30), image=head_image,
        image_position=(5, 5), text_position=(65, 10),
        func=lambda: users(screen, menu))
    current_level = "Completed"
    for level in level_list:
        for i in current_user[1]:
            if i and level.str == i[0]:
                break
        else:
            current_level = level.str
            break
    instructions_btn = pgb.Button((0, 140 - 3.5, ss.SCREEN_WIDTH - 1100 + 7, 130 + 7),
                                  (255, 255, 255), change_screen, func=lambda: instructions(screen, menu),
                                  hover_color=(150, 150, 150), clicked_color=(80, 80, 80), text="Instructions",
                                  font=pygame.font.Font(None, 38), image=[instruction_button_bg, faint_bg_change_level],
                                  image_position=[None, (0, 130 - 30)], text_position=(5, 130 - 28),
                                  border_radius=int(ss.SCREEN_WIDTH // 143), border_color=(0, 0, 0))
    scoreboard_btn = pgb.Button(
        (ss.SCREEN_WIDTH/2 - 200 - 50, 630, 200, ss.SCREEN_HEIGHT - 630),
        (255, 255, 255), change_screen, func=lambda: scoreboard(screen, menu),
        hover_color=(150, 150, 150), clicked_color=(80, 80, 80),
        image=[transparent_bg, score_board_img],
        text="Score Board",
        image_position=[None, (200 / 2 - score_board_img.get_width() / 2, 0)], fill_bg=False,
        font_color=(0, 0, 0))
    scoreboard_btn.text_position = (200 / 2 - scoreboard_btn.text.get_width() / 2, 55)
    leaderboard_btn = pgb.Button(
        (ss.SCREEN_WIDTH/2 + 50, 630, 200, ss.SCREEN_HEIGHT - 630),
        (255, 255, 255), change_screen,
        hover_color=(150, 150, 150), clicked_color=(80, 80, 80), image=[transparent_bg, leader_board_img],
        text="Leaderboard", image_position=[None, (200 / 2 - leader_board_img.get_width() / 2, 0)], fill_bg=False,
        font_color=(0, 0, 0), func=lambda: leaderboard(screen, menu))
    leaderboard_btn.text_position = (200 / 2 - leaderboard_btn.text.get_width() / 2, 55)

    single_player = pgb.Button(
        (1100 - 7, 160 - 3.5, ss.SCREEN_WIDTH - 1100 + 7, 130 + 7),
        (255, 185, 2), change_screen, hover_color=(254, 158, 2),
        clicked_color=(187, 99, 5), func=lambda: platformer_game(screen, menu),
        text="Single player", border_radius=int(ss.SCREEN_WIDTH // 143), border_color=(0, 0, 0),
        font=pygame.font.Font(None, 38), image=[single_player_bg, faint_bg_change_level], image_position=[None, None])
    # multiplayer = pgb.Button(
    #     (3 * ss.SCREEN_WIDTH / 4 - 3 * ss.SCREEN_WIDTH / 16, ss.SCREEN_HEIGHT / 2, 3 * ss.SCREEN_WIDTH / 16,
    #      3 * ss.SCREEN_HEIGHT / 16),
    #     (5, 176, 254), show_multiplayer, hover_color=(8, 143, 254), clicked_color=(2, 92, 177),
    #     text="Multiplayer", border_radius=10, border_color=(8, 143, 254),
    #     font=pygame.font.Font(None, int(ss.SCREEN_WIDTH // 29.79)), image=lock,
    #     image_position=(0, 0))
    # multiplayer.text_position = (multiplayer.rect.w / 2 - multiplayer.text.get_width() / 2,
    #                              multiplayer.rect.h / 2 - multiplayer.text.get_height() / 2)
    skins_btn = pgb.Button(
        (0, 350 - 3.5, ss.SCREEN_WIDTH - 1100 + 7, 130 + 7),
        (255, 185, 2), change_screen, hover_color=(254, 158, 2),
        clicked_color=(187, 99, 5), font_color=(0, 0, 0), border_radius=int(ss.SCREEN_WIDTH // 143),
        border_color=(0, 0, 0),
        text="Avatar", image=skins_img, image_align="bottom", func=lambda: skins(screen, menu))
    level_btn = pgb.Button(
        (1100 - 7, 450 - 3.5,
         level_img.get_width() + 7, level_img.get_height() + 7), (255, 185, 2),
        change_screen, hover_color=(254, 158, 2),
        clicked_color=(187, 99, 5), font=pygame.font.Font(None, 35),
        image=[level_img, faint_bg_change_level], border_radius=int(ss.SCREEN_WIDTH // 143),
        image_position=[None, (2.5, level_img.get_height() - 30)], border_color=(0, 0, 0),
        text="Choose Level", text_position=(10, level_img.get_height() - 28),
        func=lambda: level_screen(screen, menu))

    button_lis = [quit_button, single_player, users_button,
                  skins_btn, level_btn, instructions_btn, leaderboard_btn, scoreboard_btn]
    font = pygame.font.Font(None, 30)
    level_text = font.render(current_level.title(), True, (255, 255, 255))
    alpha = 0
    games_played = sorted(var["users"][var["current_user"][0]][1], key=lambda x: (x[0], x[1], x[2], x[3]), reverse=True)

    current_stars = 0
    for level in level_list:
        for game in games_played:
            if level.str == game[0]:
                current_stars += game[1]
                break

    letter_lis = []
    font_stars = pygame.font.Font(decode_file(extra_images.font_new), 50)
    number_stars = font_stars.render(str(current_stars), True, (0, 0, 0))
    faint_bg = pygame.transform.scale(faint_bg, (85, 40))
    star = pygame.image.load("images/Menu_page/Stars.png").convert()
    star = pygame.transform.scale(star, (40 * star.get_width() / star.get_height(), 40))
    star.set_colorkey((0, 0, 0))
    player = PlayerBig()
    # faint_bg.set_alpha(128)
    while True:
        screen.blit(background, (0, 0))
        # screen.blit(surface_stars, (916 + 41/2, 15))
        screen.blit(faint_bg, (916, 18))
        screen.blit(star, (916, 18))
        screen.blit(number_stars, (916 + 41 + 5, 3))
        screen.blit(player.image, (ss.SCREEN_WIDTH/2 - player.image.get_width()/2,
                                   ss.SCREEN_HEIGHT - player.image.get_height()))
        player.change_skin()
        # show_no_multiplayer_page = multiplayer.value_from_function or False
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                end_screen()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                rand_letter = random.choice(tuple(Letter.letter_dic.keys()))
                image = pygame.image.load(decode_file(Letter.letter_dic.get(rand_letter)))
                image = pygame.transform.scale(image, (50, 50))
                letter_lis.append([image, [event.pos[0], event.pos[1]]])
                print(event.pos)
            for i in button_lis:
                i.check_event(event)
        # if show_no_multiplayer_page:
        #     blit_text(screen, "Multiplayer would be added in the next update",
        #               (multiplayer.rect.centerx, multiplayer.rect.bottom + int(ss.SCREEN_WIDTH / 39.72) / 2),
        #               font, multiplayer.rect.right, color=(255, 255, 255, 0), alpha=min(alpha, 255))
        #     if alpha <= 300:  # Don't change this to ss.SCREEN_WIDTH / number
        #         alpha += 0.75

        for i in button_lis:
            i.update(screen)
        screen.blit(level_text, (65, 10 + users_button.text.get_height() + 5))

        for i in letter_lis:
            if i[1][1] + 0.5 < ss.SCREEN_HEIGHT - i[0].get_height():
                i[1][1] += 0.5
            screen.blit(i[0], i[1])
        pygame.display.update()
        clock.tick()
        # print(clock.get_fps())


if __name__ == "__main__":
    root = pygame.display.set_mode((ss.SCREEN_WIDTH, ss.SCREEN_HEIGHT))
    menu(root)
