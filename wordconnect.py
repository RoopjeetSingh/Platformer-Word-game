from spellchecker import SpellChecker
import pygame as py
from pygame.locals import *
import math
import time
from letter import Letter

py.init()
screen = py.display.set_mode((1000, 500))
screen.fill((255, 255, 255))
letters = ["h", "b"]
d = SpellChecker()
input_rect = py.Rect(200, 200, 140, 32)
intro_rect = py.Rect(400, 218, 200, 50)

i = -1
working = True
starting = False
check = []
list_images = Letter.letter_dic
coord = []
entered = []
word = ""
mystery_letter = ""
mystery_number = 5
score = 0
rect_pressed = False
on = True
pressed = False
incorrect = False
intro_pressed = False


def background(x, y, z, c):
    bg_image = py.image.load("hellop/flat-design-copy-space-winter-background_52683-48883.jpeg")
    bg_image = py.transform.scale(bg_image, (1000, 500))
    table = py.Surface((420, c))
    table.set_alpha(128)
    table.fill((x, y, z))
    screen.blit(bg_image, (0, 0))
    screen.blit(table, (300, 25))


def place(n, on, coord):
    if on == True:
        a = 0
        adding = (2 * 3.14) / n
        for i in range(0, n):
            im = py.image.load(list_images[letters[i]])
            im = py.transform.scale(im, (35, 35))
            screen.blit(im, ((480 + 130 * math.cos(a), 300 + 130 * math.sin(a))))
            if len(coord) < len(letters):
                coord.append((480 + 130 * math.cos(a), 300 + 130 * math.sin(a)))
            a += adding


def lines():
    if entered != []:
        for cd in range(len(entered) - 1):
            py.draw.line(screen, (34, 153, 153), (entered[cd][0] + 20, entered[cd][1] + 20),
                         (entered[cd + 1][0] + 20, entered[cd + 1][1] + 20), width=3)


def near(x, y):
    z = []
    for i in range(len(x)):
        z.append((math.sqrt(pow(x[i][0] - y[0], 2)) + math.sqrt(pow(x[i][1] - y[1], 2))))

    return x[z.index(min(z))]


def show(word):
    adding = 5
    subtraction = 15
    font = py.font.Font(None, 50)
    w = ""
    for i in range(len(word)):
        w += word[i]
        text = font.render(w, True, (255, 255, 255), (0, 234, 56))

        screen.blit(text, (500 - (subtraction * len(w)) + (adding * len(w)), 90))


def mystery(input, c):
    if pressed == True:
        py.draw.rect(screen, (30, 212, 212), input_rect)
        font = py.font.Font(None, 32)
        if c == 0:
            py.draw.rect(screen, (212, 11, 14), input_rect)
        if rect_pressed == True and c != 0:
            py.draw.rect(screen, (95, 204, 0), input_rect)
            text_pressed = font.render(input, True, (255, 255, 255))
            if input != "":
                screen.blit(text_pressed, input_rect)


def mystery_and_submit_button(x):
    if x == True:
        image = py.image.load("hellop/question.png")
        image = py.transform.scale(image, (50, 50))
        screen.blit(image, (0, 0))
        image = py.image.load("hellop/arrow1.png")
        image_submit = py.transform.scale(image, (50, 50))
        screen.blit(image_submit, (850, 340))


def score_show(x):
    font = py.font.Font(None, 50)
    if x == True:
        text = font.render(f"score: {score}", True, (0, 0, 0))
        screen.blit(text, (800, 50))
    if x == False:
        text1 = font.render("game over", True, (0, 0, 0))
        text = font.render(f"score: {score}", True, (0, 0, 0))
        screen.blit(text1, (500, 100))
        screen.blit(text, (500, 250))


def intro():
    image_intro = py.image.load(
        "hellop/abstract-grunge-decorative-relief-navy-blue-stucco-wall-texture-wide-angle-rough-colored-background_1258-28311.jpg")
    image_intro = py.transform.scale(image_intro, (1000, 500))
    screen.blit(image_intro, (0, 0))
    py.draw.rect(screen, (93, 245, 22), intro_rect)


run = True
intro()

start = ()
clock = py.time.Clock()
while run:
    if working == True:

        mouse = py.mouse.get_pos()

        for ev in py.event.get():
            if ev.type == QUIT:
                py.quit()
            if ev.type == KEYDOWN:

                if mystery_number != 0 and ev.unicode not in letters and rect_pressed == True and mystery_number != 0:
                    if ev.unicode != '\r':
                        letters.append(ev.unicode)
                        mystery(ev.unicode, mystery_number)
                        coord = []
                        mystery_number -= 1

            if ev.type == MOUSEBUTTONDOWN:

                if intro_rect.collidepoint(mouse):
                    intro_pressed = True

                if 850 < mouse[0] < 950 and 340 < mouse[1] < 390 and intro_pressed:

                    on = False
                    working = False

                elif 0 < mouse[0] < 50 and 0 < mouse[1] < 50 and intro_pressed:
                    i += 1
                    if i % 2 == 0:
                        pressed = True
                        print(pressed)
                    else:
                        pressed = False
                        print(pressed)

                if input_rect.collidepoint(mouse) and pressed == True and intro_pressed:
                    rect_pressed = True
                else:
                    rect_pressed = False

                mystery("", mystery_number)

                if on == True and 300 < mouse[0] < 700 and 25 < mouse[
                    1] < 475 and rect_pressed != True and starting == True:

                    start = near(coord, mouse)
                    if start not in entered:

                        word += letters[coord.index(start)]
                        entered.append(start)
                    else:
                        word = ""
                        entered = []
                        start = ()

                if pressed == False and intro_pressed:
                    starting = True
                    background(255, 255, 255, 450)
                    place(len(letters), on, coord)
                    mystery_and_submit_button(intro_pressed)
                    score_show(intro_pressed)

                    if ev.type == KEYDOWN:
                        if mystery_number != 0 and ev.unicode not in letters and rect_pressed == True:

                            if ev.unicode != '\r':
                                letters.append(ev.unicode)
                                mystery(ev.unicode, mystery_number)

        if start != ():
            background(255, 255, 255, 450)
            mystery_and_submit_button(intro_pressed)
            place(len(letters), on, coord)

            score_show(intro_pressed)
            py.draw.line(screen, (34, 153, 153), (start[0] + 20, start[1] + 20), (mouse[0] + 20, mouse[1] + 20),
                         width=5)
            lines()
            show(word)
            if len(word) == len(letters) and (word == d.correction(word) or word in check):
                incorrect = True
                start = ()
                entered = []
                background(201, 47, 4, 450)
                mystery_and_submit_button(intro_pressed)
                score_show(intro_pressed)
                place(len(letters), on, coord)
                show(word)
                print(word)
                word = ""

            if len(word) > 1 and word not in check and word == d.correction(word):
                check.append(word)
                score += len(word)
                start = ()
                entered = []
                background(235, 235, 35, 450)
                mystery_and_submit_button(intro_pressed)
                score_show(intro_pressed)
                place(len(letters), on, coord)
                show(word)
                print(word)
                word = ""

    if working == False:
        background(255, 255, 255, 450)
        score_show(working)
    py.display.update()
