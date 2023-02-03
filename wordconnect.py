import random
import pygame as py
from pygame.locals import *
import math
from pygame import mixer
import main
from letter import Letter
from helpful_functions import blit_text
import selection

py.init()
mixer.init()
# Removes letters that are 2 letters long
copy = main.WORDS.copy().keys()
for i in copy:
    if len(i) <= 2:
        main.WORDS[i] = False

screen = py.display.set_mode((1200, 600))
screen.fill((255, 255, 255))
image_list = ["hellop/zero_stars.png", "hellop/single_star.png", "hellop/double _star.png", "hellop/triple_star.png"]

single_star = ["you were close, try again", "better luck next time", " you can do better than one star"]
double_star = ["good job, now try to get three stars", "you can do better than two stars", "you were close to getting three stars"]
triple_star = ["Great job! You are a real Future Business Leader of America!!", "You are a G.O.A.T"]

count = 0
clock_star = py.time.Clock()
x_change = 0
message_show = 1
list_images = Letter.letter_dic

possible_characters = list(list_images.keys())


def background(x, y, z, c):
    bg_image = py.image.load("hellop/flat-design-copy-space-winter-background_52683-48883.jpeg")
    bg_image = py.transform.scale(bg_image, (1200, 600))
    table = py.Surface((540, c))
    table.set_alpha(128)
    table.fill((x, y, z))
    screen.blit(bg_image, (0, 0))
    screen.blit(table, (340, 50))


def place(n, on, coord, letters, list_images):
    if on == True:
        a = 0
        adding = (2 * 3.14) / n
        for i in range(0, n):
            im = py.image.load(list_images[letters[i]])
            im = py.transform.scale(im, (40,40))
            screen.blit(im, ((600 + 170 * math.cos(a), 315 + 170 * math.sin(a))))
            if len(coord) < len(letters):
                coord.append((600 + 170* math.cos(a), 315 + 170 * math.sin(a)))
            a += adding


def update(incorect, shake_count):
    global x_change
    if shake_count % 2 == 0:
        x_change = 5
    else:
        x_change = -5


def lines(entered):
    if entered != []:
        for cd in range(len(entered) - 1):
            py.draw.line(screen, (34, 153, 153), (entered[cd][0] + 20, entered[cd][1] + 20),
                         (entered[cd + 1][0] + 20, entered[cd + 1][1] + 20), width=3)


def near(x, y):
    z = []
    for i in range(len(x)):
        z.append((math.sqrt(pow(x[i][0] - y[0], 2)) + math.sqrt(pow(x[i][1] - y[1], 2))))

    return x[z.index(min(z))]


def show(word, x_change):
    adding = 5
    subtraction = 15
    font = py.font.Font(None, 50)
    w = ""
    for i in range(len(word)):
        w += word[i]
        text = font.render(w.upper(), True, (255, 255, 255), (0, 234, 56))
        screen.blit(text, (600 - (subtraction * len(w)) + (adding * len(w)) + x_change, 85))


def mystery(input, c, pressed, rect_pressed):
    if pressed == True:
        py.draw.circle(screen, (30, 212, 212), (620, 340), 70)
        font = py.font.Font(None, 80)
        if c == 0:
            py.draw.circle(screen, (212, 11, 14), (620, 340), 70)

        if rect_pressed == True and c != 0:
            py.draw.circle(screen, (95, 204, 0), (620, 340), 70, width=5)
            text_pressed = font.render(input.upper(), True, (255, 255, 255))
            text_effect = font.render(input.upper(), True, (0, 0, 0))
            if input != "":
                rect_image = text_pressed.get_rect()
                rect_image.center = (620, 340)
                rect_image_1 = text_effect.get_rect()
                rect_image_1.center = (618, 338)
                screen.blit(text_pressed, (rect_image))
                screen.blit(text_effect, (rect_image_1))


def mystery_and_submit_button(mystery_number):
    image = py.image.load("hellop/question.png")
    image = py.transform.scale(image, (50, 50))

    font = py.font.Font(None, 50)
    text = font.render(f":{mystery_number}", True, (0, 0, 0))
    py.draw.rect(screen, (22, 171, 171), (20, 445, 100, 60))
    screen.blit(text, (80, 463))
    screen.blit(image, (25, 450))

    image = py.image.load("hellop/arrow1.png")
    image_submit = py.transform.scale(image, (50, 50))
    screen.blit(image_submit, (1100, 450))


def score_show(x, score):
    font = py.font.Font(None, 50)
    if x == True:
        py.draw.rect(screen, (224, 177, 22), (980, 67, 170, 35))
        text = font.render(f"score: {score}", True, (0, 0, 0))
        screen.blit(text, (1000, 67))

    if x == False:

        text = font.render(f"score: {score}", True, (0, 0, 0))
        rect = text.get_rect()
        rect.center = (620, 400)
        screen.blit(text, rect)


def shake(shake_count,working, letters, incorrect, on, coord, word, score, list_images, counter, mystery_number):
    for i in range(4):
        background(201, 47, 4, 490)
        mystery_and_submit_button(mystery_number)

        text_draw(counter)

        place(len(letters), on, coord, letters, list_images)
        progress_bar(score, 20, 30)
        show(word, x_change)
        update(incorrect, shake_count)
        py.display.update()
        shake_count += 1


def text_draw(counter):
    py.draw.rect(screen, (blink(counter)), (20, 50, 50, 50))
    font = py.font.Font(None, 30)
    text = font.render(str(counter), True, (255, 255, 255))
    screen.blit(text, (45, 67))


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


def progress_bar(x, time1, points):
    x1 = round((x / points) * 500)
    py.draw.rect(screen, (21, 28, 28), (355, 560, 500, 30))
    im = py.image.load("hellop/600-6003350_star-game-icon-png-image-free-download-searchpng__1_-removebg-preview.png")
    im = py.transform.scale(im, (42, 35))

    if x1 < 500:
        py.draw.rect(screen, (204, 55, 75), (360, 560, 500, 25))
        py.draw.rect(screen, (255, 215, 0), (360, 560, x1, 25))
        py.draw.rect(screen, (80, 199, 100), (360, 560, x1, 25), width=5)
        py.draw.line(screen, (0, 0, 0), (360 + 0.2 * 500 + 20, 560), (360 + 0.2 * 500 + 20, 585), width=3)
        py.draw.line(screen, (0, 0, 0), (360 + 0.5 * 500 + 40, 560), (360 + 0.5 * 500 + 40, 585), width=3)
        py.draw.line(screen, (0, 0, 0), (860, 560), (860, 585), width=3)
        screen.blit(im, (round(360 + 0.2 * 500), 523))
        screen.blit(im, (round(360 + 0.5 * 500), 523))
        screen.blit(im, (round(360 + 0.5 * 500) + 42, 523))
        screen.blit(im, (round(365 + 500) - 65, 523))
        screen.blit(im, (round(365 + 500) - 25, 523))
        screen.blit(im, (round(365 + 500) + 15, 523))
    else:
        py.draw.rect(screen, (255, 215, 0), (360, 560, 500, 25))


def stars():
    global count
    if count <= len(image_list) - 1:
        im = py.image.load(image_list[count])
        im = py.transform.scale(im, (350, 350))
        screen.blit(im, (430,0))


def update_stars(score, points):
    global count
    if score >= points and count < 3:

        count += 1

    elif round(0.5 * points) <= score < points and count < 2:

        count += 1

    elif round(0.2 * points) <= score < round(0.5 * points) and count < 1:

        count += 1

    elif score == 0:
        count = 0


def celebration(score, x, points):
    if score >= points:
        blit_text(screen, x, (610, 300),
                  py.font.Font(None, 50), 800)
    elif points > score >= round(0.5 * points):
        blit_text(screen, x, (610, 300),
                  py.font.Font(None, 50), 800)
    elif round(0.5 * points) > score >= round(0.2 * points):
        blit_text(screen, x, (610, 300), py.font.Font(None, 50), 800)

    elif round(0.2*points) > score:
        blit_text(screen, x, (610, 300), py.font.Font(None, 50), 800)

def message(score, points):
    if score >= points:
        x = random.choice(triple_star)
    elif points > score >= round(0.5* points):
        x = random.choice(double_star)
    elif round(0.5 * points) > score >= round(0.2 * points):
        x = random.choice(single_star)
    elif round(points * 0.2) > score:
        x = "you loose, the world is over!!!! HA HA HA HA"

    return x

def transition():
    star_color = 100
    while star_color >= 0:
        screen.fill((star_color, star_color, star_color))
        star_color -= 1
        py.display.flip()

def game_Loop_Wordle(screen, letters, mystery_number):
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
    counter = 60
    working = True
    timer_event = py.USEREVENT
    py.time.set_timer(timer_event, 1000)
    y = 1
    run = True
    background(255, 255, 255, 490)
    place(len(letters), on, coord, letters, list_images)
    mystery_and_submit_button(mystery_number)
    start = ()
    clock = py.time.Clock()
    mixer.music.load("hellop/digital-love-127441.mp3")
    mixer.music.play()

    while run:
        mouse = py.mouse.get_pos()
        for ev in py.event.get():
            if ev.type == QUIT or (ev.type == KEYDOWN and ev.key == K_ESCAPE):
                run = False
                py.quit()
                exit()
            if working == True:
                if ev.type == timer_event and game_started:
                    counter -= 1
                    text_draw(counter)

                    if counter == 0:
                        working = False

                if ev.type == KEYDOWN:

                    if mystery_number != 0 and rect_pressed and mystery_number != 0:
                        if ev.unicode.lower() in possible_characters:
                            letters.append(ev.unicode.lower())
                            mystery(ev.unicode.lower(), mystery_number, pressed, rect_pressed)
                            coord = []
                            mystery_number -= 1

                    if ev.key == K_SPACE:
                        incorrect = True
                    elif ev.key == K_RETURN and rect_pressed:
                        i += 1
                        pressed = False
                        background(255, 255, 255, 520)
                        text_draw(counter)
                        place(len(letters), on, coord, letters, list_images)
                        mystery_and_submit_button(mystery_number)
                        score_show(working, score)

                if ev.type == MOUSEBUTTONDOWN:

                    if 1100 < mouse[0] < 1150 and 450 < mouse[1] < 500 and start == ():

                        on = False
                        working = False
                        transition()
                    elif 25 < mouse[0] < 75 and 450 < mouse[1] < 500:
                        i += 1
                        if i % 2 == 0:
                            pressed = True

                        else:
                            pressed = False
                            background(255, 255, 255, 520)
                            text_draw(counter)
                            place(len(letters), on, coord, letters, list_images)
                            mystery_and_submit_button(mystery_number)
                            score_show(working, score)

                    if 550 < mouse[0] < 690 and 270 < mouse[1] < 410 and pressed:
                        rect_pressed = True

                    else:
                        rect_pressed = False

                    mystery("", mystery_number, pressed, rect_pressed)

                    if on == True  and 300 < mouse[0] < 1000 and 125 < mouse[1] < 575 and not pressed and clock.tick() > 100:
                        game_started = True
                        start = near(coord, mouse)
                        outside = False
                        if start not in entered:

                            word += letters[coord.index(start)]
                            entered.append(start)

                        else:
                            print(word)
                            incorrect = True
                    if mouse[0] < 500:
                        outside = True

                if start != ():
                    background(255, 255, 255,490)
                    place(len(letters), on, coord, letters, list_images)
                    if 300 < mouse[0] < 1000 and 125 < mouse[1] < 575:
                        py.draw.line(screen, (34, 153, 153), (start[0] + 20, start[1] + 20),
                                     (mouse[0] + 20, mouse[1] + 20), width=5)
                    lines(entered)
                    show(word, x_change)
                    if len(word) == len(letters) and not main.WORDS.get(word, False):
                        incorrect = True

                    if len(word) > 1 and main.WORDS.get(word, False) and word not in check:
                        check.append(word)
                        score += len(word)
                        start = ()
                        entered = []
                        background(235, 235, 35, 490)

                        text_draw(counter)
                        mystery_and_submit_button(mystery_number)
                        score_show(working, score)
                        place(len(letters), on, coord, letters, list_images)
                        show(word, x_change)

                        word = ""
                if incorrect == True:
                    start = ()
                    entered = []

                    shake(shake_count, working, letters, incorrect, on, coord, word, score, list_images, counter,
                          mystery_number)

                    incorrect = False
                    word = ""

                progress_bar(score, 20, 30)
                text_draw(counter)
                if outside and start == ():
                    mystery_and_submit_button(mystery_number)
                score_show(working, score)



        if working == False:

            mixer.music.fadeout(1)
            background(255, 255, 255, 490)
            clock_star.tick(5)
            stars()
            update_stars(score, 30)
            score_show(working, score)

            if message_count != 0:
                x = message(score, 30)
                message_count -= 1
            celebration(score, x, 30)
        py.display.update()



if __name__ == "__main__":
    selection.game_loop_select_letters(3)

    game_Loop_Wordle(screen, selection.letter_selected, 3)


    py.quit()
