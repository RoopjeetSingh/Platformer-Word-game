import random
import pygame as py
from pygame.locals import *
import math
from pygame import mixer
import main
import ui_tools
from letter import Letter
from helpful_functions import blit_text

import screen_size as ss
import json_storer
from datetime import datetime
from decode_file import decode_file
import other_small_images
import extra_images

# datetime object containing current date and time
current_time = datetime.now()

py.init()
mixer.init()
# Removes letters that are 2 letters long
copy = main.WORDS.copy().keys()
vi = list(copy)
for i in copy:
    if len(i) <= 2:
        vi.remove(i)
        main.WORDS[i] = False

screen = py.display.set_mode((1300, 710))

image_list = [extra_images.zero_stars, extra_images.single_stars, extra_images.double_stars, extra_images.triple_stars]

single_star = ["you were close", "better luck next time", " you can do better than one star"]
double_star = ["good job, now try to get three stars", "you can do better than two stars",
               "you were close to getting three stars"]
triple_star = ["Great job! You are a real Future Business Leader of America!!"]
mystery_letters = []
count = 0
clock_star = py.time.Clock()
x_change = 0
message_show = 1
list_images = Letter.letter_dic

possible_characters = list(list_images.keys())
collect_letter_sound = py.mixer.Sound("images/Menu_page/collectcoin-6075.mp3")
incorrect_word_sound = py.mixer.Sound("images/Menu_page/human-impact-on-ground-6982.mp3")


def background(screen, x, y, z, c):
    bg_image = py.image.load(decode_file(extra_images.word_connect_bg))
    bg_image = py.transform.scale(bg_image, (1300, 710))
    table = py.Surface((550, c))
    table.set_alpha(128)
    table.fill((x, y, z))
    screen.blit(bg_image, (0, 0))
    screen.blit(table, (375, 50))


def background_celeb(screen, x, y, z, c):
    bg_image = py.image.load("images/fjf.webp")
    bg_image = py.transform.scale(bg_image, (1300, 710))
    table = py.Surface((550, c))
    table.set_alpha(128)
    table.fill((x, y, z))
    screen.blit(bg_image, (0, 0))
    screen.blit(table, (375, 50))


def place(screen, n, on, coord, letters, list_images):
    if on == True:
        a = 0
        adding = (2 * 3.14) / n
        for i in range(0, n):
            position = (630 + 190 * math.cos(a), 335 + 190 * math.sin(a))
            im = py.image.load(decode_file(list_images[letters[i]]))
            im = py.transform.scale(im, (40, 40))
            screen.blit(im, (position))
            if len(coord) < len(letters):
                coord.append(position)
            a += adding


def update(incorect, shake_count):
    global x_change
    if shake_count % 2 == 0:
        x_change = 5
    else:
        x_change = -5


def lines(screen, entered):
    if entered != []:
        for cd in range(len(entered) - 1):
            py.draw.line(screen, (34, 153, 153), (entered[cd][0] + 20, entered[cd][1] + 20),
                         (entered[cd + 1][0] + 20, entered[cd + 1][1] + 20), width=3)


def near(x, y, co):
    if co:
        z = []
        for i in range(len(x)):
            z.append((math.sqrt(pow(x[i][0] - y[0], 2)) + math.sqrt(pow(x[i][1] - y[1], 2))))

        return x[z.index(min(z))]


def show(screen, word, x_change):
    font = py.font.Font(None, 50)
    w = ""
    for i in range(len(word)):
        w += word[i]
        text = font.render(w.upper(), True, (255, 255, 255), (0, 234, 56))
        rect = text.get_rect()
        rect.center = 650 + x_change, 90
        screen.blit(text, rect)


def mystery(screen, input, c, pressed, rect_pressed):
    if pressed == True:
        py.draw.circle(screen, (30, 212, 212), (650, 340), 70)
        font = py.font.Font(None, 80)
        if c == 0:
            py.draw.circle(screen, (212, 11, 14), (650, 340), 70)

        if rect_pressed == True and c != 0:
            py.draw.circle(screen, (95, 204, 0), (650, 340), 70, width=5)

            text_pressed = font.render(input.upper(), True, (255, 255, 255))
            text_effect = font.render(input.upper(), True, (0, 0, 0))
            if input != "":
                rect_image = text_pressed.get_rect()
                rect_image.center = (650, 345)
                rect_image_1 = text_effect.get_rect()
                rect_image_1.center = (648, 343)
                screen.blit(text_pressed, (rect_image))
                screen.blit(text_effect, (rect_image_1))


def mystery_and_submit_button(screen, mystery_number):
    font = py.font.Font(None, 75)
    text = font.render(f":{mystery_number}", True, (0, 0, 0))

    image = py.image.load(decode_file(extra_images.question))
    image = py.transform.scale(image, (50, 50))
    py.draw.rect(screen, (22, 171, 171), (20, 545, 130, 65))
    screen.blit(text, (85, 553))
    screen.blit(image, (30, 553))
    if mystery_number == 0:
        surface = py.Surface((130, 65))
        surface.set_alpha(128)
        surface.fill((255, 255, 255))
        screen.blit(surface, (20, 545))
    image = py.image.load(decode_file(other_small_images.arrow))
    image_submit = py.transform.scale(image, (50, 50))
    screen.blit(image_submit, (1150, 550))


def score_show(screen, x, score):
    font = py.font.Font(None, 50)
    if x == True:
        py.draw.rect(screen, (224, 177, 22), (1075, 50, 170, 35))
        text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(text, (1100, 50))

    if x == False:
        text = font.render(f"Score: {score}", True, (0, 0, 0))
        rect = text.get_rect()
        rect.center = (650, 500)
        screen.blit(text, rect)


def shake(screen, shake_count, working, letters, incorrect, on, coord, word, score, list_images, counter,
          mystery_number):
    for i in range(4):
        background(screen, 201, 47, 4, 590)
        mystery_and_submit_button(screen, mystery_number)

        text_draw(screen, counter)

        place(screen, len(letters), on, coord, letters, list_images)
        progress_bar(screen, score, 20, 30)
        show(screen, word, x_change)
        update(incorrect, shake_count)
        py.display.update()
        shake_count += 1


def text_draw(screen, counter):
    py.draw.rect(screen, (blink(counter)), (20, 50, 50, 50))
    font = py.font.Font(None, 30)
    text = font.render(str(counter), True, (255, 255, 255))
    rect = text.get_rect()
    rect.center = 45, 75
    screen.blit(text, rect)


def blink(counter):
    if counter % 2 == 0:
        if counter >= 40:
            return (103, 240, 24)
        elif 20 <= counter < 40:
            return (240, 182, 24)
        elif counter < 20:
            return (240, 64, 24)
    else:
        return (0, 0, 0)


def progress_bar(screen, x, time1, points):
    # remove time1 as a parameter
    x1 = round((x / points) * 500)
    py.draw.rect(screen, (21, 28, 28), (390, 660, 500, 30))
    im = py.image.load(decode_file(extra_images.new_star))
    im = py.transform.scale(im, (42, 35))
    screen.blit(im, (round(395 + 0.2 * 500) - 21, 625))
    screen.blit(im, (round(395 + 0.5 * 500) - 42, 625))
    screen.blit(im, (round(395 + 0.5 * 500), 625))
    screen.blit(im, (round(395 + 500) - 65, 625))
    screen.blit(im, (round(395 + 500) - 25, 625))
    screen.blit(im, (round(395 + 500) + 15, 625))

    if x1 < 500:
        py.draw.rect(screen, (204, 55, 75), (395, 658, 500, 25))
        py.draw.rect(screen, (255, 215, 0), (395, 658, x1, 25))
        py.draw.rect(screen, (80, 199, 100), (395, 658, x1, 25), width=5)
        py.draw.line(screen, (0, 0, 0), (395 + 0.2 * 500, 658), (395 + 0.2 * 500, 683), width=3)
        py.draw.line(screen, (0, 0, 0), (395 + 0.5 * 500, 658), (395 + 0.5 * 500, 683), width=3)
        py.draw.line(screen, (0, 0, 0), (895, 658), (895, 683), width=3)

    else:
        py.draw.rect(screen, (255, 215, 0), (395, 658, 500, 25))

        py.draw.line(screen, (0, 0, 0), (395 + 0.2 * 500, 658), (395 + 0.2 * 500, 683), width=3)
        py.draw.line(screen, (0, 0, 0), (395 + 0.5 * 500, 658), (395 + 0.5 * 500, 683), width=3)
        py.draw.line(screen, (0, 0, 0), (895, 658), (895, 683), width=3)


def stars(screen):
    global count
    clock = py.time.Clock()

    if count <= len(image_list) - 1:
        im = py.image.load(decode_file(image_list[count]))
        im = py.transform.scale(im, (400, 400))
        screen.blit(im, (450, 0))


def update_stars(score, points):
    global count

    if score >= points and count < 3:

        count += 1

    elif round(0.5 * points) <= score < points and count < 2:

        count += 1

    elif round(0.2 * points) < score <= round(0.5 * points) and count < 1:
        count += 1

    elif score == 0:
        count = 0


def celebration(screen, score, x, points):
    if score >= points:
        blit_text(screen, x, (660, 340),
                  py.font.Font(None, 50), 800)
    elif points > score >= round(0.5 * points):
        blit_text(screen, x, (660, 340),
                  py.font.Font(None, 50), 800)
    elif round(0.5 * points) > score >= round(0.2 * points):
        blit_text(screen, x, (660, 340), py.font.Font(None, 50), 800)

    elif round(0.2 * points) > score:
        blit_text(screen, x, (660, 340), py.font.Font(None, 50), 800)


def message(score, points):
    if score >= points:
        x = random.choice(triple_star).title()
    elif points > score >= round(0.5 * points):
        x = random.choice(double_star).title()
    elif round(0.5 * points) > score >= round(0.2 * points):
        x = random.choice(single_star).title()
    elif round(points * 0.2) > score:
        x = "you did not even try".title()

    return x


def get_hints(word_selected):
    for i in vi:
        li = word_selected.copy()
        for c in i:
            if c in li:
                if i.index(c) < (len(i) - 1):
                    li.remove(c)
                else:
                    if len(i) < 4:
                        font = py.font.Font(None, 50)
                        text = font.render(i, True, (0, 0, 0))
                        rect = text.get_rect()
                        rect.center = (650, 355)
                        co = py.Rect(rect.x - 5, rect.y - 5, rect.right - rect.left + 10, rect.bottom - rect.top + 10)

                        rectangle = py.draw.rect(screen, (234, 25, 79), (co))
                        screen.blit(text, rect)
                        vi.remove(i)
                        return i
            else:
                break


def next_level(kwargs):
    platformer = kwargs["platformer"]
    from menu import menu
    platformer(screen, menu)


def choose_random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return r, g, b


class Streak():
    def __init__(self, x, y, screen):
        self.screen = screen
        self.color = choose_random_color()
        self.x = x
        self.y = y
        angle = random.uniform(-60, 240)
        velocity_mag = random.uniform(.3, 2.5)
        self.vx = velocity_mag * math.cos(math.radians(angle))  # velocity x
        self.vy = -velocity_mag * math.sin(math.radians(angle))  # velocity y
        self.timer = 0
        self.ended = False

    def get_angle(self):
        return math.atan2(-self.vy, self.vx)

    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.timer += 1
        if self.timer >= 90:
            self.ended = True

    def draw(self):
        angle = self.get_angle()
        length = 1
        dx = length * math.cos(angle)
        dy = length * math.sin(angle)
        a = [int(self.x + dx), int(self.y - dy)]
        b = [int(self.x - dx), int(self.y + dy)]
        py.draw.line(self.screen, self.color, a, b, 15)


class Firework():
    def __init__(self, screen):
        self.screen = screen
        self.x = random.choice([random.randint(0, 370), random.randint(930, 1300)])
        self.y = 600
        self.velocity = random.uniform(10, 15)
        self.end_y = random.uniform(10, 300)
        self.ended = False

    def move(self):
        self.y -= self.velocity
        if self.y <= self.end_y:
            self.ended = True

    def draw(self):
        a = [self.x, int(self.y + 15)]
        b = [self.x, int(self.y - 20)]
        py.draw.line(self.screen, (128, 128, 128), a, b, 4)


fireworks = [Firework(screen)]
streaks = []


def game(screen):
    global streaks

    if random.uniform(0, 1) <= 1 / 60:
        fireworks.append(Firework(screen))
    for firework in fireworks:
        firework.move()
        firework.draw()
        if firework.ended:
            streaks += [Streak(firework.x, firework.y, screen) for i in range(random.randint(20, 40))]
            fireworks.remove(firework)
    for streak in streaks:
        streak.move()
        streak.draw()
        if streak.ended:
            streaks.remove(streak)


def game_Loop_Wordle(screen, letters, mystery_number, counter, points, platformer, level):
    py.mixer.music.load('images/Menu_page/Komiku_-_67_-_The_Moment_of_Truth.mp3')
    py.mixer.music.set_volume(0.2)
    py.mixer.music.play(-1)
    x_change = 0
    i = -1
    shake_count = 0
    message_count = 1
    check = []
    coord = []
    entered = []
    word = ""
    score = 0
    rect_pressed = False
    outside = False
    on = True
    pressed = False
    incorrect = False
    game_started = False
    added_button = 0
    button_lis = []
    working = True
    timer_event = py.USEREVENT
    py.time.set_timer(timer_event, 1000)
    run = True
    background(screen, 255, 255, 255, 590)
    place(screen, len(letters), on, coord, letters, list_images)
    mystery_and_submit_button(screen, mystery_number)
    start = ()
    clock = py.time.Clock()
    count_mystery_backspace = 0

    co = True
    img = py.image.load("images/hint-removebg-preview.png")
    img = py.transform.scale(img, (90, 90))
    rect4 = img.get_rect()
    rect4.x = 10
    rect4.y = 200

    while run:

        mouse = py.mouse.get_pos()
        for ev in py.event.get():
            if ev.type == QUIT or (ev.type == KEYDOWN and ev.key == K_ESCAPE):
                py.quit()
                exit()
            for i in button_lis:
                i.check_event(ev)
            if working == True:

                if ev.type == timer_event and game_started:
                    counter -= 1
                    text_draw(screen, counter)

                    if counter == 0:
                        working = False

                if ev.type == KEYDOWN:

                    if mystery_number != 0 and rect_pressed:
                        if ev.unicode.lower() in possible_characters:
                            let = ev.unicode
                            mystery(screen, ev.unicode.lower(), mystery_number, pressed, rect_pressed)
                            coord = []

                    if ev.key == K_SPACE:
                        incorrect = True
                    elif ev.key == K_RETURN and rect_pressed:
                        mystery_number -= 1
                        mystery_letters.append(let)

                        letters.append(let)
                        background(screen, 255, 255, 255, 590)
                        text_draw(screen, counter)
                        place(screen, len(letters), on, coord, letters, list_images)
                        mystery_and_submit_button(screen, mystery_number)
                        score_show(screen, working, score)
                        mystery(screen, "", mystery_number, pressed, rect_pressed)
                        count_mystery_backspace += 1
                    elif ev.key == K_BACKSPACE and count_mystery_backspace != len(mystery_letters) and len(
                            mystery_letters) != 0:
                        letters.remove(mystery_letters.pop())

                if ev.type == MOUSEBUTTONDOWN:
                    if rect4.collidepoint(ev.pos):
                        pass
                        get_hints(letters)
                    if 1150 < mouse[0] < 1200 and 550 < mouse[1] < 600 and start == ():

                        on = False
                        working = False

                    elif 20 < mouse[0] < 150 and 545 < mouse[1] < 610:

                        i += 1
                        if i % 2 == 0 and mystery_number != 0:
                            pressed = True
                            background(screen, 255, 255, 255, 590)
                            text_draw(screen, counter)
                            place(screen, len(letters), on, coord, letters, list_images)
                            mystery_and_submit_button(screen, mystery_number)
                            score_show(screen, working, score)

                        elif i % 2 != 0 and count_mystery_backspace == len(mystery_letters):
                            pressed = False
                            background(screen, 255, 255, 255, 590)
                            text_draw(screen, counter)
                            place(screen, len(letters), on, coord, letters, list_images)
                            mystery_and_submit_button(screen, mystery_number)
                            score_show(screen, working, score)

                    if 580 < mouse[0] < 720 and 270 < mouse[1] < 410 and pressed:
                        rect_pressed = True

                    else:
                        if rect_pressed:
                            rect_pressed = False
                            pressed = False
                            i += 1
                            background(screen, 255, 255, 255, 590)
                            text_draw(screen, counter)
                            place(screen, len(letters), on, coord, letters, list_images)
                            mystery_and_submit_button(screen, mystery_number)
                            score_show(screen, working, score)

                    mystery(screen, "", mystery_number, pressed, rect_pressed)

                    if on == True and 300 < mouse[0] < 1000 and 125 < mouse[
                        1] < 575 and not pressed and clock.tick() > 100:
                        game_started = True
                        start = near(coord, mouse, co)
                        outside = False
                        if start not in entered:

                            word += letters[coord.index(start)]
                            entered.append(start)

                        else:
                            incorrect = True
                    if mouse[0] < 500:
                        outside = True

                if start != ():
                    background(screen, 255, 255, 255, 590)
                    place(screen, len(letters), on, coord, letters, list_images)
                    if 300 < mouse[0] < 1000 and 125 < mouse[1] < 575:
                        py.draw.line(screen, (34, 153, 153), (start[0] + 20, start[1] + 20),
                                     (mouse[0] + 20, mouse[1] + 20), width=5)
                    lines(screen, entered)
                    show(screen, word, x_change)
                    if len(word) == len(letters) and not main.WORDS.get(word, False):
                        incorrect = True
                        py.mixer.Sound.play(incorrect_word_sound)
                        py.mixer.music.stop()

                    if len(word) > 1 and main.WORDS.get(word, False) and word not in check:
                        py.mixer.Sound.play(collect_letter_sound)
                        py.mixer.music.stop()
                        check.append(word)
                        score += len(word)
                        start = ()
                        entered = []
                        background(screen, 235, 235, 35, 590)

                        text_draw(screen, counter)
                        mystery_and_submit_button(screen, mystery_number)
                        score_show(screen, working, score)
                        place(screen, len(letters), on, coord, letters, list_images)
                        show(screen, word, x_change)
                        if word in vi:
                            vi.remove(word)
                        word = ""
                if incorrect == True:
                    start = ()
                    entered = []

                    shake(screen, shake_count, working, letters, incorrect, on, coord, word, score, list_images,
                          counter,
                          mystery_number)

                    incorrect = False
                    word = ""

                progress_bar(screen, score, 20, points)
                text_draw(screen, counter)
                if outside and start == ():
                    mystery_and_submit_button(screen, mystery_number)
                screen.blit(img, rect4)
                score_show(screen, working, score)

        if working == False:
            mixer.music.fadeout(1)
            background_celeb(screen, 255, 255, 255, 590)
            stars(screen)
            update_stars(score, points)
            score_show(screen, working, score)

            from menu import menu
            if added_button == 5:
                if count > 0:
                    var = json_storer.var

                    var["users"][var["current_user"][0]][1].append(
                        [level.str, count, score, current_time.strftime("%m/%d/%Y")])
                    with open('json_storer.py', 'w') as wvar:
                        wvar.write("var=" + str(var))
                retry_img = py.transform.scale(py.image.load(decode_file(other_small_images.retry)).convert_alpha(),
                                               (50, 50))
                button_menu = ui_tools.Button(
                    (ss.SCREEN_WIDTH / 2 - 100 - ss.SCREEN_WIDTH / 8, 520, ss.SCREEN_WIDTH / 8, 50),
                    (59, 83, 121), lambda: menu(screen), text="Menu", hover_color=(35, 53, 78),
                    clicked_color=(15, 20, 35),
                    border_radius=10, border_color=(35, 53, 78))
                retry_button = ui_tools.Button(
                    (ss.SCREEN_WIDTH / 2 - ss.SCREEN_WIDTH / 16, 520, ss.SCREEN_WIDTH / 8, 50),
                    (59, 83, 121), lambda: platformer(screen, menu, level), image=retry_img,
                    hover_color=(35, 53, 78),
                    clicked_color=(15, 20, 35),
                    border_radius=10, border_color=(35, 53, 78))
                state = False if count > 0 else True
                alpha = 255 if count > 0 else 30
                next_level_button = ui_tools.Button(
                    (ss.SCREEN_WIDTH / 2 + 100, 520, ss.SCREEN_WIDTH / 8, 50),
                    (59, 83, 121), next_level, text="Next Level", hover_color=(35, 53, 78),
                    clicked_color=(15, 20, 35),
                    border_radius=10, border_color=(35, 53, 78), platformer=platformer, state_disabled=state,
                    alpha=alpha)
                button_lis.append(button_menu)
                button_lis.append(retry_button)
                button_lis.append(next_level_button)
                added_button += 1
            elif added_button < 10:
                added_button += 1
            if message_count != 0:
                x = message(score, points)
                message_count -= 1

            celebration(screen, score, x, points)
            game(screen)
            game(screen)
        for i in button_lis:
            i.update(screen)
        py.display.update()


if __name__ == "__main__":
    from platformer_game import platformer_game
    from Level import level_list

    game_Loop_Wordle(screen, ["a", "b", "c", "d"], 4, 160, 30, platformer_game, level_list[2])
