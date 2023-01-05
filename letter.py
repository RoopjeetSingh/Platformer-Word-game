import pygame
import screen_size as ss

pygame.init()
screen = pygame.display.set_mode((600, 400))


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
        self.image2 = self.image1.copy()
        brighten = 60
        self.image2.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_ADD)
        self.image = self.image1
        self.rect = self.image.get_rect(topleft=(x, y))
        self.pos = [x, y]
        self.start_y = y
        self.num = 0
        self.going_down = True
        self.gravity = 1
        self.collecting_animation = False
        self.brighten = True
        self.size = 1
        self.num_collect_anim = 0

    def bounce_brighten(self):
        if self.brighten:
            if self.image == self.image1 and self.num >= 30:
                self.image = self.image2
                self.num = 0
            elif self.image == self.image2 and self.num >= 30:
                self.image = self.image1
                self.num = 0

            if self.going_down:
                self.pos[1] += self.gravity
                self.rect.y = round(self.pos[1])
            else:
                self.pos[1] -= self.gravity
                self.rect.y = round(self.pos[1])

            if self.start_y > self.rect.y:
                self.going_down = True
                self.rect.y = self.start_y
            if self.rect.y - self.start_y >= 50:
                self.going_down = False
            self.num += 1

    def collect_self(self, player, level):
        if self.collecting_animation:
            if self.num_collect_anim == 0:
                level.letter_group.remove(self)
                self.image = self.image1
                self.brighten = False
                self.end_pos = (
                    ((len(player.letter_lis) - 1) * (ss.tile_size + 20) + 20, ss.tile_size), (self.rect.x, self.rect.y))
                self.distance = ((self.end_pos[1][0] - self.end_pos[0][0]) / 5,
                                 (self.end_pos[1][1] - self.end_pos[0][1]) / 5)
            if self.num_collect_anim % 5 == 0:
                self.rect.x -= round(self.distance[0])
                self.rect.y -= round(self.distance[1])
            # if self.num_collect_anim == 20:
            if abs(self.end_pos[0][0] - self.rect.x) <= 5 and abs(self.end_pos[0][1] - self.rect.y) <= 5:
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
        self.image1 = pygame.transform.scale(self.image1, (ss.tile_size*2, ss.tile_size*2))
        self.image2 = self.image1.copy()
        brighten = 60
        self.image2.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_ADD)
        self.image = self.image1
        self.rect = self.image.get_rect(topleft=(x, y))
        self.pos = [x, y]
        self.start_y = y
        self.num = 0
        self.going_down = True
        self.gravity = 1
        self.collecting_animation = False
        self.brighten = True
        self.size = 1
        self.num_collect_anim = 0

    def bounce_brighten(self):
        if self.brighten:
            if self.image == self.image1 and self.num >= 30:
                self.image = self.image2
                self.num = 0
            elif self.image == self.image2 and self.num >= 30:
                self.image = self.image1
                self.num = 0

            if self.going_down:
                self.pos[1] += self.gravity
                self.rect.y = round(self.pos[1])
            else:
                self.pos[1] -= self.gravity
                self.rect.y = round(self.pos[1])

            if self.start_y > self.rect.y:
                self.going_down = True
                self.rect.y = self.start_y
            if self.rect.y - self.start_y >= 50:
                self.going_down = False
            self.num += 1

    def collect_self(self, player, level):
        if self.collecting_animation:
            if self.num_collect_anim == 0:
                level.letter_group.remove(self)
                self.image = self.image1
                self.brighten = False
                self.end_pos = (((len(player.mystery_letter_lis) - 1) * (ss.tile_size + 20) + 20, ss.tile_size*2+10),
                                (self.rect.x, self.rect.y))
                self.distance = ((self.end_pos[1][0] - self.end_pos[0][0]) / 5,
                                 (self.end_pos[1][1] - self.end_pos[0][1]) / 5)
            if self.num_collect_anim % 5 == 0:
                self.rect.x -= round(self.distance[0])
                self.rect.y -= round(self.distance[1])
            if abs(self.end_pos[0][0] - self.rect.x) <= 5 and abs(self.end_pos[0][1] - self.rect.y) <= 5:
                self.rect.x = self.end_pos[0][0]
                self.rect.y = self.end_pos[0][1]
                self.collecting_animation = False
            self.num_collect_anim += 1


def a_letter(x, y):
    return Letter("a", x, y)


def b_letter(x, y):
    return Letter("b", x, y)


def c_letter(x, y):
    return Letter("c", x, y)


def d_letter(x, y):
    return Letter("d", x, y)


def e_letter(x, y):
    return Letter("e", x, y)


def f_letter(x, y):
    return Letter("f", x, y)


def g_letter(x, y):
    return Letter("g", x, y)


def h_letter(x, y):
    return Letter("h", x, y)


def i_letter(x, y):
    return Letter("i", x, y)


def j_letter(x, y):
    return Letter("j", x, y)


def k_letter(x, y):
    return Letter("k", x, y)


def l_letter(x, y):
    return Letter("l", x, y)


def m_letter(x, y):
    return Letter("m", x, y)


def n_letter(x, y):
    return Letter("n", x, y)


def o_letter(x, y):
    return Letter("o", x, y)


def p_letter(x, y):
    return Letter("p", x, y)


def q_letter(x, y):
    return Letter("q", x, y)


def r_letter(x, y):
    return Letter("r", x, y)


def s_letter(x, y):
    return Letter("s", x, y)


def t_letter(x, y):
    return Letter("t", x, y)


def u_letter(x, y):
    return Letter("u", x, y)


def v_letter(x, y):
    return Letter("v", x, y)


def w_letter(x, y):
    return Letter("w", x, y)


def x_letter(x, y):
    return Letter("x", x, y)


def y_letter(x, y):
    return Letter("y", x, y)


def z_letter(x, y):
    return Letter("z", x, y)
