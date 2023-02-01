import random
import pygame as py
from pygame.locals import *
import math
from pygame import mixer
import main
from letter import Letter


py.init()
mixer.init()

screen = py.display.set_mode((1000, 500))
screen.fill((255, 255, 255))
image_list = ["hellop/zero_stars.png", "hellop/single_star.png", "hellop/double _star.png", "hellop/triple_star.png"]

count = 0
clock_star = py.time.Clock()
x_change = 0
message_show = 1
list_images = Letter.letter_dic

possible_characters = list(list_images.keys())

def music():
    pass
def background(x, y, z, c):
    bg_image = py.image.load("hellop/flat-design-copy-space-winter-background_52683-48883.jpeg")
    bg_image = py.transform.scale(bg_image, (1000, 500))
    table = py.Surface((420, c))
    table.set_alpha(128)
    table.fill((x, y, z))
    screen.blit(bg_image, (0, 0))
    screen.blit(table, (300, 25))


def place(n, on, coord, letters, list_images):
    if on == True:
        a = 0
        adding = (2 * 3.14) / n
        for i in range(0, n):
            im = py.image.load(list_images[letters[i]])
            im = py.transform.scale(im, (35, 35))
            screen.blit(im, ((500 + 130 * math.cos(a), 250 + 130 * math.sin(a))))
            if len(coord) < len(letters):
                coord.append((500 + 130 * math.cos(a), 250 + 130 * math.sin(a)))
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
        screen.blit(text, (515 - (subtraction * len(w)) + (adding * len(w)) + x_change, 60))


def mystery(input, c, pressed,rect_pressed):
    if pressed == True:
        py.draw.circle(screen, (30, 212, 212), (520, 265), 50)
        font = py.font.Font(None, 50)
        if c == 0:
            py.draw.circle(screen, (212, 11, 14), (520, 265), 50)

        if rect_pressed == True and c != 0:
            py.draw.circle(screen, (95, 204, 0), (520, 265), 50, width = 5)
            text_pressed = font.render(input, True, (255, 255, 255))
            text_effect = font.render(input, True, (0,0,0))
            if input != "":
                screen.blit(text_pressed, (510, 250))
                screen.blit(text_effect, (507, 247))

def mystery_and_submit_button(mystery_number):

    image = py.image.load("hellop/question.png")
    image = py.transform.scale(image, (50, 50))

    font = py.font.Font(None, 50)
    text = font.render(f":{mystery_number}", True, (0,0,0))
    py.draw.rect(screen, (22, 171, 171), (20, 345, 100,60))
    screen.blit(text, (80, 363))
    screen.blit(image, (25, 350))

    image = py.image.load("hellop/arrow1.png")
    image_submit = py.transform.scale(image, (50, 50))
    screen.blit(image_submit, (900, 350))


def score_show(x, score):
    font = py.font.Font(None, 50)
    if x == True:
        py.draw.rect(screen, (224, 177, 22), (780, 60, 170, 35))
        text = font.render(f"score: {score}", True, (0, 0, 0))
        screen.blit(text, (800, 60))

    if x == False:
        text = font.render(f"score: {score}", True, (0, 0, 0))
        screen.blit(text, (445, 350))



def shake(shake_count, working, letters, incorrect, on, coord, word, score, list_images, counter, mystery_number):
    for i in range(4):
        background(201, 47, 4, 420)
        mystery_and_submit_button(mystery_number)

        text_draw(counter)

        place(len(letters), on, coord, letters, list_images)
        progress_bar(score, 20, 30)
        show(word, x_change)
        update(incorrect, shake_count)
        py.display.update()
        shake_count += 1

def text_draw(counter):
    py.draw.rect(screen, (blink(counter)), (20, 50,50,50))
    font = py.font.Font(None, 30)
    text = font.render(str(counter), True, (255,255,255))
    screen.blit(text, (35, 67))



def blink(counter):
    if counter % 2 == 0:
        if counter >= 40:
            return (103, 240, 24)
        elif 20 <= counter < 40:
            return (240, 182, 24)
        elif counter < 20:
            return (240, 64, 24)
    else:
        return (0,0,0)

def progress_bar(x, time1,points):
    x1 = round((x /points) * 500)
    py.draw.rect(screen, (21, 28, 28), (255, 460, 500, 30))
    im = py.image.load("hellop/600-6003350_star-game-icon-png-image-free-download-searchpng__1_-removebg-preview.png")
    im = py.transform.scale(im, (42, 35))

    if x1 < 500:
        py.draw.rect(screen, (204, 55, 75), (260,455, 500, 25))
        py.draw.rect(screen, (255,215,0), (260, 455, x1, 25))
        py.draw.rect(screen, (80, 199, 100),(260, 455,x1, 25), width = 5)
        py.draw.line(screen, (0, 0, 0), (260 + 0.2 * 500 + 20, 455), (260 + 0.2 * 500+ 20, 483), width =3)
        py.draw.line(screen, (0, 0, 0), (260 + 0.5*500 + 40, 455), (260 + 0.5*500 + 40, 483), width = 3)
        py.draw.line(screen, (0, 0, 0), (760, 455), (760, 479), width = 3)
        screen.blit(im, (round(260 + 0.2*500), 423))
        screen.blit(im, (round(260 + 0.5*500), 423))
        screen.blit(im, (round(260 + 0.5* 500) + 42, 423))
        screen.blit(im,(round(260+ 500) -65, 423))
        screen.blit(im, (round(260 + 500) - 25, 423))
        screen.blit(im, (round(260 + 500) + 15, 423))
    else:
        py.draw.rect(screen, (255,215,0), (260, 460, 500, 25))

def stars():
    global count
    if count <= len(image_list) - 1:
        im = py.image.load(image_list[count])
        im = py.transform.scale(im, (300,300))
        screen.blit(im, (360,0))

def update_stars(score, points):
    global count
    if score >= points and count < 3:

        count += 1

    elif round(0.5*points) <= score < points and count < 2:

        count += 1

    elif round(0.2 * points)<= score < round(0.5 * points) and count < 1:

        count += 1

    elif score == 0:
        count = 0

def celebration(message):
    font1 = py.font.Font(None, 50)
    text = font1.render(message, True, (0,0,0))
    rect = text.get_rect()
    rect.center = 500, 250
    screen.blit(text, rect)

def game_Loop_Wordle(screen, letters, mystery_number):

    x_change = 0
    i = -1
    shake_count = 0
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
    background(255, 255, 255, 420)
    place(len(letters), on, coord, letters, list_images)
    mystery_and_submit_button(mystery_number)
    music()
    start = ()
    clock = py.time.Clock()
    mixer.music.load("hellop/digital-love-127441.mp3")
    mixer.music.play()
    messages = ["great job", "good job", "Bravo!!!!", "you got it", "you win"]
    x = random.choice(messages)
    while run:
            mouse = py.mouse.get_pos()
            for ev in py.event.get():
                if ev.type == QUIT:
                    run = False
                if working == True:
                    if ev.type == timer_event and game_started:
                        counter -= 1
                        text_draw(counter)

                        if counter == 0:
                            working = False

                    if ev.type == KEYDOWN:

                        if mystery_number != 0 and ev.unicode not in letters and rect_pressed and mystery_number != 0:
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
                            background(255, 255, 255, 420)
                            text_draw(counter)
                            place(len(letters), on, coord, letters, list_images)
                            mystery_and_submit_button(mystery_number)
                            score_show(working, score)

                    if ev.type == MOUSEBUTTONDOWN:

                        if 850 < mouse[0] < 950 and 340 < mouse[1] < 390 and start == ():

                            on = False
                            working = False

                        elif 25 < mouse[0] < 75 and 350< mouse[1] < 400:
                            i += 1
                            if i % 2 == 0:
                                pressed = True

                            else:
                                pressed = False
                                background(255, 255, 255, 420)
                                text_draw(counter)
                                place(len(letters), on, coord, letters, list_images)
                                mystery_and_submit_button(mystery_number)
                                score_show(working, score)


                        if 470< mouse[0]< 570 and 210< mouse[1]< 315 and pressed:
                            rect_pressed = True

                        else:
                            rect_pressed = False

                        mystery("", mystery_number, pressed,rect_pressed)

                        if on == True and 300 < mouse[0] < 700 and 25 < mouse[1] < 475 and not pressed  and clock.tick() > 100:
                            game_started = True
                            start = near(coord, mouse)
                            outside = False
                            if start not in entered:

                                word += letters[coord.index(start)]
                                entered.append(start)

                            else:
                                print(word)
                                incorrect = True
                        if mouse[0] < 300:
                            outside = True

                    if start != ():
                        background(255, 255, 255, 420)
                        place(len(letters), on, coord, letters, list_images)
                        if 280 < mouse[0] < 750 and 25 < mouse[1] < 475:
                            py.draw.line(screen, (34, 153, 153), (start[0] + 20, start[1] + 20), (mouse[0] + 20, mouse[1] + 20), width=5)
                        lines(entered)
                        show(word, x_change)
                        if len(word) == len(letters) and not main.WORDS.get(word, False):
                            incorrect = True

                        if len(word) > 1 and main.WORDS.get(word, False) and word not in check:
                            check.append(word)
                            score += len(word)
                            start = ()
                            entered = []
                            background(235, 235, 35, 420)

                            text_draw(counter)
                            mystery_and_submit_button(mystery_number)
                            score_show(working, score)
                            place(len(letters), on, coord, letters, list_images)
                            show(word, x_change)

                            word = ""
                    if incorrect == True:
                        start = ()
                        entered = []

                        shake(shake_count, working, letters, incorrect, on, coord, word, score, list_images, counter, mystery_number)

                        incorrect = False
                        word = ""

                    progress_bar(score, 20, 30)
                    text_draw(counter)
                    if outside and start == ():
                        mystery_and_submit_button(mystery_number)
                    score_show(working, score)


            if working == False:
                mixer.music.fadeout(1)
                background(255, 255, 255, 450)
                clock_star.tick(5)
                stars()
                update_stars(score, 30)
                score_show(working, score)
                celebration(x)

            py.display.update()

game_Loop_Wordle(screen, ["a", "b", "c", "d", "e", "g", "n", "m", "y"],3)
py.quit()
