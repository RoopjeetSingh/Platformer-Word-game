import pygame
import ui_tools as pgb
import screen_size as ss
import json
from Level import level1
from helpful_functions import blit_text

pygame.init()


def opening_page(screen):
    def get_name():
        name_user = name.text
        if name_user:
            var["users"].append([name_user, [], "boy", ["boy", "santa"]])  # [["Roopjeet", [["level1", 3, 256, time],
            # ...], current skin, unlocked skins], ...]
            # Users is a list of people, a dictionary would have been more suitable, but it can not be
            # used because it is not sorted. Later a list of the name and a list that would store another list of
            # level, stars, score and time
            var["current_user"] = [len(var["users"]) - 1, name_user]
            # Current_user is a list with two values, the index of the current user and the actual name

    with open('variables.json', 'r') as f:
        var = json.load(f)
    # if var["1_time"] == "True" and len(var["users"]) == 0:
    clock = pygame.time.Clock()
    background = pygame.transform.scale(pygame.image.load("images/Menu_page/fblaGameBg.jpg"), (ss.SCREEN_WIDTH,
                                                                                               ss.SCREEN_HEIGHT))
    name_surface = pygame.Surface((ss.SCREEN_WIDTH / 2, ss.SCREEN_HEIGHT / 2), pygame.SRCALPHA)
    name = pgb.InputBox(int(name_surface.get_width()/9.5)+ss.SCREEN_WIDTH / 2 - name_surface.get_width() / 2,
                        int(name_surface.get_height()/3.75) + ss.SCREEN_HEIGHT / 2 - name_surface.get_height() / 2,
                        name_surface.get_width() - 2*int(name_surface.get_width()/9.5), 50, (255, 255, 255),
                        color_hover=(255, 255, 255), color_active=(255, 255, 255), text="What is your name?",
                        border_radius=15, font_color=(0, 0, 0), active=True, remove_active=True)
    font = pygame.font.SysFont("copperplate", 32)
    ask_name = font.render("What is your name?", True, (255, 255, 255))
    font_text = pygame.font.SysFont("copperplate", 24, bold=True)
    ok_button = pgb.Button((ss.SCREEN_WIDTH/2 - 175/2,
                            2.6*name_surface.get_height()/4+ss.SCREEN_HEIGHT / 2 - name_surface.get_height() / 2,
                            175, 100), (5, 176, 254), get_name, disabled_color=(156, 153, 157), border_radius=15,
                           hover_color=(8, 143, 254), clicked_color=(2, 92, 177),
                           text="OK", border_color=(8, 143, 254), state_disabled=True,
                           font=pygame.font.Font(None, 48), disabled_border_color=(70, 67, 72))
    button_lis = [ok_button]
    input_lis = [name]
    while True:
        screen.blit(background, (0, 0))
        pygame.draw.rect(name_surface, (100, 103, 127), name_surface.get_rect(), border_radius=15)
        pygame.draw.rect(name_surface, (222, 234, 244),
                         (25, 50 + ask_name.get_height(), name_surface.get_width() - 50, name_surface.get_height() - 75 - ask_name.get_height()),
                         border_radius=15)
        name_surface.blit(ask_name, (name_surface.get_width()/2 - ask_name.get_width()/2, 25))
        blit_text(name_surface, "Pick a name you'd like other users to know you by",
                  (name_surface.get_width()/2, name_surface.get_height()/2), font_text,
                  name_surface.get_width() - name_surface.get_width()/7.91, (95, 99, 110))
        screen.blit(name_surface, (
            ss.SCREEN_WIDTH / 2 - name_surface.get_width() / 2, ss.SCREEN_HEIGHT / 2 - name_surface.get_height() / 2))
        if name.text:
            ok_button.state_disabled = False
        else:
            ok_button.state_disabled = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                with open('variables.json', 'w') as wvar:
                    json.dump(var, wvar, indent=4)
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


# def show_level(screen):

if __name__ == "__main__":
    root = pygame.display.set_mode((ss.SCREEN_WIDTH, ss.SCREEN_HEIGHT))
    opening_page(root)
