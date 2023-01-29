from spellchecker import SpellChecker
import pygame as py
from pygame.locals import *
import math
from pygame import mixer
from letter import Letter

spell = SpellChecker()
py.init()
mixer.init()

screen = py.display.set_mode((1000, 500))
screen.fill((255, 255, 255))
x_change = 0


# def music(x):
#     mixer.music.load("hellop/digital-love-127441.mp3")
#
#     if x == 0:
#         mixer.music.play()
#     elif x == 1:
#         mixer.music.stop()

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

    #font = py.font.Font(None, 50)
    #text = font.render(f":{mystery_number}", True, (0,0,0))
    #screen.blit(text, (65, 15))

    screen.blit(image, (25, 350))

    image = py.image.load("hellop/arrow1.png")
    image_submit = py.transform.scale(image, (50, 50))
    screen.blit(image_submit, (900, 350))


#def score_show(x, score):
 #   font = py.font.Font(None, 50)
  #  if x == True:
   #     py.draw.rect(screen, (224, 177, 22), (780, 60, 170, 35))
    #    text = font.render(f"score: {score}", True, (0, 0, 0))
     #   screen.blit(text, (800, 60))

    #if x == False:
     #   text1 = font.render("game over", True, (0, 0, 0))
      #  text = font.render(f"score: {score}", True, (0, 0, 0))
       # screen.blit(text1, (500, 100))
        #screen.blit(text, (500, 250))



def shake(shake_count, working, letters, incorrect, on, coord, word, score, list_images, counter, mystery_number):
    for i in range(4):
        background(201, 47, 4, 420)
        mystery_and_submit_button(mystery_number)

        text_draw(counter)
        #score_show(working, score)
        place(len(letters), on, coord, letters, list_images)
        progress_bar(score, 20)
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

def progress_bar(x, time1):
    x1 = round(((x + time1) / 45) * 500)
    py.draw.rect(screen, (0,0,0), (255, 460, 500, 30), width = 5)
    if x1 < 500:

        py.draw.rect(screen, (204, 55, 75), (260,460, 500, 25))
        py.draw.rect(screen, (255,215,0), (260, 460, x1, 25))
        py.draw.rect(screen, (80, 199, 100),(260, 460,x1, 25), width = 5)
    else:
        py.draw.rect(screen, (255,215,0), (260, 460, 500, 25))

def game_Loop_Wordle(screen, letters, mystery_number):

    x_change = 0
    i = -1
    shake_count = 0

    check = []

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
    game_started = False
    counter = 60
    working = True
    timer_event = py.USEREVENT
    py.time.set_timer(timer_event, 1000)

    run = True
    background(255, 255, 255, 420)
    place(len(letters), on, coord, letters, list_images)

    # music(0)
    start = ()
    clock = py.time.Clock()

    clock1 = py.time.Clock()
    while run:

        if working == True:

            mouse = py.mouse.get_pos()
            clock1.tick()
            for ev in py.event.get():
                if ev.type == QUIT:

                    py.quit()
                    run = False
                if ev.type == timer_event and game_started:
                    counter -= 1
                    text_draw(counter)

                    if counter == 0:
                        working = False

                if ev.type == KEYDOWN:

                    if mystery_number != 0 and ev.unicode not in letters and rect_pressed and mystery_number != 0:
                        if ev.unicode not in cannot_be_entered:
                            letters.append(ev.unicode.lower())
                            mystery(ev.unicode.lower(), mystery_number, pressed, rect_pressed)
                            coord = []
                            mystery_number -= 1


                if ev.type == MOUSEBUTTONDOWN:
                    print(mouse)
                    if 850 < mouse[0] < 950 and 340 < mouse[1] < 390:

                        on = False
                        working = False

                    elif 20 < mouse[0] < 70 and 300< mouse[1] < 350:
                        i += 1
                        if i % 2 == 0:
                            pressed = True

                            print(pressed)
                        else:
                            pressed = False

                            background(255, 255, 255, 420)
                            text_draw(counter)
                            place(len(letters), on, coord, letters, list_images)
                            mystery_and_submit_button(mystery_number)
                            #score_show(working, score)
                            print(1)

                    if 470< mouse[0]< 570 and 210< mouse[1]< 315 and pressed:
                        rect_pressed = True
                        print(123)
                    else:
                        rect_pressed = False

                    mystery("", mystery_number, pressed,rect_pressed)

                    if on == True and 300 < mouse[0] < 700 and 25 < mouse[1] < 475 and not pressed:
                        game_started = True
                        start = near(coord, mouse)
                        if start not in entered  and clock.tick() > 450:

                            word += letters[coord.index(start)]
                            entered.append(start)

                        else:
                            print(word)
                            incorrect = True



                if start != ():
                    background(255, 255, 255, 420)

                    #mystery_and_submit_button()
                    place(len(letters), on, coord, letters, list_images)
                    #score_show(working, score)
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
                        background(235, 235, 35, 420)

                        text_draw(counter)
                        mystery_and_submit_button(mystery_number)
                        #score_show(working, score)
                        place(len(letters), on, coord, letters, list_images)
                        show(word, x_change)

                        word = ""
                if incorrect == True:
                    start = ()
                    entered = []

                    shake(shake_count, working, letters, incorrect, on, coord, word, score, list_images, counter, mystery_number)

                    incorrect = False
                    word = ""

            progress_bar(score, 20)
            text_draw(counter)

            #score_show(working, score)
            mystery_and_submit_button(mystery_number)

        if working == False:
            # music(1)
            background(255, 255, 255, 450)
            #score_show(working, score)
        py.display.update()

game_Loop_Wordle(screen, ["a", "b", "c", "d", "e"],3)
