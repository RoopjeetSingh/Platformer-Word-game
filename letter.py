import pygame
import screen_size as ss
import math

pygame.init()
screen = pygame.display.set_mode((int(ss.SCREEN_WIDTH / 2.3833), int(ss.SCREEN_WIDTH / 3.575)))


class Letter(pygame.sprite.Sprite):
    letter_dic = {'a': "images/Letters/1.png", 'b': "images/Letters/9.png", 'c': "images/Letters/19.png",
                  'd': "images/Letters/15.png", 'e': "images/Letters/26.png", 'f': "images/Letters/23.png",
                  'g': "images/Letters/18.png", 'h': "images/Letters/2.png", 'i': "images/Letters/7.png",
                  'j': "images/Letters/12.png", 'k': "images/Letters/3.png", 'l': "images/Letters/16.png",
                  'm': "images/Letters/28.png", 'n': "images/Letters/25.png", 'o': "images/Letters/22.png",
                  'p': "images/Letters/0.png", 'q': "images/Letters/6.png", 'r': "images/Letters/17.png",
                  's': "images/Letters/20.png", 't': "images/Letters/13.png", 'u': "images/Letters/21.png",
                  'v': "images/Letters/24.png", 'w': "images/Letters/11.png", 'x': "images/Letters/10.png",
                  'y': "images/Letters/4.png", 'z': "images/Letters/14.png"}

    def __init__(self, letter: str, x: int, y: int):
        super(Letter, self).__init__()
        self.distance = None
        self.end_pos = (0, 0)
        self.letter = letter
        self.image1 = pygame.image.load(Letter.letter_dic.get(self.letter)).convert()
        self.image1 = pygame.transform.scale(self.image1, (ss.tile_size, ss.tile_size))
        self.image = self.image1
        self.rect_original = self.image.get_rect(topleft=(x, y))
        self.rect = self.rect_original.copy()
        self.pos = [x, y]
        self.start_y = y
        self.num = 0
        self.going_down = True
        self.gravity = 1
        self.collecting_animation = False
        self.brighten = True
        self.size = 1
        self.num_collect_anim = 0
        self.angle = 0

    def bounce_brighten(self):
        if self.brighten:
            new_width = round(math.sin(math.radians(self.angle)) * self.rect_original.width)
            self.angle += 2
            self.image = self.image1 if new_width >= 0 else pygame.transform.flip(self.image1, True, False)
            self.image = pygame.transform.scale(self.image, (abs(new_width), self.rect_original.height))
            self.rect = self.image.get_rect(center=self.rect_original.center)

            if self.going_down:
                self.pos[1] += self.gravity
                self.rect_original.y = round(self.pos[1])
            else:
                self.pos[1] -= self.gravity
                self.rect_original.y = round(self.pos[1])

            if self.start_y >= self.rect_original.y:
                self.going_down = True
                self.rect_original.y = self.start_y
            if self.rect_original.y - self.start_y >= ss.tile_size:
                self.going_down = False
            self.num += 1

    def collect_self(self, player, level):
        if self.collecting_animation:
            if self.num_collect_anim == 0:
                self.rect = self.rect_original.copy()
                level.letter_group.remove(self)
                self.image = self.image1
                self.brighten = False
                self.end_pos = (
                    ((len(player.letter_lis) - 1) * (ss.tile_size + 20) + int(ss.SCREEN_WIDTH / 71.5), ss.tile_size),
                    (self.rect.x, self.rect.y))
                self.distance = ((self.end_pos[1][0] - self.end_pos[0][0]) / 5,
                                 (self.end_pos[1][1] - self.end_pos[0][1]) / 5)
            if self.num_collect_anim % 5 == 0:
                self.rect.x -= round(self.distance[0])
                self.rect.y -= round(self.distance[1])
            if abs(self.end_pos[0][0] - self.rect.x) <= 5 and abs(
                    self.end_pos[0][1] - self.rect.y) <= 5:
                self.rect.x = self.end_pos[0][0]
                self.rect.y = self.end_pos[0][1]
                self.collecting_animation = False
            self.num_collect_anim += 1


class MysteryLetter(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(MysteryLetter, self).__init__()
        self.distance = None
        self.end_pos = (0, 0)
        self.image1 = pygame.image.load("images/Letters/mysteryLetter.png").convert()
        self.image1 = pygame.transform.scale(self.image1, (ss.tile_size * 1.5, ss.tile_size * 1.5))
        self.image = self.image1
        self.rect_original = self.image.get_rect(topleft=(x, y))
        self.rect = self.rect_original.copy()
        self.pos = [x, y]
        self.start_y = y
        self.num = 0
        self.going_down = True
        self.gravity = 1
        self.collecting_animation = False
        self.brighten = True
        self.size = 1
        self.num_collect_anim = 0
        self.angle = 0

    def bounce_brighten(self):
        if self.brighten:
            new_width = round(math.sin(math.radians(self.angle)) * self.rect_original.width)
            self.angle += 2
            self.image = self.image1 if new_width >= 0 else pygame.transform.flip(self.image1, True, False)
            self.image = pygame.transform.scale(self.image, (abs(new_width), self.rect_original.height))
            self.rect = self.image.get_rect(center=self.rect_original.center)

            if self.going_down:
                self.pos[1] += self.gravity
                self.rect_original.y = round(self.pos[1])
            else:
                self.pos[1] -= self.gravity
                self.rect_original.y = round(self.pos[1])

            if self.start_y > self.rect_original.y:
                self.going_down = True
                self.rect_original.y = self.start_y
            if self.rect_original.y - self.start_y >= ss.tile_size:
                self.going_down = False
            self.num += 1

    def collect_self(self, player, level):
        if self.collecting_animation:
            if self.num_collect_anim == 0:
                level.letter_group.remove(self)
                self.image = self.image1
                self.brighten = False
                self.end_pos = (
                    ((len(player.mystery_letter_lis) - 1) * (ss.tile_size + 45) + int(ss.SCREEN_WIDTH / 71.5), ss.tile_size * 2 + int(ss.SCREEN_WIDTH / 143)),
                    (self.rect_original.x, self.rect_original.y))
                self.distance = ((self.end_pos[1][0] - self.end_pos[0][0]) / 5,
                                 (self.end_pos[1][1] - self.end_pos[0][1]) / 5)
            if self.num_collect_anim % 5 == 0:
                self.rect_original.x -= round(self.distance[0])
                self.rect_original.y -= round(self.distance[1])
            if abs(self.end_pos[0][0] - self.rect_original.x) <= 5 and abs(
                    self.end_pos[0][1] - self.rect_original.y) <= 5:
                self.rect_original.x = self.end_pos[0][0]
                self.rect_original.y = self.end_pos[0][1]
                self.collecting_animation = False
            self.num_collect_anim += 1
            self.rect = self.rect_original.copy()
