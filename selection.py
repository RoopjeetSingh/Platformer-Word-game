import pygame as py
from pygame.locals import *
import math
from letter import Letter
import time

screen = py.display.set_mode((1300, 710))
list_images = Letter.letter_dic
coord = []
show_count = 1
test = []

def show(screen, letter):
    x = 300
    y = 375
    size = determine_size(letter)
    desired_width = 1000
    starting_width = 0
    for count in range(len(letter)):
        im = py.image.load(list_images[letter[count]])
        im = py.transform.scale(im, (size[0],size[0]))
        screen.blit(im, (x + starting_width, y))
        test.append((x + starting_width, y))
        coord.append((x + starting_width, y))
        x += size[1]
        if x >= desired_width:
            x = 300
            y += size[1]

def determine_size(letter):
    if len(letter) <= 15:
        size = 75
    elif len(letter) >= 15:
        size = 50
    index = size + 5
    return (size, index)

def draw(screen, letter):
    size = determine_size(letter)
    for i in range(len(letter)):
        im = py.image.load(list_images[letter[i]])
        im = py.transform.scale(im, (size[0], size[0]))
        screen.blit(im, (coord[i]))

def near(x, y, letter):
    z = []
    for i in range(len(x)):
        z.append((math.sqrt(pow((x[i][0]) - y[0] + 37, 2)) + math.sqrt(pow((x[i][1]) - y[1] + 37, 2))))
    if min(z) < 50:
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
    font= py.font.Font(None, 50)
    text = font.render("will be right back", True, (255,255,255))
    star_color =255
    while star_color >= 0:
        screen.fill((star_color, star_color, star_color))
        star_color -= 1
        screen.blit(text, (650, 350))
        py.display.flip()

def loading_screen(screen):
    count = 1
    while count <= 200:
        py.draw.rect(screen, (255,255,255), (100,100, 200, 50), width= 5)
        py.draw.rect(screen, (214,45,87), (100, 100,count, 50))
        count += 5
        py.display.flip()
        time.sleep(0.2)
letter_selected = []


def game_loop_select_letters(running_letter ,mystery_number, screen, letters_allowed):

    show(screen, running_letter)
    print(coord)
    print(test)
    run = True

    image = py.image.load("hellop/selecctionfre.jpg")
    image = py.transform.scale(image, (1300, 710))

    while run:
        screen.blit(image, (0, 0))
        word_box_show(screen,letters_allowed - mystery_number, )
        screen.blit(next_button, im_rect)
        draw(screen, running_letter)
        mouse = py.mouse.get_pos()

        for ev in py.event.get():
            if ev.type == QUIT:
                run = False
            if ev.type == MOUSEBUTTONDOWN:
                if len(letter_selected) < letters_allowed - mystery_number:
                    if near(coord, mouse, running_letter):
                        selected = near(coord, mouse, running_letter)

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
    loading_screen(screen)
