import pygame as py
from pygame.locals import *
import math
from letter import Letter
from helpful_functions import blit_text
import wordconnect


x = 100
y = 350
desired_width = 600
starting_width = 0
list_images = Letter.letter_dic

count = 0

coord = []
def show(screen, letter):
    global x
    global y
    global count
    global desired_width
    global starting_width
    while count < len(letter):
        im = py.image.load(list_images[letter[count]])
        im = py.transform.scale(im, (50,50))
        screen.blit(im, (x + starting_width + 250, y))
        coord.append((x + starting_width + 250, y))
        x += 60

        if x >= desired_width:
            x = 100
            y += 60
            desired_width -= 100
            starting_width += 50
        count += 1


def draw(screen, letter):
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

def word_box_show(screen, num):
    word_box = py.image.load("hellop/word_box.jpg")
    word_box = py.transform.scale(word_box, (50, 50))
    for i in range(num):
        rect = word_box.get_rect()
        rect.center = (425 + 60*i,200)
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
deleted_lettters = {}

def game_loop_select_letters(running_letter ,mystery_number, screen):

    show(screen, running_letter)
    letters_allowed = 10
    run = True
    alpha = 200
    while run:
        screen.fill((255,255,255))
        word_box_show(screen,letters_allowed - mystery_number)
        screen.blit(next_button, im_rect)
        draw(screen, running_letter)
        mouse = py.mouse.get_pos()
        deleted_coord = list(deleted_lettters.keys())
        alpha = 0
        for ev in py.event.get():
            if ev.type == QUIT:
                run = False
            if ev.type == MOUSEBUTTONDOWN:
                if len(letter_selected) < letters_allowed - mystery_number:
                    if near(coord, mouse):
                        selected = near(coord, mouse)
                        deleted_lettters[selected] = running_letter[coord.index(selected)]
                        letter_selected.append(running_letter[coord.index(selected)])
                        running_letter.pop(coord.index(selected))
                        coord.remove(selected)
                        print(deleted_coord)

                if im_rect.collidepoint(mouse):
                    if len(letter_selected) > 0:
                        run = False

                    else:
                        print(123)
                        blit_text(screen,"selct one letter", (200, 200), py.font.Font(None, 30), 250, color= (0,0,0), alpha = min(alpha, 255))
                        if alpha <= 300:
                            alpha += 0.75

        if len(letter_selected) != 0:
            for i in range(len(letter_selected)):
                im = py.image.load(list_images[letter_selected[i]])
                im = py.transform.scale(im, (50,50))
                screen.blit(im, (rect_list[i]))

        py.display.update()

    transition(screen)

if __name__ == "__main__":
    screen = py.display.set_mode((1200, 600))
    game_loop_select_letters(["a", "b", "c","d", 'e', 'f', 'g'],3, screen)
    wordconnect.game_Loop_Wordle(screen,letter_selected, 3)
    py.quit()
