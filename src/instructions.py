import pygame
import ui_tools
import screen_size as ss
import json_storer
from helpful_functions import blit_text
from decode_file import decode_file
import other_small_images

pygame.init()
font = pygame.font.Font(None, int(ss.SCREEN_WIDTH / 39.72))


def instructions(screen, back_button_func):
    def change_screen(func):
        with open('json_storer.py', 'w') as wvar:
            wvar.write("var=" + str(var))
        func["func"]()

    class Scroller:
        def __init__(self):
            self.x_pos = 0

        def go_to_next_page(self, next_page_bool: dict = {}):
            # global x_pos
            # Although global is discouraged, this was a place where it is actually suitable. This is because returning
            # a value was not possible in a lambda function and creating a class just for a single x_pos variable was not
            # viable
            next_page_bool = next_page_bool.get("next_page_bool", True)
            if next_page_bool and self.x_pos > -ss.SCREEN_WIDTH * 3:
                self.x_pos -= ss.SCREEN_WIDTH
            elif not next_page_bool and self.x_pos < 0:
                self.x_pos += ss.SCREEN_WIDTH

            if self.x_pos <= -ss.SCREEN_WIDTH * 3:
                next_page.state_disabled = True
            else:
                next_page.state_disabled = False

            if self.x_pos >= 0:
                previous_page.state_disabled = True
            else:
                previous_page.state_disabled = False

            # print(previous_page.state_disabled, next_page.state_disabled, x_pos)

    var = json_storer.var

    help_surface = pygame.Surface((ss.SCREEN_WIDTH * 3, ss.SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    background = pygame.image.load(decode_file(other_small_images.instruction_bg)).convert()
    background = pygame.transform.scale(background, (ss.SCREEN_WIDTH, ss.SCREEN_HEIGHT))
    next_button = pygame.transform.scale(pygame.image.load(decode_file(other_small_images.next_button)).convert_alpha(),
                                         (ss.SCREEN_WIDTH / 14.3, ss.SCREEN_WIDTH / 9.53))
    disabled_next_button = pygame.transform.scale(
        pygame.image.load(decode_file(other_small_images.disabled_next_button)).convert_alpha(),
        (ss.SCREEN_WIDTH / 14.3, ss.SCREEN_WIDTH / 9.53))
    previous_button = pygame.transform.flip(next_button, True, False)
    disabled_previous_button = pygame.transform.flip(disabled_next_button, True, False)

    back_image = pygame.transform.scale(pygame.image.load(decode_file(other_small_images.back_button)).convert_alpha(),
                                        (ss.SCREEN_WIDTH / 14.3, ss.SCREEN_HEIGHT / 8.4))  # 75, 75
    back_button = ui_tools.Button((20, 20, ss.SCREEN_WIDTH / 19.1, ss.SCREEN_HEIGHT / 10.4), (0, 0, 0),
                                  change_screen, image=back_image,
                                  fill_bg=False, func=lambda: back_button_func(screen))
    scroller = Scroller()
    next_page = ui_tools.Button(
        (ss.SCREEN_WIDTH - 20 - next_button.get_width(), ss.SCREEN_HEIGHT / 2 - next_button.get_height() / 2,
         next_button.get_width(), next_button.get_height()),
        (0, 0, 0), scroller.go_to_next_page, image=next_button, fill_bg=False, disabled_image=disabled_next_button)
    previous_page = ui_tools.Button(
        (20, ss.SCREEN_HEIGHT / 2 - next_button.get_height() / 2, next_button.get_width(), next_button.get_height()),
        (0, 0, 0), scroller.go_to_next_page, image=previous_button, fill_bg=False,
        disabled_image=disabled_previous_button, state_disabled=True, next_page_bool=False)
    button_lis = [back_button, next_page, previous_page]

    while True:
        help_surface.blit(background, (0, 0))
        help_surface.blit(background, (ss.SCREEN_WIDTH, 0))
        help_surface.blit(background, (ss.SCREEN_WIDTH * 2, 0))

        table = pygame.Surface((1000, 550))
        table.set_alpha(128)
        table.fill((255, 255, 255))
        # first screen - how to use the game
        blit_text(help_surface, "Instructions", (650, 100),
                  pygame.font.Font(None, 100), 900, color=(255, 255, 255))

        help_surface.blit(table, (150, 150))
        blit_text(help_surface, "HOW TO PLAY THE GAME", (650, 200),
                  pygame.font.Font(None, 50), 900, color=(130, 1, 29))
        blit_text(help_surface, "GOAL: ", (210, 250),
                  pygame.font.Font(None, 40), 300, color=(130, 1, 29))
        blit_text(help_surface,
                  "COLLECT LETTERS IN THE RUNNING GAME AND USE THEM IN THE WORD-CONNECT GAME TO EARN POINTS BEFORE THE TIME RUNS OUT",
                  (200, 300),
                  pygame.font.Font(None, 25), 650, color=(130, 1, 29), alignment="left")
        blit_text(help_surface, "ADVANCED FEATURES: ", (320, 420),
                  pygame.font.Font(None, 40), 405, color=(130, 1, 29))
        blit_text(help_surface,
                  "ADD USER: CLICK ON THE USER BUTTON WHERE YOU CAN ADD USERS TO PLAY WITH FRIENDS.",
                  (200, 450),
                  pygame.font.Font(None, 20), 650, color=(130, 1, 29), alignment="left")
        blit_text(help_surface,
                  "CHOOSE AN AVATAR: CLICK ON THE AVATAR BUTTON AND THEN ON THE SKIN YOU WANT. EARLIER, ONLY TWO "
                  "AVATARS CAN BE SELECTED, GET MORE STARS TO UNLOCK AVATARS",
                  (200, 510),
                  pygame.font.Font(None, 20), 850, color=(130, 1, 29), alignment="left")
        blit_text(help_surface,
                  "TO START THE GAME, CLICK ON SINGLE-PLAYER, OR TO CHOOSE A LEVEL CLICK ON LEVEL IMAGE OR ICON, "
                  "HERE YOU CAN SEE ALL UNLOCKED LEVELS",
                  (200, 570),
                  pygame.font.Font(None, 20), 850, color=(130, 1, 29), alignment="left")
        blit_text(help_surface,
                  "FOURTH, TO SEE YOUR HIGHEST SCORE OR THE USER WITH THE HIGHEST SCORE, CLICK ON THE SCOREBOARD OR "
                  "THE LEADERBOARD BUTTON, RESPECTIVELY",
                  (200, 630),
                  pygame.font.Font(None, 20), 850, color=(130, 1, 29), alignment="left")

        # second screen - how to play the running game
        blit_text(help_surface, "Instructions", (1950, 100),
                  pygame.font.Font(None, 100), 2200, color=(255, 255, 255))
        help_surface.blit(table, (1450, 150))
        blit_text(help_surface, "RUNNING GAME", (1950, 200),
                  pygame.font.Font(None, 50), 2200, color=(130, 1, 29))
        blit_text(help_surface, "GOAL: ", (1510, 250),
                  pygame.font.Font(None, 40), 1600, color=(130, 1, 29))
        blit_text(help_surface, "DODGE OBSTACLES TO COLLECT LETTERS BEFORE TIME RUNS OUT!!! ", (1500, 310),
                  pygame.font.Font(None, 30), 1900, color=(130, 1, 29), alignment="left")
        blit_text(help_surface, "CONTROLS: ", (1550, 420),
                  pygame.font.Font(None, 40), 1600, color=(130, 1, 29))
        blit_text(help_surface, "MOVE LEFT: A-KEY OR LEFT ARROW KEY", (1500, 450),
                  pygame.font.Font(None, 20), 1950, color=(130, 1, 29), alignment="left")
        blit_text(help_surface, "MOVE RIGHT: D-KEY OR RIGHT ARROW KEY", (1500, 480),
                  pygame.font.Font(None, 20), 1950, color=(130, 1, 29), alignment="left")
        blit_text(help_surface, "JUMP: W-KEY OR UP ARROW KEY OR SPACE BAR", (1500, 510),
                  pygame.font.Font(None, 20), 1950, color=(130, 1, 29), alignment="left")
        blit_text(help_surface, "RESTART: PRESS R TO RESTART LEVEL", (1500, 540),
                  pygame.font.Font(None, 20), 1950, color=(130, 1, 29), alignment="left")
        blit_text(help_surface,
                  "AVOID OBSTACLES LIKE SNOWMAN, TREE, SPIKES BY JUMPING OVER THEM. THERE ARE ALSO POWER-UPS LIKE JUMP-BOOST TO HELP YOU FINISH THE LEVEL.",
                  (1500, 570),
                  pygame.font.Font(None, 20), 2250, color=(130, 1, 29), alignment="left")
        blit_text(help_surface,
                  "TRY TO GET THE MYSTERY LETTER, WHICH YOU CAN USE IN THE NEXT PART OF THE GAME, WORD-CONNECT. THIS WOULD ALLOW YOU TO ADD ANY LETTER OF YOUR WISH WHENEVER YOU NEED IT.",
                  (1500, 620),
                  pygame.font.Font(None, 20), 2250, color=(130, 1, 29), alignment="left")
        # fourth screen - how to play the word-connect game
        blit_text(help_surface, "Instructions", (3250, 100),
                  pygame.font.Font(None, 100), 3500, color=(255, 255, 255))
        help_surface.blit(table, (2750, 150))
        blit_text(help_surface, "WORD-CONNECT", (3250, 200),
                  pygame.font.Font(None, 50), 3500, color=(130, 1, 29))
        blit_text(help_surface, "GOAL:", (2810, 250),
                  pygame.font.Font(None, 40), 2900, color=(130, 1, 29))
        blit_text(help_surface,
                  "MAKE WORDS BY JOINING LETTERS TO GET POINTS. THE NUMBER OF POINTS YOU GET FOR EACH CORRECT WORD WILL DEPEND UPON THE LENGTH OF THE WORD",
                  (2800, 300),
                  pygame.font.Font(None, 25), 3400, color=(130, 1, 29), alignment="left")
        blit_text(help_surface, "CONTROLS: ", (2850, 420),
                  pygame.font.Font(None, 40), 2900, color=(130, 1, 29))
        blit_text(help_surface, "TO MAKE WORDS, SIMPLY CONNECT LETTERS", (2800, 450),
                  pygame.font.Font(None, 20), 3250, color=(130, 1, 29), alignment="left")
        blit_text(help_surface,
                  "TO USE THE MYSTERY LETTER COLLECTED IN THE RUNNING GAME, CLICK ON THE MYSTERY ICON ON THE BOTTON LEFT AND ADD LETTERS IN THE TEXT BOX, BY PRESSING ITS KEY ON KEYBOARD AND THEN PRESSING THE ENTER KEY.",
                  (2800, 490),
                  pygame.font.Font(None, 20), 3450, color=(130, 1, 29), alignment="left")
        blit_text(help_surface,
                  "TO GO TO THE NEXT LEVEL BEFORE TIME RUNS OUT, CLICK ON THE NEXT ARROW BUTTON ON THE BOTTOM RIGHT OF THE SCREEN",
                  (2800, 565),
                  pygame.font.Font(None, 20), 3450, color=(130, 1, 29), alignment="left")

        blit_text(help_surface,
                  "IN THIS GAME YOU CAN UNLOCK NEW LEVELS AND AVATARS ONLY BY GAINING STARS IN THE WORD-CONNECT GAME. IN THE GAME, EACH LEVEL HAS DIFFERENT MAX POINTS, HOWEVER TO HELP YOU TRACK YOUR PROGRESS, A BAR HAS BEEN PROVIDED BELOW THE SCREEN IN THIS PART OF THE GAME.",
                  (2800, 630),
                  pygame.font.Font(None, 20), 3450, color=(130, 1, 29), alignment="left")
        screen.blit(help_surface, (scroller.x_pos, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                with open('json_storer.py', 'w') as wvar:
                    wvar.write("var=" + str(var))
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
