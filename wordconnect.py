import time
import pygame as py
from pygame.locals import *
from pygame import mixer
import math

py.init()
mixer.init()
mixer.music.load("./hellop/success-1-6297.mp3")
screen = py.display.set_mode((1000, 500))
screen.fill((255, 255, 255))
letters = ["a", "b", "c", "d", "e"]

# find better images here
list_images = {"a": py.image.load("./hellop/im.png"), "b": py.image.load("./hellop/b.png"),
               "c": py.image.load("./hellop/images (1).png"), "d": py.image.load("./hellop/d.png"),
               "e": py.image.load("hellop/6422859.png")}
coord = []
entered = []
correct_words = ["dabc", "ebcd"]
word = ""


def background(x,y,z):
    bg_image = py.image.load("hellop/winter.jpg")
    bg_image = py.transform.scale(bg_image, (1000, 500))
    table = py.Surface((400, 100))
    table.set_alpha(128)
    table.fill((x,y,z))
    screen.blit(bg_image, (0, 0))
    screen.blit(table, (300, 50))


def place(n):
    global coord
    a = 0
    adding = (2 * 3.14) / n
    for i in range(0, n):
        im = list_images[letters[i]]
        im = py.transform.scale(im, (35, 35))
        screen.blit(im, (480 + 130 * math.cos(a), 320 + 130 * math.sin(a)))
        coord.append((480 + 130 * math.cos(a), 320 + 130 * math.sin(a)))
        a += adding


def near(x, y):
    z = []
    for i in range(len(x)):
        z.append((math.sqrt(pow(x[i][0] - y[0], 2)) + math.sqrt(pow(x[i][1] - y[1], 2))))

    return x[z.index(min(z))]


def show():
    global word

    adding = 30
    subtraction = 15
    for i in range(len(word)):
        im = list_images[word[i]]
        im = py.transform.scale(im, (25, 25))
        screen.blit(im, (500 + (adding * i) - (subtraction * len(word)), 90))




def correct():
    py.mixer.music.play()
    time.sleep(0.8)
    py.mixer.music.stop()


run = True
background(255,255,255)
place(len(letters))
start = ()

while run:

    mouse = py.mouse.get_pos()
    for ev in py.event.get():
        if ev.type == QUIT:
            py.quit()
        if ev.type == MOUSEBUTTONDOWN:
            start = near(coord, mouse)
            if start not in entered:
                word += letters[coord.index(start)]
                entered.append(start)
            else:
                word = ""
                entered = []

    if start != ():
        background(255,255,255)
        place(len(letters))
        py.draw.line(screen, (34, 153, 153), (start[0] + 20, start[1] + 20), (mouse[0] + 20, mouse[1] + 20), width=5)
        show()
        if len(word) == len(letters):
            start= ()
            entered = []
            background(201, 47, 4)
            place(len(letters))
            show()
            word = ""

        elif word in correct_words:
            start= ()
            entered = []
            background(235, 235, 35)
            place(len(letters))
            show()
            word = ""
    py.display.update()

