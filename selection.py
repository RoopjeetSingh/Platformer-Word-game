import pygame as py
from pygame.locals import *
import math

screen = py.display.set_mode((1000, 500))
x = 0
y = 300
desired_height = 500
starting_height = 0
list_images = {'a': "hellop/Platformer-word-game-master/images/Letters/1.png",
               'b': "hellop/Platformer-word-game-master/images/Letters/9.png",
               'c': "hellop/Platformer-word-game-master/images/Letters/19.png",
               'd': "hellop/Platformer-word-game-master/images/Letters/15.png",
               'e': "hellop/Platformer-word-game-master/images/Letters/26.png",
               'f': "hellop/Platformer-word-game-master/images/Letters/23.png",
               'g': "hellop/Platformer-word-game-master/images/Letters/18.png",
               'h': "hellop/Platformer-word-game-master/images/Letters/2.png",
               'i': "hellop/Platformer-word-game-master/images/Letters/7.png",
               'j': "hellop/Platformer-word-game-master/images/Letters/12.png",
               'k': "hellop/Platformer-word-game-master/images/Letters/3.png",
               'l': "hellop/Platformer-word-game-master/images/Letters/16.png",
               'm': "hellop/Platformer-word-game-master/images/Letters/28.png",
               'n': "hellop/Platformer-word-game-master/images/Letters/25.png",
               'o': "hellop/Platformer-word-game-master/images/Letters/22.png",
               'p': "hellop/Platformer-word-game-master/images/Letters/0.png",
               'q': "hellop/Platformer-word-game-master/images/Letters/6.png",
               'r': "hellop/Platformer-word-game-master/images/Letters/17.png",
               's': "hellop/Platformer-word-game-master/images/Letters/20.png",
               't': "hellop/Platformer-word-game-master/images/Letters/13.png",
               'u': "hellop/Platformer-word-game-master/images/Letters/21.png",
               'v': "hellop/Platformer-word-game-master/images/Letters/24.png",
               'w': "hellop/Platformer-word-game-master/images/Letters/11.png",
               'x': "hellop/Platformer-word-game-master/images/Letters/10.png",
               'y': "hellop/Platformer-word-game-master/images/Letters/4.png",
               'z': "hellop/Platformer-word-game-master/images/Letters/14.png"}

count = 0
letter = ["a", "b","c", "d", "e", "f", "g", "h","i", "j", "k", "l", "m", "n","o", "t", "u", "v"]
coord = []
def show():
    global x
    global y
    global count
    global desired_height
    global starting_height
    while count < len(letter):
        im = py.image.load(list_images[letter[count]])
        im = py.transform.scale(im, (50,50))
        screen.blit(im, (x + starting_height + 250, y))
        coord.append((x + starting_height + 250, y))
        x += 60

        if x >= desired_height:
            x = 0
            y += 60
            desired_height -= 100
            starting_height += 50
        count += 1


def draw():
    for i in range(len(letter)):
        im = py.image.load(list_images[letter[i]])
        im = py.transform.scale(im, (50,50))
        screen.blit(im, (coord[i]))

def near(x, y):
    z = []
    for i in range(len(x)):
        z.append((math.sqrt(pow((x[i][0] + 25) - y[0], 2)) + math.sqrt(pow((x[i][1] + 25) - y[1], 2))))
    if min(z) < 50:
        return x[z.index(min(z))]
    else:
        return False

rect_list = []

def word_box_show(num):
    word_box = py.image.load("hellop/download (1).jpg")
    word_box = py.transform.scale(word_box, (50, 50))
    for i in range(num):
        rect = word_box.get_rect()
        rect.center = (300 + 60*i,100)
        screen.blit(word_box, rect)
        rect_list.append(rect)

letter_selected = []
def game_loop_select_letters(mystery_number):

    show()
    letters_allowed = 10

    run = True
    while run:
        screen.fill((255,255,255))
        word_box_show(letters_allowed - mystery_number)
        draw()
        mouse = py.mouse.get_pos()
        for ev in py.event.get():
            if ev.type == QUIT:
                run = False
            if ev.type == MOUSEBUTTONDOWN and len(letter_selected) < letters_allowed - mystery_number:
                if near(coord, mouse):
                    selected = near(coord, mouse)
                    print(letter[coord.index(selected)])
                    letter_selected.append(letter[coord.index(selected)])
                    letter.pop(coord.index(selected))
                    coord.remove(selected)
                    print(letter_selected)

        if len(letter_selected) != 0:
            for i in range(len(letter_selected)):
                im = py.image.load(list_images[letter_selected[i]])
                im = py.transform.scale(im, (50,50))
                screen.blit(im, (rect_list[i]))

        py.display.update()

game_loop_select_letters(3)
