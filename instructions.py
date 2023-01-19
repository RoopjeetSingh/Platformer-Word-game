import pygame
import ui_tools
import screen_size as ss
import json

pygame.init()
font = pygame.font.Font(None, 36)
x_pos = 0


def display_text_animation(screen, string: str, text: str, i: int, x: int, y: int):
    """
    Supporter method: only to be used by instructions page to create writing effect
    :param screen: Screen to blit on
    :param string: String to blit
    :param text: the string that has yet been blit on screen
    :param i: the number of words we have blit on the screen yet
    :param x: x position of text
    :param y: y position of text
    :return: returns a tuple of the i which has been incremented and text where the newly added word has been added
    """
    if i < len(string):  # could also be if text == string
        text += string[i]
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(topleft=(x, y))
        screen.blit(text_surface, text_rect)
        pygame.display.update()
        pygame.time.wait(100)
        i += 1
        return i, text


def instructions(screen, back_button_func):
    def change_screen(func):
        with open('variables.json', 'w') as wvar:
            json.dump(var, wvar, indent=4)
        func()

    def go_to_next_page(next_page_bool: bool = True):
        global x_pos
        # Although global is discouraged, this was a place where it is actually suitable. This is because returning
        # a value was not possible in a lambda function and creating a class just for a single x_pos variable was not
        # viable
        if next_page_bool and x_pos > -ss.SCREEN_WIDTH * 3:
            x_pos -= ss.SCREEN_WIDTH
        elif not next_page_bool and x_pos < 0:
            x_pos += ss.SCREEN_WIDTH

        if x_pos <= -ss.SCREEN_WIDTH * 3:
            next_page.state_disabled = True
        else:
            next_page.state_disabled = False

        if x_pos >= 0:
            previous_page.state_disabled = True
        else:
            previous_page.state_disabled = False

        # print(previous_page.state_disabled, next_page.state_disabled, x_pos)

    with open('variables.json', 'r') as f:
        var = json.load(f)
    help_surface = pygame.Surface((ss.SCREEN_WIDTH * 3, ss.SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    background = pygame.image.load("images/Menu_page/menu_bg.png").convert()
    next_button = pygame.transform.scale(pygame.image.load("images/Menu_page/i02_next_button.png").convert_alpha(),
                                         (100, 150))
    disabled_next_button = pygame.transform.scale(
        pygame.image.load("images/Menu_page/i01_next_button.png").convert_alpha(),
        (100, 150))
    previous_button = pygame.transform.flip(next_button, True, False)
    disabled_previous_button = pygame.transform.flip(disabled_next_button, True, False)

    back_image = pygame.transform.scale(pygame.image.load("images/back_button.png").convert_alpha(),
                                        (ss.SCREEN_WIDTH / 14.3, ss.SCREEN_HEIGHT / 8.4))  # 75, 75
    back_button = ui_tools.Button((20, 20, ss.SCREEN_WIDTH / 19.1, ss.SCREEN_HEIGHT / 10.4), (0, 0, 0),
                                  lambda: change_screen(lambda: back_button_func(screen)), image=back_image,
                                  fill_bg=False)

    next_page = ui_tools.Button(
        (ss.SCREEN_WIDTH - 20 - next_button.get_width(), ss.SCREEN_HEIGHT / 2 - next_button.get_height() / 2,
         next_button.get_width(), next_button.get_height()),
        (0, 0, 0), lambda: go_to_next_page(), image=next_button, fill_bg=False, disabled_image=disabled_next_button)
    previous_page = ui_tools.Button(
        (20, ss.SCREEN_HEIGHT / 2 - next_button.get_height() / 2, next_button.get_width(), next_button.get_height()),
        (0, 0, 0), lambda: go_to_next_page(False), image=previous_button, fill_bg=False,
        disabled_image=disabled_previous_button, state_disabled=True)
    button_lis = [back_button, next_page, previous_page]
    while True:
        help_surface.blit(background, (0, 0))
        help_surface.blit(background, (ss.SCREEN_WIDTH, 0))
        help_surface.blit(background, (ss.SCREEN_WIDTH * 2, 0))
        screen.blit(help_surface, (x_pos, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                with open('variables.json', 'w') as wvar:
                    json.dump(var, wvar, indent=4)
                pygame.quit()
                exit()
            for i in button_lis:
                i.check_event(event)

        for i in button_lis:
            i.update(screen)
        pygame.display.update()
        clock.tick()


if __name__ == "__main__":
    from menu import menu

    root = pygame.display.set_mode((ss.SCREEN_WIDTH, ss.SCREEN_HEIGHT))
    instructions(root, menu)
