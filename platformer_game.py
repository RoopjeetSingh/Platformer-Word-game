import pygame.mixer

from player import *
from Level import *
import screen_size as ss
import json_storer
from helpful_functions import calculate_current_level, blit_text
from wordconnect import game_Loop_Wordle
import ui_tools
from decode_file import decode_file
import other_small_images
import extra_images

pygame.init()
death_bg = pygame.image.load(decode_file(other_small_images.death_screen)).convert_alpha()
death_bg = pygame.transform.scale(death_bg, (
    ss.SCREEN_WIDTH, ss.SCREEN_WIDTH / death_bg.get_width() * death_bg.get_height()))
clock = pygame.time.Clock()
font = pygame.font.SysFont("applesdgothicneo", int(ss.SCREEN_WIDTH / 19.067), bold=True)
retry_img = pygame.transform.scale(pygame.image.load(decode_file(other_small_images.retry)).convert_alpha(), (50, 50))
death_sound = pygame.mixer.Sound("images/Menu_page/videogame-death-sound-43894.mp3")


def platformer_game(screen, menu, level=None):
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

        game_Loop_Wordle(
            screen, [letter_obj.letter for letter_obj in player.letter_lis],
            len(player.mystery_letter_lis), time_display, current_level.stars, platformer_game, current_level)

    def killed_screen(alpha):
        blit_text(death_bg, "YOU DIED", (ss.SCREEN_WIDTH / 2, death_bg.get_height() / 5),
                  pygame.font.Font(decode_file(extra_images.font_new), 100), 1000)
        death_bg.set_alpha(alpha)
        screen.blit(death_bg, (0, ss.SCREEN_HEIGHT / 2 - death_bg.get_height() / 2))
        button_menu = ui_tools.Button((
            ss.SCREEN_WIDTH / 2 - 150 - 2 * ss.SCREEN_WIDTH / 16,
            ss.SCREEN_HEIGHT / 2 + death_bg.get_height() / 2 - 100, ss.SCREEN_WIDTH / 8, 50),
            (59, 83, 121), lambda: menu(screen), text="Menu", hover_color=(35, 53, 78), clicked_color=(15, 20, 35),
            border_radius=10, border_color=(35, 53, 78), font=pygame.font.Font(None, int(ss.SCREEN_WIDTH // 29.79)))
        retry_button = ui_tools.Button((
            ss.SCREEN_WIDTH / 2 + 150,
            ss.SCREEN_HEIGHT / 2 + death_bg.get_height() / 2 - 100, ss.SCREEN_WIDTH / 8, 50),
            (59, 83, 121), lambda: platformer_game(screen, menu, level), image=retry_img, hover_color=(35, 53, 78),
            clicked_color=(15, 20, 35),
            border_radius=10, border_color=(35, 53, 78))
        if not num:
            button_lis.append(button_menu)
            button_lis.append(retry_button)

    pressed = False
    var = json_storer.var
        

    current_level = level or calculate_current_level(var)
    if current_level.str == level_list[0].str:
        import opening_page
        opening_page.show_level(screen)
    current_level.clear()
    current_level.letter_list = level_generator(current_level.no_of_letter)
    current_level.start = 0
    current_level.make_platforms_objects()
    current_level.make_letters()
    current_level.make_power_ups()
    # current_level = current_level()
    time_display = current_level.time
    # time_display_current = time.time()
    timer_event = pygame.USEREVENT
    pygame.time.set_timer(timer_event, 1000)
    player = Player(ss.tile_size, ss.tile_size * 2, var["users"][var["current_user"][0]][2])
    # print(pygame.font.get_fonts())
    alpha = 0
    button_lis = []
    num = False

    while True:
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
        player.double_jump_power_up = True
        pressed, killed = player.update_player(screen, current_level, pressed)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and \
                    event.key == pygame.K_r:
                platformer_game(screen, menu, level)
            if event.type == timer_event and not killed and time_display != 0:
                time_display -= 1
            for i in button_lis:
                i.check_event(event)
        if killed or time_display == 0:
            if alpha == 0:
                pygame.mixer.Sound.play(death_sound)
                pygame.mixer.music.stop()
            killed_screen(alpha)
            num = True
            alpha += 6
        if player.completed:
            show_word_connect()

        time_as_str = f"{time_display // 60: 003d}: {time_display % 60: 003d}"
        # print(time_as_str)
        time_surface = font.render(time_as_str, True, (20, 255, 255))
        time_surface.set_alpha(int(ss.SCREEN_WIDTH / 7.15))
        screen.blit(time_surface, (ss.SCREEN_WIDTH - time_surface.get_width() - ss.tile_size * 2, ss.tile_size))
        for i in button_lis:
            i.update(screen)
        pygame.display.update()
        clock.tick(90)


if __name__ == "__main__":
    from menu import menu

    root = pygame.display.set_mode((ss.SCREEN_WIDTH, ss.SCREEN_HEIGHT))
    platformer_game(root, menu, level5)
