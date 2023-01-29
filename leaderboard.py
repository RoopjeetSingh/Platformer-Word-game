import pygame
import ui_tools
import screen_size as ss
import json

# from helpful_functions import blit_text

font = pygame.font.Font("images/Menu_page/SnowtopCaps.ttf", 50)
y_pos_text = 0
text_width, text_height = 250, 75  # Change text_width


def leaderboard(screen, back_button_func):
    def change_screen(func):
        with open('variables.json', 'w') as wvar:
            json.dump(var, wvar, indent=4)
        func["func"]()

    def create_font(y_pos):
        rank_1_image = pygame.image.load("images/Menu_page/rank1.png").convert_alpha()
        rank_1_image = pygame.transform.scale(rank_1_image, (50, text_height - 10))
        rank_2_image = pygame.image.load("images/Menu_page/rank2.png").convert_alpha()
        rank_2_image = pygame.transform.scale(rank_2_image, (50, text_height - 10))
        rank_3_image = pygame.image.load("images/Menu_page/rank3.png").convert_alpha()
        rank_3_image = pygame.transform.scale(rank_3_image, (50, text_height - 10))
        rank_images_dic = {1: rank_1_image, 2: rank_2_image, 3: rank_3_image}
        surface_list.clear()
        for index, value in enumerate(games_played):
            # Add ranking and reduce the x position of the rect showing the current user
            # Add scrolling
            # add rect boundaries across stars
            rank_type = rank_images_dic.get((index + 1), (index + 1))

            color = (28, 249, 15) if value[0] == var["current_user"][1] else (42, 74, 105)
            surface = pygame.Surface((text_width * 5 + 30, text_height))
            surface.fill(color)
            color_name = (0, 0, 0)
            if isinstance(rank_type, int):
                bg_font((0, 0), make_font(str(index + 1)), surface, 60)
            else:
                if color != (28, 249, 15):
                    color_name = (250, 213, 70)
                surface.blit(rank_type,
                             ((60 - rank_type.get_width()) / 2, (surface.get_height() - rank_type.get_height()) / 2))
            # scores_levels_fonts.append(())  # Name
            bg_font((0 * text_width + 60, 0), make_font(str(value[0]), color_name), surface)
            # scores_levels_fonts.append(())  # Level
            bg_font((1 * text_width + 60, 0), make_font(str(value[1][0])), surface)
            # Decides the arrangement based on the number of Stars -- value[1] is the number of stars
            if int(value[1][1]) == 1:  # x of Stars text
                # stars_surface_list.append([2 * text_width + text_width / 2 - stars_img.get_width() / 2,
                #                            0 + (text_height - stars_img.get_height()) / 2])
                surface.blit(stars_img, (2 * text_width + text_width / 2 - stars_img.get_width() / 2 + 60,
                                         (text_height - stars_img.get_height()) / 2 + y_pos))
            elif int(value[1][1]) == 2:
                # stars_surface_list.append([2 * text_width + text_width / 3 - stars_img.get_width() / 2,
                #                            -0 + (text_height - stars_img.get_height()) / 2])
                surface.blit(stars_img, (2 * text_width + text_width / 3 - stars_img.get_width() / 2 + 60,
                                         (text_height - stars_img.get_height()) / 2))
                # stars_surface_list.append([2 * text_width + 2 * text_width / 3 - stars_img.get_width() / 2,
                #                            -0 + (text_height - stars_img.get_height()) / 2])
                surface.blit(stars_img, (2 * text_width + 2 * text_width / 3 - stars_img.get_width() / 2 + 60,
                                         (text_height - stars_img.get_height()) / 2))
            elif int(value[1][1]) == 3:
                # stars_surface_list.append([2 * text_width + ((text_width / 3 - 75) / 2),
                #                            -0 + (text_height - stars_img.get_height()) / 2])
                surface.blit(stars_img, (2 * text_width + ((text_width / 3 - 75) / 2) + 60,
                                         (text_height - stars_img.get_height()) / 2))
                # stars_surface_list.append([2 * text_width + ((text_width / 3 - 75) / 2) * 3 + 75,
                #                            -0 + (text_height - stars_img.get_height()) / 2])
                surface.blit(stars_img, (2 * text_width + ((text_width / 3 - 75) / 2) * 3 + 75 + 60,
                                         (text_height - stars_img.get_height()) / 2))
                # stars_surface_list.append([2 * text_width + ((text_width / 3 - 75) / 2) * 5 + 75 * 2,
                #                            -0 + (text_height - stars_img.get_height()) / 2])
                surface.blit(stars_img, (2 * text_width + ((text_width / 3 - 75) / 2) * 5 + 75 * 2 + 60,
                                         (text_height - stars_img.get_height()) / 2))

            # scores_levels_fonts.append(())  # Score
            bg_font((3 * text_width + 60, 0), make_font(str(value[1][2])), surface)
            # scores_levels_fonts.append(((4 * text_width,
            #                              0), make_font(str(value[1][3]))))  # Time
            bg_font((4 * text_width + 60, 0), make_font(str(value[1][3])), surface)
            surface_list.append((70, (index + 1) * (text_height + 10) + 170 + y_pos, surface))

    def scroll(up: dict = {}):
        up = up.get("up", True)
        global y_pos_text
        if up:
            y_pos_text += 50
        else:
            y_pos_text -= 50
        # create_font(y_pos_text)

    def bg_font(pos, text_render, surface, width=text_width):
        # draw rect as boundary
        pos = pygame.Rect(pos, (width, text_height))
        # pygame.draw.rect(surface, (255, 255, 255), pos, 2)
        rect_f = text_render.get_rect(center=pos.center)
        surface.blit(text_render, rect_f)

    def make_font(text, color=(0, 0, 0)):
        text_render = font.render(text, True, color)
        return text_render

    with open('variables.json', 'r') as f:
        var = json.load(f)
    clock = pygame.time.Clock()
    background = pygame.image.load("images/Menu_page/menu_bg.png").convert()
    background = pygame.transform.scale(background, (ss.SCREEN_WIDTH, ss.SCREEN_HEIGHT))
    leaderboard_bg = pygame.image.load("images/Menu_page/scoreboard_bg Background Removed.png").convert_alpha()
    leaderboard_bg = pygame.transform.scale(leaderboard_bg, (ss.SCREEN_WIDTH / 1.05, ss.SCREEN_HEIGHT / 1.2))
    leaderboard_bg.set_colorkey((255, 255, 255))
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

    # Could have done this using for loop but any one of them might have some different optimisation than the other
    font_lis_top = [((120, 165), make_font("Name")),
                    ((120 + text_width, 165), make_font("Level")),
                    ((120 + text_width * 2, 165), make_font("Stars")),
                    ((120 + text_width * 3, 165), make_font("Score")),
                    ((120 + text_width * 4, 165), make_font("Time"))]

    font_current_usr = pygame.font.SysFont("copperplate", 50, bold=True)

    current_user_text = font_current_usr.render(var["current_user"][1], True, (255, 0, 0))
    # scores_levels_fonts = []
    # stars_surface_list = []  # Would have lists of x and y position
    stars_img = pygame.image.load('images/Menu_page/Stars.png').convert_alpha()
    stars_img = pygame.transform.scale(stars_img, (80 / stars_img.get_height() * stars_img.get_width(), 70))

    users_top_score = [[user[0], max(user[1], key=lambda x: (x[0], x[1], x[2], x[3]))] for user in var["users"] if
                       len(user[1])]
    games_played = sorted(users_top_score, key=lambda x: (x[1][0], x[1][1], x[1][2], x[1][3]), reverse=True)
    # print(games_played)  # [['Roopjeet', ['level2', 2, 480, 'date']], ['Tanishq', ['level1', 2, 200, 'date']]]
    current_user_rect = []
    surface_list = []
    create_font(0)

    surface_font = pygame.Surface((ss.SCREEN_WIDTH, 165 + text_height))
    down_side_surface = pygame.Surface((ss.SCREEN_WIDTH, ss.SCREEN_HEIGHT - (
            ss.SCREEN_HEIGHT - leaderboard_bg.get_height()) / 2 - 45 - leaderboard_bg.get_height() + 15))
    # button_lis = []
    font_main_text = pygame.font.Font("images/Menu_page/SnowtopCaps.ttf", 100)
    leaderboard_text = font_main_text.render("Leaderboard", True, (0, 0, 0))
    circle_pos = []
    while True:
        if len(surface_list) > 1 and surface_list[-1][1] + stars_img.get_height() + y_pos_text > (
                ss.SCREEN_HEIGHT - leaderboard_bg.get_height()) / 2 + 45 + leaderboard_bg.get_height() + 15:
            scroll_down.state_disabled = False
        else:
            scroll_down.state_disabled = True

        if len(surface_list) > 1 and surface_list[0][1] + y_pos_text < surface_font.get_height():
            scroll_up.state_disabled = False
        else:
            scroll_up.state_disabled = True

        screen.blit(background, (0, 0))
        screen.blit(leaderboard_bg, ((ss.SCREEN_WIDTH - leaderboard_bg.get_width()) / 2,
                                     (ss.SCREEN_HEIGHT - leaderboard_bg.get_height()) / 2 + 45))
        screen.blit(leaderboard_text, (
            ss.SCREEN_WIDTH / 2 - leaderboard_text.get_width() / 2,
            ss.SCREEN_HEIGHT / 10 - leaderboard_text.get_height() / 2))

        surface_font.blit(background, (0, 0))
        surface_font.blit(leaderboard_bg, ((ss.SCREEN_WIDTH - leaderboard_bg.get_width()) / 2,
                                           (ss.SCREEN_HEIGHT - leaderboard_bg.get_height()) / 2 + 45))
        surface_font.blit(leaderboard_text, (
            ss.SCREEN_WIDTH / 2 - leaderboard_text.get_width() / 2,
            ss.SCREEN_HEIGHT / 10 - leaderboard_text.get_height() / 2))
        for rect in current_user_rect:
            pygame.draw.rect(screen, (255, 255, 255), rect, 7, border_radius=15)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                with open('variables.json', 'w') as wvar:
                    json.dump(var, wvar, indent=4)
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                circle_pos.append(event.pos)
                print(event.pos)
            # for i in button_lis:
            #     i.check_event(event)
            back_button.check_event(event)
            scroll_up.check_event(event)
            scroll_down.check_event(event)

        # for i in button_lis:
        #     i.update(screen)
        # for rect_font, text_font in scores_levels_fonts:
        #     bg_font((rect_font[0], rect_font[1] + y_pos_text), text_font, screen)

        for rect_font, text_font in font_lis_top:
            bg_font(rect_font, text_font, surface_font)

        # for rect_stars in stars_surface_list:
        #     screen.blit(stars_img, (rect_stars[0], rect_stars[1] + y_pos_text))
        for posx, posy, surface in surface_list:
            screen.blit(surface, (posx, posy + y_pos_text))

        back_button.update(surface_font)
        scroll_up.update(surface_font)
        scroll_down.update(screen)
        for circle in circle_pos:
            pygame.draw.circle(screen, (255, 0, 0), circle, 10)
        screen.blit(current_user_text, (ss.SCREEN_WIDTH - 15 - current_user_text.get_width(), 20))
        screen.blit(surface_font, (0, 0))
        down_side_surface.blit(background, (0, 0), (
            0, (ss.SCREEN_HEIGHT - leaderboard_bg.get_height()) / 2 + 45 + leaderboard_bg.get_height() - 15,
            background.get_width(), background.get_height()))
        screen.blit(down_side_surface,
                    (0, (ss.SCREEN_HEIGHT - leaderboard_bg.get_height()) / 2 + 45 + leaderboard_bg.get_height() - 15))
        pygame.display.update()
        clock.tick()


if __name__ == "__main__":
    from menu import menu

    root = pygame.display.set_mode((ss.SCREEN_WIDTH, ss.SCREEN_HEIGHT))
    leaderboard(root, menu)
