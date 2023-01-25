import pygame
import ui_tools
import screen_size as ss
import json
from helpful_functions import blit_text

font = pygame.font.Font("images/Menu_page/SnowtopCaps.ttf", 50)
y_pos_text = 0


def scoreboard(screen, back_button_func):
    def change_screen(func):
        with open('variables.json', 'w') as wvar:
            json.dump(var, wvar, indent=4)
        func["func"]()

    def scroll(up: dict = {}):
        up = up.get("up", True)
        global y_pos_text
        if up:
            y_pos_text += 50
        else:
            y_pos_text -= 50

    def bg_font(rect, text_render, surface):
        # pygame.draw.rect(surface, color, rect, 4)
        rect = pygame.Rect(rect, (text_width, text_height))
        rect_f = text_render.get_rect(center=rect.center)
        surface.blit(text_render, rect_f)

    def make_font(text, color=(0, 0, 0)):
        text_render = font.render(text, True, color)
        return text_render

    with open('variables.json', 'r') as f:
        var = json.load(f)
    clock = pygame.time.Clock()
    background = pygame.image.load("images/Menu_page/menu_bg.png").convert()
    background = pygame.transform.scale(background, (ss.SCREEN_WIDTH, ss.SCREEN_HEIGHT))
    scoreboard_bg = pygame.image.load("images/Menu_page/scoreboard_bg Background Removed.png").convert_alpha()
    scoreboard_bg = pygame.transform.scale(scoreboard_bg, (ss.SCREEN_WIDTH / 1.05, ss.SCREEN_HEIGHT / 1.2))
    scoreboard_bg.set_colorkey((255, 255, 255))
    back_image = pygame.transform.scale(pygame.image.load("images/back_button.png").convert_alpha(),
                                        (ss.SCREEN_WIDTH / 14.3, ss.SCREEN_HEIGHT / 8.4))  # text_height, text_height
    back_button = ui_tools.Button((20, 20, ss.SCREEN_WIDTH / 19.1, ss.SCREEN_HEIGHT / 10.4), (0, 0, 0),
                                  change_screen, image=back_image,
                                  fill_bg=False, func=lambda: back_button_func(screen))
    go_down = pygame.transform.scale(pygame.image.load("images/Menu_page/i02_next_button.png").convert_alpha(),
                                     (100, 150))
    disabled_go_down = pygame.transform.scale(
        pygame.image.load("images/Menu_page/i01_next_button.png").convert_alpha(),
        (100, 150))
    go_down = pygame.transform.rotate(go_down, -90)
    disabled_go_down = pygame.transform.rotate(disabled_go_down, -90)
    go_up = pygame.transform.flip(go_down, False, True)
    disabled_go_up = pygame.transform.flip(disabled_go_down, False, True)
    scroll_up = ui_tools.Button(
        (1340 - go_up.get_width() / 2, 80, go_up.get_width(), go_up.get_height()),
        (0, 0, 0), scroll, image=go_up, fill_bg=False, disabled_image=disabled_go_up, state_disabled=True)
    scroll_down = ui_tools.Button(
        (1340 - go_down.get_width() / 2, 740 - go_down.get_height(), go_down.get_width(), go_down.get_height()),
        (0, 0, 0), scroll, image=go_down, fill_bg=False,
        disabled_image=disabled_go_down, state_disabled=True, up=False)

    text_width, text_height = 280, 75
    font_lis_top = [((101, 165), make_font("Level")),
                    ((101 + text_width, 165), make_font("Stars")),
                    ((101 + text_width * 2, 165), make_font("Score")),
                    ((101 + text_width * 3, 165), make_font("Time"))]
    font_current_usr = pygame.font.SysFont("copperplate", 50, bold=True)

    current_user_text = font_current_usr.render(var["current_user"][1], True, (255, 0, 0))
    scores_levels_fonts = []
    stars_surface_list = []  # Would have lists of x and y position
    stars_img = pygame.image.load('images/Menu_page/Stars.png').convert_alpha()
    stars_img = pygame.transform.scale(stars_img, (80 / stars_img.get_height() * stars_img.get_width(), 70))

    games_played = sorted(var["users"][var["current_user"][0]][1], key=lambda x: (x[0], x[1], x[2], x[3]), reverse=True)
    if len(games_played) > 15:
        games_played = games_played[:15]
    for index, value in enumerate(games_played):
        scores_levels_fonts.append(((0 * text_width + 101,
                                     (index + 1) * text_height + 170), make_font(str(value[0]))))  # Level
        # Decides the arrangement based on the number of Stars -- value[1] is the number of stars
        if int(value[1]) == 1:
            stars_surface_list.append([1 * text_width + 101 + text_width / 2 - stars_img.get_width() / 2 -
                                       (ss.SCREEN_WIDTH - scoreboard_bg.get_width()) / 2,
                                       (index + 1) * text_height + 170 + (text_height - stars_img.get_height()) / 2])
        elif int(value[1]) == 2:
            stars_surface_list.append([1 * text_width + 101 + text_width / 3 - stars_img.get_width() / 2 - (
                    ss.SCREEN_WIDTH - scoreboard_bg.get_width()) / 2,
                                       (index + 1) * text_height + 170 + (text_height - stars_img.get_height()) / 2])
            stars_surface_list.append([1 * text_width + 101 + 2 * text_width / 3 - stars_img.get_width() / 2 - (
                    ss.SCREEN_WIDTH - scoreboard_bg.get_width()) / 2,
                                       (index + 1) * text_height + 170 + (text_height - stars_img.get_height()) / 2])
        elif int(value[1]) == 3:
            stars_surface_list.append([1 * text_width + 101 + ((text_width / 3 - 75) / 2) - (
                    ss.SCREEN_WIDTH - scoreboard_bg.get_width()) / 2,
                                       (index + 1) * text_height + 170 + (text_height - stars_img.get_height()) / 2])
            stars_surface_list.append([1 * text_width + 101 + ((text_width / 3 - 75) / 2) * 3 + 75 - (
                    ss.SCREEN_WIDTH - scoreboard_bg.get_width()) / 2,
                                       (index + 1) * text_height + 170 + (text_height - stars_img.get_height()) / 2])
            stars_surface_list.append([1 * text_width + 101 + ((text_width / 3 - 75) / 2) * 5 + 75 * 2 - (
                    ss.SCREEN_WIDTH - scoreboard_bg.get_width()) / 2,
                                       (index + 1) * text_height + 170 + (text_height - stars_img.get_height()) / 2])

        scores_levels_fonts.append(((2 * text_width + 101,
                                     (index + 1) * text_height + 170), make_font(str(value[2]))))  # Score
        scores_levels_fonts.append(((3 * text_width + 101,
                                     (index + 1) * text_height + 170), make_font(str(value[3]))))  # Time

    surface_font = pygame.Surface((ss.SCREEN_WIDTH, 165 + text_height))
    down_side_surface = pygame.Surface((ss.SCREEN_WIDTH, ss.SCREEN_HEIGHT - (
            ss.SCREEN_HEIGHT - scoreboard_bg.get_height()) / 2 - 45 - scoreboard_bg.get_height() + 15))
    # button_lis = []
    font_main_text = pygame.font.Font("images/Menu_page/SnowtopCaps.ttf", 100)
    scoreboard_text = font_main_text.render("ScoreBoard", True, (0, 0, 0))
    # circle_pos = []
    while True:
        if len(stars_surface_list) > 1 and stars_surface_list[-1][1] + stars_img.get_height() + y_pos_text > (
                ss.SCREEN_HEIGHT - scoreboard_bg.get_height()) / 2 + 45 + scoreboard_bg.get_height() + 15:
            scroll_down.state_disabled = False
        else:
            scroll_down.state_disabled = True

        if len(stars_surface_list) > 1 and stars_surface_list[0][1] + y_pos_text < surface_font.get_height():
            scroll_up.state_disabled = False
        else:
            scroll_up.state_disabled = True

        screen.blit(background, (0, 0))
        screen.blit(scoreboard_bg, ((ss.SCREEN_WIDTH - scoreboard_bg.get_width()) / 2,
                                    (ss.SCREEN_HEIGHT - scoreboard_bg.get_height()) / 2 + 45))
        # scoreboard_bg.blit(scoreboard_bg, (0, 0))
        screen.blit(scoreboard_text, (
            ss.SCREEN_WIDTH / 2 - scoreboard_text.get_width() / 2,
            ss.SCREEN_HEIGHT / 10 - scoreboard_text.get_height() / 2))

        surface_font.blit(background, (0, 0))
        surface_font.blit(scoreboard_bg, ((ss.SCREEN_WIDTH - scoreboard_bg.get_width()) / 2,
                                          (ss.SCREEN_HEIGHT - scoreboard_bg.get_height()) / 2 + 45))
        surface_font.blit(scoreboard_text, (
            ss.SCREEN_WIDTH / 2 - scoreboard_text.get_width() / 2,
            ss.SCREEN_HEIGHT / 10 - scoreboard_text.get_height() / 2))

        if len(games_played) < 15:
            play_more_y = 170+text_height*2 if len(stars_surface_list) == 0 \
                else stars_surface_list[-1][1] + text_height*1.5
            blit_text(screen, "Play more to add scores", (ss.SCREEN_WIDTH/2, play_more_y),
                      pygame.font.Font("images/Menu_page/SnowtopCaps.ttf", 42),
                      3*ss.SCREEN_WIDTH/4)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                with open('variables.json', 'w') as wvar:
                    json.dump(var, wvar, indent=4)
                pygame.quit()
                exit()
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     circle_pos.append(event.pos)
            #     print(event.pos)
            # for i in button_lis:
            #     i.check_event(event)
            back_button.check_event(event)
            scroll_up.check_event(event)
            scroll_down.check_event(event)

        # for i in button_lis:
        #     i.update(screen)
        for rect_font, text_font in scores_levels_fonts:
            bg_font((rect_font[0], rect_font[1] + y_pos_text), text_font, screen)

        for rect_font, text_font in font_lis_top:
            bg_font(rect_font, text_font, surface_font)

        for rect_stars in stars_surface_list:
            screen.blit(stars_img, (rect_stars[0], rect_stars[1] + y_pos_text))

        back_button.update(surface_font)
        scroll_up.update(surface_font)
        scroll_down.update(screen)
        # for circle in circle_pos:
        #     pygame.draw.circle(screen, (255, 0, 0), circle, 10)
        screen.blit(current_user_text, (ss.SCREEN_WIDTH - 15 - current_user_text.get_width(), 15))
        screen.blit(surface_font, (0, 0))
        down_side_surface.blit(background, (0, 0), (
            0, (ss.SCREEN_HEIGHT - scoreboard_bg.get_height()) / 2 + 45 + scoreboard_bg.get_height() - 15,
            background.get_width(), background.get_height()))
        screen.blit(down_side_surface,
                    (0, (ss.SCREEN_HEIGHT - scoreboard_bg.get_height()) / 2 + 45 + scoreboard_bg.get_height() - 15))
        pygame.display.update()
        clock.tick()


if __name__ == "__main__":
    from menu import menu

    root = pygame.display.set_mode((ss.SCREEN_WIDTH, ss.SCREEN_HEIGHT))
    scoreboard(root, menu)
