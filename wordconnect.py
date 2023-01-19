from spellchecker import SpellChecker
import pygame as py
from pygame.locals import *
import math
from letter import Letter

spell = SpellChecker()

py.init()
screen = py.display.set_mode((1000, 500))
screen.fill((255, 255, 255))
x_change = 0


def background(x, y, z, c):
    bg_image = py.image.load("hellop/flat-design-copy-space-winter-background_52683-48883.jpeg")
    bg_image = py.transform.scale(bg_image, (1000, 500))
    table = py.Surface((420, c))
    table.set_alpha(128)
    table.fill((x, y, z))
    screen.blit(bg_image, (0, 0))
    screen.blit(table, (300, 25))


def block():
    table = py.Surface((420, 200))
    table.set_alpha(128)
    table.fill((255, 255, 255))
    screen.blit(table, (300, 25))


def place(n, on, coord, letters, list_images):
    if on == True:
        a = 0
        adding = (2 * 3.14) / n
        for i in range(0, n):
            im = py.image.load(list_images[letters[i]])
            im = py.transform.scale(im, (35, 35))
            screen.blit(im, ((500 + 130 * math.cos(a), 300 + 130 * math.sin(a))))
            if len(coord) < len(letters):
                coord.append((500 + 130 * math.cos(a), 300 + 130 * math.sin(a)))
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
        text = font.render(w, True, (255, 255, 255), (0, 234, 56))
        screen.blit(text, (500 - (subtraction * len(w)) + (adding * len(w)) + x_change, 90))


def mystery(input, c, pressed, input_rect, rect_pressed):
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


def mystery_and_submit_button():
    image = py.image.load("hellop/question.png")
    image = py.transform.scale(image, (50, 50))
    screen.blit(image, (0, 0))
    image = py.image.load("hellop/arrow1.png")
    image_submit = py.transform.scale(image, (50, 50))
    screen.blit(image_submit, (850, 340))


def score_show(x, score):
    font = py.font.Font(None, 50)
    if x == True:
        text = font.render(f"score: {score}", True, (0, 0, 0))
        screen.blit(text, (800, 50))
    if x == False:
        text1 = font.render("game over", True, (0, 0, 0))
        text = font.render(f"score: {score}", True, (0, 0, 0))
        screen.blit(text1, (500, 100))
        screen.blit(text, (500, 250))


def shake(shake_count, working, letters, incorrect, on, coord, word, score, list_images):
    for i in range(6):
        background(201, 47, 4, 450)
        mystery_and_submit_button()
        py.draw.rect(screen, (0, 0, 0), (100, 200, 50, 50))

        score_show(working, score)
        place(len(letters), on, coord, letters, list_images)
        show(word, x_change)
        update(incorrect, shake_count)
        py.display.update()
        shake_count += 1


def check_word(word, check):
    if word == spell.correction(word):
        check.append(word)
        return True
    else:
        return False


def text_draw(counter):
    font = py.font.Font(None, 30)
    py.draw.rect(screen, (0, 0, 0), (100, 200, 50, 50))
    text = font.render(str(counter), True, (255, 255, 255))
    screen.blit(text, (125, 225))


def game(screen, letters, mystery_number):
    input_rect = py.Rect(400, 218, 200, 50)
    x_change = 0
    i = -1
    shake_count = 0
    starting = False

    check = []
    mouse_pressed = False
    cannot_be_entered = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", ",", "/", "[", "]"]
    list_images = Letter.letter_dic
    coord = []
    entered = []
    word = ""

    score = 0
    rect_pressed = False
    on = True
    pressed = False
    incorrect = False

    counter = 60
    working = True
    timer_event = py.USEREVENT + 1
    py.time.set_timer(timer_event, 1000)

    run = True
    background(255, 255, 255, 450)
    place(len(letters), on, coord, letters, list_images)

    start = ()
    clock = py.time.Clock()

    while run:

        if working == True:

            mouse = py.mouse.get_pos()

            for ev in py.event.get():
                if ev.type == QUIT:
                    py.quit()
                if ev.type == timer_event and mouse_pressed == True:
                    counter -= 1
                    text_draw(counter)
                    if counter == 0:
                        working = False

                if ev.type == KEYDOWN:

                    if mystery_number != 0 and ev.unicode not in letters and rect_pressed == True and mystery_number != 0:
                        if ev.unicode not in cannot_be_entered:
                            letters.append(ev.unicode)
                            mystery(ev.unicode, mystery_number, pressed, input_rect, rect_pressed)
                            coord = []
                            mystery_number -= 1

                if ev.type == MOUSEBUTTONDOWN:

                    mouse_pressed = True
                    if 850 < mouse[0] < 950 and 340 < mouse[1] < 390:

                        on = False
                        working = False

                    elif 0 < mouse[0] < 50 and 0 < mouse[1] < 50:
                        i += 1
                        if i % 2 == 0:
                            pressed = True
                            print(pressed)
                        else:
                            pressed = False
                            print(pressed)

                    if input_rect.collidepoint(mouse) and pressed == True:
                        rect_pressed = True
                    else:
                        rect_pressed = False

                    mystery("", mystery_number, pressed, input_rect, rect_pressed)

                    if on == True and 300 < mouse[0] < 700 and 25 < mouse[
                        1] < 475 and rect_pressed != True and starting == True:

                        start = near(coord, mouse)
                        if start not in entered and clock.tick() > 250:

                            word += letters[coord.index(start)]
                            entered.append(start)
                        else:
                            print(word)
                            incorrect = True

                    if pressed == False:
                        starting = True
                        background(255, 255, 255, 450)
                        text_draw(counter)
                        place(len(letters), on, coord, letters, list_images)
                        mystery_and_submit_button()
                        score_show(working, score)

                        if ev.type == KEYDOWN:
                            if mystery_number != 0 and ev.unicode not in letters and rect_pressed == True:

                                if ev.unicode != '\r':
                                    letters.append(ev.unicode)
                                    mystery(ev.unicode, mystery_number, pressed, input_rect, rect_pressed)

            if start != ():
                background(255, 255, 255, 450)

                mystery_and_submit_button()
                place(len(letters), on, coord, letters, list_images)

                score_show(working, score)
                py.draw.line(screen, (34, 153, 153), (start[0] + 20, start[1] + 20), (mouse[0] + 20, mouse[1] + 20),
                             width=5)
                lines(entered)
                show(word, x_change)
                if len(word) == len(letters) and ((check_word(word, check) == False) or word in check):
                    incorrect = True

                if len(word) > 1 and word not in check and check_word(word, check) == True:
                    check.append(word)
                    score += len(word)
                    start = ()
                    entered = []
                    background(235, 235, 35, 450)
                    py.draw.rect(screen, (0, 0, 0), (100, 200, 50, 50))
                    text_draw(counter)
                    mystery_and_submit_button()
                    score_show(working, score)
                    place(len(letters), on, coord, letters, list_images)
                    show(word, x_change)

                    word = ""
            if incorrect == True:
                start = ()
                entered = []

                shake(shake_count, working, letters, incorrect, on, coord, word, score, list_images)

                incorrect = False
                word = ""

            text_draw(counter)

        if working == False:
            background(255, 255, 255, 450)
            score_show(working, score)
        py.display.update()


game(screen, ["h", "t", "u", "a", "b"], 2)
