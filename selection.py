import pygame as py
from pygame.locals import *
import math
from letter import Letter
from helpful_functions import blit_text
import wordconnect

screen = py.display.set_mode((1300, 710))
list_images = Letter.letter_dic
coord = []

def show(screen, letter):
    x = 320
    y = 375
    size = 100
    index = size + 5
    desired_width = 320 + index * (len(letter) // 2)
    starting_width = 0

    for count in range(len(letter)):
        im = py.image.load(list_images[letter[count]])
        im = py.transform.scale(im, (size,size))
        screen.blit(im, (x + starting_width, y))
        coord.append((x + starting_width, y))
        x += index
        if x >= desired_width:
            x = 320
            y += index

def draw(screen, letter):
    for i in range(len(letter)):
        im = py.image.load(list_images[letter[i]])
        im = py.transform.scale(im, (100,100))
        screen.blit(im, (coord[i]))

def near(x, y):
    z = []
    index = 105
    for i in range(len(x)):
        z.append((math.sqrt(pow((x[i][0] + 25) - y[0], 2)) + math.sqrt(pow((x[i][1] + 25) - y[1], 2))))
    if min(z) < index:
        return x[z.index(min(z))]
    else:
        return False

rect_list = []

def word_box_show(screen, num):
    word_box = py.image.load("hellop/word_box.jpg")
    word_box = py.transform.scale(word_box, (50, 50))
    starting_point = (1300 - (num * 60)) // 2

    for i in range(num):
        rect = word_box.get_rect()
        rect.center = (starting_point + 60*i,200)
        screen.blit(word_box, rect)
        rect_list.append(rect)

next_button = py.image.load("hellop/arrow1.png")
next_button = py.transform.scale(next_button, (50, 50))
im_rect = next_button.get_rect()
im_rect.center = (25,25)
def transition(screen):
    star_color = 100
    while star_color >= 0:
        screen.fill((star_color, star_color, star_color))
        star_color -= 1
        py.display.flip()

letter_selected = []


def game_loop_select_letters(running_letter ,mystery_number, screen, letters_allowed):

    show(screen, running_letter)
    run = True
    while run:
        screen.fill((255,255,255))
        word_box_show(screen,letters_allowed - mystery_number, )
        screen.blit(next_button, im_rect)
        draw(screen, running_letter)
        mouse = py.mouse.get_pos()

        for ev in py.event.get():
            if ev.type == QUIT:
                run = False
            if ev.type == MOUSEBUTTONDOWN:
                if len(letter_selected) < letters_allowed - mystery_number:
                    if near(coord, mouse):
                        selected = near(coord, mouse)

                        letter_selected.append(running_letter[coord.index(selected)])
                        running_letter.pop(coord.index(selected))
                        coord.remove(selected)


                if im_rect.collidepoint(mouse):
                    if len(letter_selected) > 0:
                        run = False

        if len(letter_selected) != 0:
            for i in range(len(letter_selected)):
                im = py.image.load(list_images[letter_selected[i]])
                im = py.transform.scale(im, (50,50))
                screen.blit(im, (rect_list[i]))

        py.display.update()

    transition(screen)

if __name__ == "__main__":
    game_loop_select_letters(["a", "b", "c","d", 'e', 'f', 'g','h', 'i', 'j', 'k', "h"],3, screen, 10)
    wordconnect.game_Loop_Wordle(screen,letter_selected, 3)
    py.quit()
