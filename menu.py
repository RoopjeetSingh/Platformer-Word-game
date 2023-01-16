import ui_tools as pgb
from instructions import instructions
from score_board import scoreboard
from leaderboard import leaderboard
from skins import skins
import json
from Level import *
from level_screen import level_screen
from platformer_game import platformer_game
from helpful_functions import calculate_current_level

pygame.init()


def menu(screen):
    def change_screen(func):
        with open('variables.json', 'w') as wvar:
            json.dump(var, wvar, indent=4)
        func()

    def end_screen():
        with open('variables.json', 'w') as wvar:
            json.dump(var, wvar, indent=4)
        pygame.quit()
        exit()

    with open('variables.json', 'r') as f:
        var = json.load(f)
    clock = pygame.time.Clock()
    background = pygame.image.load("images/Menu_page/menu_bg.png").convert()
    background = pygame.transform.scale(background, (ss.SCREEN_WIDTH, ss.SCREEN_HEIGHT))
    help_text = pygame.transform.scale(pygame.image.load("images/Menu_page/help.png").convert_alpha(),
                                       (ss.SCREEN_WIDTH / 5.7, ss.SCREEN_HEIGHT / 8.4))  # 250, 50
    score_board_img = pygame.transform.scale(
        pygame.image.load("images/Menu_page/scoreboard.png").convert_alpha(),
        (ss.SCREEN_WIDTH / 9.53, ss.SCREEN_HEIGHT / 8.4))  # 150, 100
    leader_board_img = pygame.transform.scale(
        pygame.image.load("images/Menu_page/leaderboard.png").convert_alpha(),
        (ss.SCREEN_WIDTH / 11.1, ss.SCREEN_HEIGHT / 6.7))  # 125, 125
    skins_img = pygame.transform.scale(
        pygame.image.load("images/Menu_page/skins.png").convert(),
        (ss.SCREEN_WIDTH / 7.15, ss.SCREEN_HEIGHT / 8.4))  # 200, 100
    # skins_img.set_colorkey((0, 0, 0))
    leader_board_img.set_colorkey((255, 255, 255))
    level_img = calculate_current_level(var).bg_display
    level_img = pygame.transform.scale(
        level_img,
        (ss.SCREEN_WIDTH / 2.86,
         ss.SCREEN_HEIGHT / 1.56 / level_img.get_width() * level_img.get_height()))

    quit_button = pgb.Button((ss.SCREEN_WIDTH / 2 - 3 * ss.SCREEN_WIDTH / 16 / 2, 3 * ss.SCREEN_HEIGHT / 4,
                              3 * ss.SCREEN_WIDTH / 16, 3 * ss.SCREEN_HEIGHT / 16), (255, 255, 255),
                             end_screen, hover_color=(150, 150, 150), clicked_color=(80, 80, 80), text="Quit",
                             font=pygame.font.Font(None, 80), font_color=(0, 0, 0), border_radius=15)
    instructions_btn = pgb.Button((13 * ss.SCREEN_WIDTH / 16, 0, 3 * ss.SCREEN_WIDTH / 16, 3 * ss.SCREEN_HEIGHT / 16),
                                  (255, 255, 255), lambda: change_screen(lambda: instructions(screen, menu)),
                                  hover_color=(150, 150, 150), clicked_color=(80, 80, 80), image=help_text)
    scoreboard_btn = pgb.Button((0, 13 * ss.SCREEN_HEIGHT / 16, 3 * ss.SCREEN_WIDTH / 16, 3 * ss.SCREEN_HEIGHT / 16),
                                (255, 255, 255), lambda: change_screen(lambda: scoreboard()),
                                hover_color=(150, 150, 150), clicked_color=(80, 80, 80), image=score_board_img,
                                text="Scoreboard", image_align="bottom", font_color=(0, 0, 0))
    leaderboard_btn = pgb.Button(
        (13 * ss.SCREEN_WIDTH / 16, 13 * ss.SCREEN_HEIGHT / 16, 3 * ss.SCREEN_WIDTH / 16, 3 * ss.SCREEN_HEIGHT / 16),
        (255, 255, 255), lambda: change_screen(lambda: leaderboard()),
        hover_color=(150, 150, 150), clicked_color=(80, 80, 80), image=leader_board_img,
        text="Leaderboard", image_align="bottom", font_color=(0, 0, 0))

    single_player = pgb.Button(
        (ss.SCREEN_WIDTH / 4, ss.SCREEN_HEIGHT / 2, 3 * ss.SCREEN_WIDTH / 16, 3 * ss.SCREEN_HEIGHT / 16),
        (255, 185, 2), lambda: change_screen(lambda: platformer_game(screen)), hover_color=(254, 158, 2),
        clicked_color=(187, 99, 5),
        text="Single player", border_radius=10, border_color=(254, 158, 2), font=pygame.font.Font(None, 48))
    multiplayer = pgb.Button(
        (3 * ss.SCREEN_WIDTH / 4 - 3 * ss.SCREEN_WIDTH / 16, ss.SCREEN_HEIGHT / 2, 3 * ss.SCREEN_WIDTH / 16,
         3 * ss.SCREEN_HEIGHT / 16),
        (5, 176, 254), lambda: print("Multiplayer"), hover_color=(8, 143, 254), clicked_color=(2, 92, 177),
        text="Multiplayer", border_radius=10, border_color=(8, 143, 254), font=pygame.font.Font(None, 48))
    skins_btn = pgb.Button(
        (0, 0, 3 * ss.SCREEN_WIDTH / 16, 3 * ss.SCREEN_HEIGHT / 16),
        (255, 255, 255), lambda: change_screen(lambda: skins(screen, menu)), hover_color=(150, 150, 150),
        clicked_color=(80, 80, 80), font_color=(0, 0, 0),
        text="Avatar", image_align="bottom", image=skins_img)
    level_btn = pgb.Button(
        (ss.SCREEN_WIDTH / 2 - level_img.get_width() / 2, ss.SCREEN_HEIGHT / 4 - level_img.get_height() / 2,
         level_img.get_width(), level_img.get_height()), (0, 0, 0), lambda: change_screen(lambda: level_screen(screen)),
        image=level_img)
    button_lis = [quit_button, instructions_btn, scoreboard_btn, leaderboard_btn, single_player, multiplayer,
                  skins_btn, level_btn]

    while True:
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                end_screen()
            for i in button_lis:
                i.check_event(event)

        for i in button_lis:
            i.update(screen)
        pygame.display.update()
        clock.tick()


if __name__ == "__main__":
    root = pygame.display.set_mode((ss.SCREEN_WIDTH, ss.SCREEN_HEIGHT))
    menu(root)
