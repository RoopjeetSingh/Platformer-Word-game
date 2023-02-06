import pygame
import ui_tools
import screen_size as ss
import json
from decode_file import decode_file
import smaller_store
import other_small_images
import extra_images

# from helpful_functions import blit_text

font = pygame.font.Font("images/Menu_page/SnowtopCaps.ttf", int(ss.SCREEN_WIDTH/28.6))
text_width, text_height = ss.SCREEN_WIDTH/5.72, ss.SCREEN_WIDTH/19.07  # Change text_width


def leaderboard(screen, back_button_func):
    def change_screen(func):
        with open('variables.json', 'w') as wvar:
            json.dump(var, wvar, indent=4)
        func["func"]()

    def create_font(y_pos):
        rank_1_image = pygame.image.load(decode_file(smaller_store.rank1)).convert_alpha()
        rank_1_image = pygame.transform.scale(rank_1_image, (int(ss.SCREEN_WIDTH/28.6), text_height - 10))
        rank_2_image = pygame.image.load(decode_file(smaller_store.rank2)).convert_alpha()
        rank_2_image = pygame.transform.scale(rank_2_image, (int(ss.SCREEN_WIDTH/28.6), text_height - 10))
        rank_3_image = pygame.image.load(decode_file(smaller_store.rank3)).convert_alpha()
        rank_3_image = pygame.transform.scale(rank_3_image, (int(ss.SCREEN_WIDTH/28.6), text_height - 10))
        rank_images_dic = {1: rank_1_image, 2: rank_2_image, 3: rank_3_image}
        surface_list.clear()
        for index, value in enumerate(games_played):
            # Add ranking and reduce the x position of the rect showing the current user
            # Add scrolling
            # add rect boundaries across stars
            rank_type = rank_images_dic.get((index + 1), (index + 1))

            color = (28, 249, 15) if value[0] == var["current_user"][1] else (42, 74, 105)
            surface = pygame.Surface((text_width * 5 + int(ss.SCREEN_WIDTH/47.67), text_height))
            surface.fill(color)
            color_name = (0, 0, 0)
            if isinstance(rank_type, int):
                bg_font((0, 0), make_font(str(index + 1)), surface, int(ss.SCREEN_WIDTH/23.8))
            else:
                if color != (28, 249, 15):
                    color_name = (250, 213, 70)
                surface.blit(rank_type,
                             ((int(ss.SCREEN_WIDTH/23.8) - rank_type.get_width()) / 2, (surface.get_height() - rank_type.get_height()) / 2))
            # scores_levels_fonts.append(())  # Name
            bg_font((0 * text_width + int(ss.SCREEN_WIDTH/23.8), 0), make_font(str(value[0]), color_name), surface)
            # scores_levels_fonts.append(())  # Level
            bg_font((1 * text_width + int(ss.SCREEN_WIDTH/23.8), 0), make_font(str(value[1][0])), surface)
            # Decides the arrangement based on the number of Stars -- value[1] is the number of stars
            if int(value[1][1]) == 1:  # x of Stars text
                # stars_surface_list.append([2 * text_width + text_width / 2 - stars_img.get_width() / 2,
                #                            0 + (text_height - stars_img.get_height()) / 2])
                surface.blit(stars_img, (2 * text_width + text_width / 2 - stars_img.get_width() / 2 + int(ss.SCREEN_WIDTH/23.8),
                                         (text_height - stars_img.get_height()) / 2 + y_pos))
            elif int(value[1][1]) == 2:
                # stars_surface_list.append([2 * text_width + text_width / 3 - stars_img.get_width() / 2,
                #                            -0 + (text_height - stars_img.get_height()) / 2])
                surface.blit(stars_img, (2 * text_width + text_width / 3 - stars_img.get_width() / 2 + int(ss.SCREEN_WIDTH/23.8),
                                         (text_height - stars_img.get_height()) / 2))
                # stars_surface_list.append([2 * text_width + 2 * text_width / 3 - stars_img.get_width() / 2,
                #                            -0 + (text_height - stars_img.get_height()) / 2])
                surface.blit(stars_img, (2 * text_width + 2 * text_width / 3 - stars_img.get_width() / 2 + int(ss.SCREEN_WIDTH/23.8),
                                         (text_height - stars_img.get_height()) / 2))
            elif int(value[1][1]) == 3:
                surface.blit(stars_img, (2 * text_width + ((text_width / 3 - int(ss.SCREEN_WIDTH/19.06)) / 2) +
                                         int(ss.SCREEN_WIDTH/23.8),
                                         (text_height - stars_img.get_height()) / 2))
                surface.blit(stars_img, (2 * text_width + ((text_width / 3 - int(ss.SCREEN_WIDTH/19.06)) / 2) * 3 +
                                         int(ss.SCREEN_WIDTH/19.06) + int(ss.SCREEN_WIDTH/23.8),
                                         (text_height - stars_img.get_height()) / 2))
                surface.blit(stars_img, (2 * text_width + ((text_width / 3 - int(ss.SCREEN_WIDTH/19.06)) / 2) * 5 +
                                         int(ss.SCREEN_WIDTH/19.06) * 2 + int(ss.SCREEN_WIDTH/23.8),
                                         (text_height - stars_img.get_height()) / 2))

            # scores_levels_fonts.append(())  # Score
            bg_font((3 * text_width + int(ss.SCREEN_WIDTH/23.8), 0), make_font(str(value[1][2])), surface)
            # scores_levels_fonts.append(((4 * text_width,
            #                              0), make_font(str(value[1][3]))))  # Time
            bg_font((4 * text_width + int(ss.SCREEN_WIDTH/23.8), 0), make_font(str(value[1][3])), surface)
            surface_list.append((int(ss.SCREEN_WIDTH/20.43), (index + 1) * (text_height + 10) + int(ss.SCREEN_WIDTH/8.4)
                                 + y_pos, surface))

    class Scroller:
        def __init__(self):
            self.y_pos_text = 0

        def scroll(self, up: dict = {}):
            up = up.get("up", True)
            # global y_pos_text
            if up:
                self.y_pos_text += int(ss.SCREEN_WIDTH/28.6)
            else:
                self.y_pos_text -= int(ss.SCREEN_WIDTH/28.6)
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
    background = pygame.image.load(decode_file(other_small_images.menu_bg)).convert()
    background = pygame.transform.scale(background, (ss.SCREEN_WIDTH, ss.SCREEN_HEIGHT))
    leaderboard_bg = pygame.image.load(decode_file(extra_images.scoreboard_background)).convert_alpha()
    leaderboard_bg = pygame.transform.scale(leaderboard_bg, (ss.SCREEN_WIDTH / 1.05, ss.SCREEN_HEIGHT / 1.2))
    leaderboard_bg.set_colorkey((255, 255, 255))
    # Left here
    back_image = pygame.transform.scale(pygame.image.load(decode_file(other_small_images.back_button)).convert_alpha(),
                                        (ss.SCREEN_WIDTH / 14.3, ss.SCREEN_HEIGHT / 8.4))  # text_height, text_height
    back_button = ui_tools.Button((20, 20, ss.SCREEN_WIDTH / 19.1, ss.SCREEN_HEIGHT / 10.4), (0, 0, 0),
                                  change_screen, image=back_image,
                                  fill_bg=False, func=lambda: back_button_func(screen))
    go_down = pygame.transform.scale(pygame.image.load(decode_file(other_small_images.next_button)).convert_alpha(),
                                     (ss.SCREEN_WIDTH/14.3, ss.SCREEN_WIDTH/9.53))
    disabled_go_down = pygame.transform.scale(
        pygame.image.load(decode_file(other_small_images.disabled_next_button)).convert_alpha(),
        (ss.SCREEN_WIDTH/14.3, ss.SCREEN_WIDTH/9.53))
    go_down = pygame.transform.rotate(go_down, -90)
    disabled_go_down = pygame.transform.rotate(disabled_go_down, -90)
    go_up = pygame.transform.flip(go_down, False, True)
    disabled_go_up = pygame.transform.flip(disabled_go_down, False, True)
    scroller = Scroller()
    scroll_up = ui_tools.Button(
        (int(ss.SCREEN_WIDTH/1.07) - go_up.get_width() / 2, int(ss.SCREEN_WIDTH/17.875), go_up.get_width(),
         go_up.get_height()),
        (0, 0, 0), scroller.scroll, image=go_up, fill_bg=False, disabled_image=disabled_go_up, state_disabled=True)
    scroll_down = ui_tools.Button(
        (int(ss.SCREEN_WIDTH/1.07) - go_down.get_width() / 2, int(ss.SCREEN_WIDTH/1.93) - go_down.get_height(),
         go_down.get_width(), go_down.get_height()),
        (0, 0, 0), scroller.scroll, image=go_down, fill_bg=False,
        disabled_image=disabled_go_down, state_disabled=True, up=False)

    # Could have done this using for loop but any one of them might have some different optimisation than the other
    starting_y = ss.SCREEN_WIDTH/8.6
    x_start = ss.SCREEN_WIDTH/11.9
    font_lis_top = [((x_start, starting_y), make_font("Name")),
                    ((x_start + text_width, starting_y), make_font("Level")),
                    ((x_start + text_width * 2, starting_y), make_font("Stars")),
                    ((x_start + text_width * 3, starting_y), make_font("Score")),
                    ((x_start + text_width * 4, starting_y), make_font("Time"))]

    font_current_usr = pygame.font.SysFont("copperplate", int(ss.SCREEN_WIDTH/28.6), bold=True)

    current_user_text = font_current_usr.render(var["current_user"][1], True, (255, 0, 0))
    # scores_levels_fonts = []
    # stars_surface_list = []  # Would have lists of x and y position
    stars_img = pygame.image.load(decode_file(smaller_store.stars_img)).convert_alpha()
    stars_img = pygame.transform.scale(stars_img, (int(ss.SCREEN_WIDTH/17.875) / stars_img.get_height() *
                                                   stars_img.get_width(), int(ss.SCREEN_WIDTH/20.4)))

    users_top_score = [[user[0], max(user[1], key=lambda x: (x[0], x[1], x[2], x[3]))] for user in var["users"] if
                       len(user[1])]
    games_played = sorted(users_top_score, key=lambda x: (x[1][0], x[1][1], x[1][2], x[1][3]), reverse=True)
    # print(games_played)  # [['Roopjeet', ['level2', 2, 480, 'date']], ['Tanishq', ['level1', 2, 200, 'date']]]
    current_user_rect = []
    surface_list = []
    create_font(0)

    surface_font = pygame.Surface((ss.SCREEN_WIDTH, starting_y + text_height))
    down_side_surface = pygame.Surface((ss.SCREEN_WIDTH, ss.SCREEN_HEIGHT - (
            ss.SCREEN_HEIGHT - leaderboard_bg.get_height()) / 2 - 45 - leaderboard_bg.get_height() + 15))
    # button_lis = []
    font_main_text = pygame.font.Font("images/Menu_page/SnowtopCaps.ttf", int(ss.SCREEN_WIDTH/14.3))
    leaderboard_text = font_main_text.render("Leaderboard", True, (0, 0, 0))
    # circle_pos = []
    while True:
        if len(surface_list) > 1 and surface_list[-1][1] + stars_img.get_height() + scroller.y_pos_text > (
                ss.SCREEN_HEIGHT - leaderboard_bg.get_height()) / 2 + int(ss.SCREEN_WIDTH/31.78) + \
                leaderboard_bg.get_height() + int(ss.SCREEN_WIDTH/95.3):
            scroll_down.state_disabled = False
        else:
            scroll_down.state_disabled = True

        if len(surface_list) > 1 and surface_list[0][1] + scroller.y_pos_text < surface_font.get_height():
            scroll_up.state_disabled = False
        else:
            scroll_up.state_disabled = True

        screen.blit(background, (0, 0))
        screen.blit(leaderboard_bg, ((ss.SCREEN_WIDTH - leaderboard_bg.get_width()) / 2,
                                     (ss.SCREEN_HEIGHT - leaderboard_bg.get_height()) / 2 + int(ss.SCREEN_WIDTH/31.78)))
        screen.blit(leaderboard_text, (
            ss.SCREEN_WIDTH / 2 - leaderboard_text.get_width() / 2,
            ss.SCREEN_HEIGHT / 10 - leaderboard_text.get_height() / 2))

        surface_font.blit(background, (0, 0))
        surface_font.blit(leaderboard_bg, ((ss.SCREEN_WIDTH - leaderboard_bg.get_width()) / 2,
                                           (ss.SCREEN_HEIGHT - leaderboard_bg.get_height()) / 2 + int(ss.SCREEN_WIDTH/31.78)))
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
        # for rect_font, text_font in scores_levels_fonts:
        #     bg_font((rect_font[0], rect_font[1] + y_pos_text), text_font, screen)

        for rect_font, text_font in font_lis_top:
            bg_font(rect_font, text_font, surface_font)

        # for rect_stars in stars_surface_list:
        #     screen.blit(stars_img, (rect_stars[0], rect_stars[1] + y_pos_text))
        for posx, posy, surface in surface_list:
            screen.blit(surface, (posx, posy + scroller.y_pos_text))

        back_button.update(surface_font)
        scroll_up.update(surface_font)
        scroll_down.update(screen)
        # for circle in circle_pos:
        #     pygame.draw.circle(screen, (255, 0, 0), circle, 10)
        screen.blit(current_user_text, (ss.SCREEN_WIDTH - 15 - current_user_text.get_width(), int(ss.SCREEN_WIDTH/71.5)))
        screen.blit(surface_font, (0, 0))
        down_side_surface.blit(background, (0, 0), (
            0, (ss.SCREEN_HEIGHT - leaderboard_bg.get_height()) / 2 + int(ss.SCREEN_WIDTH/31.78) +
            leaderboard_bg.get_height() - int(ss.SCREEN_WIDTH/95.3),
            background.get_width(), background.get_height()))
        screen.blit(down_side_surface,
                    (0, (ss.SCREEN_HEIGHT - leaderboard_bg.get_height()) / 2 + int(ss.SCREEN_WIDTH/31.78) +
                     leaderboard_bg.get_height() - int(ss.SCREEN_WIDTH/95.3)))
        pygame.display.update()
        clock.tick()


if __name__ == "__main__":
    from menu import menu

    root = pygame.display.set_mode((ss.SCREEN_WIDTH, ss.SCREEN_HEIGHT))
    leaderboard(root, menu)
