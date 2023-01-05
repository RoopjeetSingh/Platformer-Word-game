import pygame
import platform_and_obstacles as po
import screen_size as ss
import letter
import cv2
import numpy as np


class Level:
    def __init__(self, bg, no_tiles: int):
        self.bg_start = cv2.imread(bg)
        self.platform_group = pygame.sprite.Group()
        self.obstruct_group = pygame.sprite.Group()
        self.letter_group = pygame.sprite.Group()
        self.start = 0
        self.width = no_tiles * ss.tile_size
        bg_lis = []
        for i in range(int(self.width / self.bg_start.shape[0]) + 1):
            bg_lis.append(self.bg_start)
        self.bg = np.concatenate(bg_lis, axis=1)
        self.bg = pygame.image.frombuffer(self.bg.tostring(), self.bg.shape[1::-1],
                                          "RGB").convert()
        self.bg = pygame.transform.scale(self.bg, (ss.SCREEN_HEIGHT / self.bg.get_height() * self.bg.get_width(),
                                                   ss.SCREEN_HEIGHT))
        self.bg_display = pygame.image.frombuffer(self.bg_start.tostring(), self.bg_start.shape[1::-1],
                                                  "RGB").convert()
        self.bg_display = pygame.transform.scale(
            self.bg_display,
            (ss.SCREEN_WIDTH / 2.86,
             ss.SCREEN_HEIGHT / 1.56 / self.bg_display.get_width() * self.bg_display.get_height()))

    def draw_for_display(self):
        for i in self.obstruct_group:
            if i.rect.x <= ss.SCREEN_WIDTH:
                i_pos = ((i.rect.x / ss.SCREEN_WIDTH) * self.bg_display.get_width(),
                         (i.rect.y / ss.SCREEN_HEIGHT) * self.bg_display.get_height())
                i_image = pygame.transform.scale(i.image, (i.rect.w * self.bg_display.get_width() / ss.SCREEN_WIDTH,
                                                           i.rect.h * self.bg_display.get_height() / ss.SCREEN_HEIGHT))
                i_image.set_colorkey((0, 0, 0))
                self.bg_display.blit(i_image, i_pos)

        for i in self.platform_group:
            if i.rect.x <= ss.SCREEN_WIDTH:
                i_pos = ((i.rect.x / ss.SCREEN_HEIGHT) * self.bg_display.get_height(),
                         (i.rect.y / ss.SCREEN_HEIGHT) * self.bg_display.get_height())
                i_image = pygame.transform.scale(i.image, (i.rect.w * self.bg_display.get_width() / ss.SCREEN_WIDTH,
                                                     i.rect.h * self.bg_display.get_height() / ss.SCREEN_HEIGHT))
                i_image.set_colorkey((0, 0, 0))
                self.bg_display.blit(i_image, i_pos)

    def draw(self, screen):
        screen.blit(self.bg, (self.start, 0))


class Level1(Level):
    def __init__(self):
        super(Level1, self).__init__(r"images/Background_platformer/BG_03.png", 62)
        self.letter_list = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
        self.make_platforms_objects()
        self.make_letters()
        self.draw_for_display()

    def make_platforms_objects(self):
        # two rows at the bottom of the screen
        for j in range(1, 3):
            self.platform_group.add(po.Platform(0 * ss.tile_size, ss.SCREEN_HEIGHT - j * ss.tile_size, 63, False,
                                    "images/platform/platform_sprites_(1).png"))
        # # ground row
        self.platform_group.add(po.Platform(0, ss.SCREEN_HEIGHT - 3 * ss.tile_size, 63, False))

        # obstacles and platforms
        self.platform_group.add(po.Platform(7 * ss.tile_size, ss.SCREEN_HEIGHT - 6 * ss.tile_size, 1))  # first platform
        self.platform_group.add(po.Platform(10 * ss.tile_size, ss.SCREEN_HEIGHT - 4 * ss.tile_size, 7,
                                            False))  # down row after first platform
        self.platform_group.add(
            po.Platform(12 * ss.tile_size, ss.SCREEN_HEIGHT - 8 * ss.tile_size, 2))  # second tower platform
        self.obstruct_group.add(po.Obstacle(19 * ss.tile_size, ss.SCREEN_HEIGHT - 3 * ss.tile_size - 100,
                                            True, w=100, h=100, set_colorkey=(0, 0, 0)))  # snowman
        self.platform_group.add(po.Platform(29 * ss.tile_size, ss.SCREEN_HEIGHT - 6 * ss.tile_size, 1))
        self.platform_group.add(po.Platform(32 * ss.tile_size, ss.SCREEN_HEIGHT - 4 * ss.tile_size, 7, False))
        self.platform_group.add(po.Platform(34 * ss.tile_size, ss.SCREEN_HEIGHT - 8 * ss.tile_size, 1))
        self.obstruct_group.add(po.Obstacle(43 * ss.tile_size, ss.SCREEN_HEIGHT - 3 * ss.tile_size - 120,
                                            False, w=75, h=120, set_colorkey=(0, 0, 0)))  # Christmas tree
        self.platform_group.add(po.Platform(53 * ss.tile_size, ss.SCREEN_HEIGHT - 6 * ss.tile_size, 1))
        self.platform_group.add(po.Platform(56 * ss.tile_size, ss.SCREEN_HEIGHT - 4 * ss.tile_size, 6, False))
        self.platform_group.add(po.Platform(58 * ss.tile_size, ss.SCREEN_HEIGHT - 8 * ss.tile_size, 1))

        # Letters

    def make_letters(self):
        self.letter_group.add(letter.Letter(self.letter_list[0], 8 * ss.tile_size,
                                            ss.SCREEN_HEIGHT - 8 * ss.tile_size))  # on the first block
        # on the second block
        self.letter_group.add(
            letter.Letter(self.letter_list[1], 12.5 * ss.tile_size, ss.SCREEN_HEIGHT - 10 * ss.tile_size))
        self.letter_group.add(
            letter.Letter(self.letter_list[2], 14.5 * ss.tile_size, ss.SCREEN_HEIGHT - 10 * ss.tile_size))
        self.letter_group.add(letter.MysteryLetter(23*ss.tile_size, ss.SCREEN_HEIGHT - 6 * ss.tile_size))  # special letter to be added here
        self.letter_group.add(
            letter.Letter(self.letter_list[3], 30 * ss.tile_size, ss.SCREEN_HEIGHT - 8 * ss.tile_size))
        self.letter_group.add(
            letter.Letter(self.letter_list[4], 35 * ss.tile_size, ss.SCREEN_HEIGHT - 10 * ss.tile_size))
        self.letter_group.add(
            letter.Letter(self.letter_list[5], 38 * ss.tile_size, ss.SCREEN_HEIGHT - 6 * ss.tile_size))
        self.letter_group.add(
            letter.Letter(self.letter_list[6], 48 * ss.tile_size, ss.SCREEN_HEIGHT - 5 * ss.tile_size))
        self.letter_group.add(
            letter.Letter(self.letter_list[7], 54 * ss.tile_size, ss.SCREEN_HEIGHT - 8 * ss.tile_size))
        self.letter_group.add(
            letter.Letter(self.letter_list[8], 60 * ss.tile_size, ss.SCREEN_HEIGHT - 6 * ss.tile_size))
        self.letter_group.add(
            letter.Letter(self.letter_list[9], 59 * ss.tile_size, ss.SCREEN_HEIGHT - 10 * ss.tile_size))


level1 = Level1()
