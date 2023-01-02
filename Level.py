import pygame
import platform_and_obstacles as po
import screen_size as ss
import letter
import cv2
import numpy as np


class Level:
    def __init__(self, bg, no_tiles: int):
        self.bg = cv2.imread(bg)
        self.platform_group = pygame.sprite.Group()
        self.obstruct_group = pygame.sprite.Group()
        self.letter_group = pygame.sprite.Group()
        self.start = 0
        self.width = no_tiles * ss.tile_size
        bg_lis = []
        for i in range(int(self.width / self.bg.shape[0]) + 1):
            bg_lis.append(self.bg)
        self.bg = np.concatenate(bg_lis, axis=1)
        self.bg = pygame.image.frombuffer(self.bg.tostring(), self.bg.shape[1::-1],
                                          "RGB").convert_alpha()
        self.bg = pygame.transform.scale(self.bg, (ss.SCREEN_HEIGHT / self.bg.get_height() * self.bg.get_width(),
                                                   ss.SCREEN_HEIGHT))

    def draw(self, screen):
        screen.blit(self.bg, (self.start, 0))


class Level1(Level):
    """Sample level"""
    def __init__(self, letter_list: list[str, str, str, str, str, str, str, str, str, str]):
        super(Level1, self).__init__(r"images/BG_03.png", 62)
        self.letter_list = letter_list
        self.make_platforms_objects()
        self.make_letters()

    def make_platforms_objects(self):
        # two rows at the bottom of the screen
        for j in range(2, 0, -1):
            for i in range(63):
                self.platform_group.add(
                    po.Platform(i * ss.tile_size, ss.SCREEN_HEIGHT - j * ss.tile_size, 0, True,
                                "images/platform/platform_sprites_(1).png", ss.tile_size, ss.tile_size))

        # ground row
        for i in range(63):
            self.platform_group.add(
                po.Platform(i * ss.tile_size, ss.SCREEN_HEIGHT - 3 * ss.tile_size, 0, True,
                            "images/platform/platform_sprites_(27).png", ss.tile_size, ss.tile_size))

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
        # self.letter_group.add(letter.Letter(self.letter_list[3], 23*ss.tile_size, ss.SCREEN_HEIGHT - 5 * ss.tile_size))  # special letter to be added here
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
