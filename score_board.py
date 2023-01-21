import pygame
import ui_tools
import screen_size as ss
import json

font = pygame.font.SysFont("copperplate", 50)


def scoreboard(screen, back_button_func):
    def change_screen(func):
        with open('variables.json', 'w') as wvar:
            json.dump(var, wvar, indent=4)
        func["func"]()

    def scroll(up: dict = {}):
        up = up.get("up", True)

    def bg_font(rect, text_render, surface, color=(101, 39, 108)):
        pygame.draw.rect(surface, color, rect, 4)
        rect_f = text_render.get_rect(center=rect.center)
        surface.blit(text_render, rect_f)

    def make_font(x, y, text):
        rect = pygame.Rect((x, y, 280, 75))
        text_render = font.render(text, True, (255, 255, 255))
        return rect, text_render

    with open('variables.json', 'r') as f:
        var = json.load(f)
    clock = pygame.time.Clock()
    background = pygame.image.load("images/Menu_page/menu_bg.png").convert()
    background = pygame.transform.scale(background, (ss.SCREEN_WIDTH, ss.SCREEN_HEIGHT))
    scoreboard_bg = pygame.image.load("images/Menu_page/scoreboard_bg.jpg").convert()
    scoreboard_bg = pygame.transform.scale(scoreboard_bg, (ss.SCREEN_WIDTH/1.5, ss.SCREEN_HEIGHT/1.5))
    back_image = pygame.transform.scale(pygame.image.load("images/back_button.png").convert_alpha(),
                                        (ss.SCREEN_WIDTH / 14.3, ss.SCREEN_HEIGHT / 8.4))  # 75, 75
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

    font_lis_top = [make_font(101, 165, "Level"), make_font(101 + 280, 165, "Stars"),
                    make_font(101 + 280 * 2, 165, "Score"), make_font(101 + 280 * 3, 165, "Time")]
    font_current_usr = pygame.font.SysFont("copperplate", 50, bold=True)
    current_user_text = font_current_usr.render(var["current_user"][1], True, (255, 0, 0))
    scores_levels_fonts = []

    print(sorted(var["users"][var["current_user"][0]][1], key=lambda x: x[2], reverse=True))
    for index, value in enumerate(sorted(var["users"][var["current_user"][0]][1], key=lambda x: x[2], reverse=True)):
        # for i, stats in enumerate(value):
        scores_levels_fonts.append(make_font(0*280 + 101, (index + 1) * 75+170, str(value[0])))  # Level
        rect = pygame.Rect((2*280 + 101, (index + 1) * 75+170, 280, 75))  # Stars

        scores_levels_fonts.append(make_font(2*280 + 101, (index + 1) * 75+170, str(value[2])))  # Score
        scores_levels_fonts.append(make_font(3*280 + 101, (index + 1) * 75+170, str(value[3])))  # Time

    surface_font = pygame.Surface((ss.SCREEN_WIDTH, 165+75))
    # button_lis = []
    circle_pos = []
    while True:
        screen.blit(background, (0, 0))
        surface_font.blit(background, (0, 0))
        screen.blit(scoreboard_bg, ((ss.SCREEN_WIDTH - scoreboard_bg.get_width())/2,
                                    (ss.SCREEN_HEIGHT - scoreboard_bg.get_height())/2))
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
        for rect_font, text_font in font_lis_top:
            bg_font(rect_font, text_font, surface_font, (61, 158, 28))
        for rect_font, text_font in scores_levels_fonts:
            bg_font(rect_font, text_font, screen)
        back_button.update(surface_font)
        scroll_up.update(surface_font)
        scroll_down.update(screen)
        for circle in circle_pos:
            pygame.draw.circle(screen, (255, 0, 0), circle, 10)
        surface_font.blit(current_user_text, (ss.SCREEN_WIDTH - 15 - current_user_text.get_width(), 20))
        screen.blit(surface_font, (0, 0))
        pygame.display.update()
        clock.tick()


if __name__ == "__main__":
    from menu import menu

    root = pygame.display.set_mode((ss.SCREEN_WIDTH, ss.SCREEN_HEIGHT))
    scoreboard(root, menu)
