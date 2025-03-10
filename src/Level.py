import pygame
import platform_and_obstacles as po
import screen_size as ss
import letter
import cv2
import numpy as np
import power_ups as pu
import random
from decode_file import decode_file
import smaller_store
import platforms_obstacles_images

background_list = [smaller_store.bg_1, smaller_store.bg_2]

bg_display_level = {"level1": smaller_store.level1_bg_display,
                    "level2": smaller_store.level2_bg_display,
                    "level3": smaller_store.level3_bg_display,
                    "level4": smaller_store.level4_bg_display,
                    "level5": smaller_store.level5_bg_display}


def level_generator(no_of_letters: int):
    letter_lis = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                  'u', 'v', 'w', 'x', 'y', 'z']
    weights = [
            43.31, 10.56, 23.13, 17.25, 56.88, 9.24, 12.59, 15.31, 38.45, 1, 5.61, 27.98,
            15.36,
            33.92, 36.51, 16.14, 1, 38.64, 29.23, 35.43, 18.51, 5.13, 6.57, 1.48, 9.06,
            1.39]
    random_letters = []
    for i in range(no_of_letters):
        random_letter = random.choices(letter_lis, weights=weights)
        random_letters.append(random_letter[0])
        weights.remove(weights[letter_lis.index(random_letter[0])])
        letter_lis.remove(random_letter[0])
    return random_letters


class Level:
    def __init__(self, bg, no_tiles: int, level_name):
        self.tiles = no_tiles
        self.bg_start = cv2.imdecode(np.frombuffer(decode_file(bg).read(), np.uint8), 1)
        self.platform_group = pygame.sprite.Group()
        self.obstruct_group = pygame.sprite.Group()
        self.letter_group = pygame.sprite.Group()
        self.power_up_group = pygame.sprite.Group()
        # Would be overloaded in the subclasses
        self.letter_list = []
        self.time = 0
        self.stars = [0, 0, 0]
        #######################################
        self.start = 0
        self.width = no_tiles * ss.tile_size
        self.str = level_name
        bg_lis = []
        for i in range(int(self.width / self.bg_start.shape[0]) + 1):
            bg_lis.append(self.bg_start)
        self.bg = np.concatenate(bg_lis, axis=1)
        self.bg = pygame.image.frombuffer(self.bg.tostring(), self.bg.shape[1::-1],
                                          "RGB").convert()
        self.bg = pygame.transform.scale(self.bg, (ss.SCREEN_HEIGHT / self.bg.get_height() * self.bg.get_width(),
                                                   ss.SCREEN_HEIGHT))
        self.bg_display = pygame.image.load(decode_file(bg_display_level[self.str]))

    def draw(self, screen):
        screen.blit(self.bg, (self.start, 0))

    def clear(self):
        self.platform_group = pygame.sprite.Group()
        self.obstruct_group = pygame.sprite.Group()
        self.letter_group = pygame.sprite.Group()
        self.power_up_group = pygame.sprite.Group()


class Level1(Level):
    def __init__(self):
        super(Level1, self).__init__(random.choice(background_list), 62, "level1")
        self.no_of_letter = 8
        self.stars = 30
        self.time = 45

    def make_platforms_objects(self):
        # two rows at the bottom of the screen
        for j in range(1, 3):
            self.platform_group.add(po.Platform(0, ss.SCREEN_HEIGHT - j * ss.tile_size, self.tiles, False,
                                                (platforms_obstacles_images.base_platform)))
        # ground row
        self.platform_group.add(po.Platform(0, ss.SCREEN_HEIGHT - 3 * ss.tile_size, self.tiles, False))

        # obstacles and platforms
        self.platform_group.add(po.Platform(7 * ss.tile_size, ss.SCREEN_HEIGHT - 6 * ss.tile_size, 1))  # first platform
        self.platform_group.add(po.Platform(10 * ss.tile_size, ss.SCREEN_HEIGHT - 4 * ss.tile_size, 7,
                                            False))  # down row after first platform
        self.platform_group.add(
            po.Platform(12 * ss.tile_size, ss.SCREEN_HEIGHT - 8 * ss.tile_size, 2))  # second tower platform

        self.obstruct_group.add(po.Obstacle(19 * ss.tile_size, ss.SCREEN_HEIGHT - 4 * ss.tile_size,
                                            "spikes", w=ss.tile_size * 2, h=ss.tile_size))  # cutter
        self.platform_group.add(po.Platform(29 * ss.tile_size, ss.SCREEN_HEIGHT - 6 * ss.tile_size, 1))
        self.platform_group.add(po.Platform(32 * ss.tile_size, ss.SCREEN_HEIGHT - 4 * ss.tile_size, 7, False))
        self.platform_group.add(po.Platform(34 * ss.tile_size, ss.SCREEN_HEIGHT - 8 * ss.tile_size, 1))

        self.obstruct_group.add(po.Obstacle(43 * ss.tile_size, ss.SCREEN_HEIGHT - 4 * ss.tile_size,
                                            "spikes", w=ss.tile_size * 2, h=ss.tile_size))  # cutter
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
        self.letter_group.add(letter.MysteryLetter(23 * ss.tile_size, ss.SCREEN_HEIGHT - 6 * ss.tile_size))
        self.letter_group.add(
            letter.Letter(self.letter_list[2], 30 * ss.tile_size, ss.SCREEN_HEIGHT - 8 * ss.tile_size))
        self.letter_group.add(
            letter.Letter(self.letter_list[3], 35 * ss.tile_size, ss.SCREEN_HEIGHT - 10 * ss.tile_size))
        self.letter_group.add(letter.MysteryLetter(35 * ss.tile_size, ss.SCREEN_HEIGHT - 7 * ss.tile_size))
        self.letter_group.add(
            letter.Letter(self.letter_list[4], 38 * ss.tile_size, ss.SCREEN_HEIGHT - 6 * ss.tile_size))
        self.letter_group.add(
            letter.Letter(self.letter_list[5], 48 * ss.tile_size, ss.SCREEN_HEIGHT - 5 * ss.tile_size))
        self.letter_group.add(
            letter.Letter(self.letter_list[6], 54 * ss.tile_size, ss.SCREEN_HEIGHT - 8 * ss.tile_size))
        self.letter_group.add(
            letter.Letter(self.letter_list[7], 59 * ss.tile_size, ss.SCREEN_HEIGHT - 10 * ss.tile_size))

    def make_power_ups(self):
        self.power_up_group.add(pu.DoubleJumpPowerUp(50 * ss.tile_size, ss.SCREEN_HEIGHT - 4 * ss.tile_size))


class Level2(Level):
    def __init__(self):
        super(Level2, self).__init__(random.choice(background_list), 112, "level2")
        self.no_of_letter = 12
        self.stars = 30
        self.time = 45

    def make_letters(self):
        self.letter_group.add(letter.Letter(self.letter_list[0], 4 * ss.tile_size,  # tile_size = 200
                                            ss.SCREEN_HEIGHT - 5 * ss.tile_size))  # 1 is the original +3 ground platform+1 bouncing=5 normally, 5
        self.letter_group.add(letter.Letter(self.letter_list[1], 8 * ss.tile_size,
                                            ss.SCREEN_HEIGHT - 8 * ss.tile_size))
        self.letter_group.add(letter.Letter(self.letter_list[2], 23 * ss.tile_size,
                                            ss.SCREEN_HEIGHT - 5 * ss.tile_size))
        self.letter_group.add(letter.MysteryLetter(31 * ss.tile_size,
                                                   ss.SCREEN_HEIGHT - 12 * ss.tile_size))
        self.letter_group.add(letter.Letter(self.letter_list[3], 37 * ss.tile_size,
                                            ss.SCREEN_HEIGHT - 9 * ss.tile_size))
        self.letter_group.add(letter.Letter(self.letter_list[4], 54 * ss.tile_size,
                                            ss.SCREEN_HEIGHT - 11 * ss.tile_size))
        self.letter_group.add(letter.Letter(self.letter_list[5], 67 * ss.tile_size,
                                            ss.SCREEN_HEIGHT - 5 * ss.tile_size))
        self.letter_group.add(letter.Letter(self.letter_list[6], 73 * ss.tile_size,
                                            ss.SCREEN_HEIGHT - 13 * ss.tile_size))
        self.letter_group.add(letter.Letter(self.letter_list[7], 80 * ss.tile_size,
                                            ss.SCREEN_HEIGHT - 13 * ss.tile_size))
        self.letter_group.add(letter.Letter(self.letter_list[8], 85 * ss.tile_size,
                                            ss.SCREEN_HEIGHT - 10 * ss.tile_size))
        self.letter_group.add(letter.Letter(self.letter_list[9], 92 * ss.tile_size,
                                            ss.SCREEN_HEIGHT - 13 * ss.tile_size))
        self.letter_group.add(letter.Letter(self.letter_list[10], 98 * ss.tile_size,
                                            ss.SCREEN_HEIGHT - 14 * ss.tile_size))
        self.letter_group.add(letter.MysteryLetter(102 * ss.tile_size,
                                                   ss.SCREEN_HEIGHT - 14 * ss.tile_size))
        self.letter_group.add(letter.Letter(self.letter_list[11], 106 * ss.tile_size,
                                            ss.SCREEN_HEIGHT - 6 * ss.tile_size))

    def make_platforms_objects(self):
        for j in range(1, 3):
            self.platform_group.add(
                po.Platform(0 * ss.tile_size, ss.SCREEN_HEIGHT - j * ss.tile_size, self.tiles, False,
                            (platforms_obstacles_images.base_platform)))
        # # ground row
        self.platform_group.add(po.Platform(0, ss.SCREEN_HEIGHT - 3 * ss.tile_size, self.tiles, False))  # 0+3
        # the upper stuff should be copied

        self.platform_group.add(po.Platform(8 * ss.tile_size, ss.SCREEN_HEIGHT - 6 * ss.tile_size,
                                            1))  # x, y, no_of_tiles, rectangle or curve
        self.platform_group.add(po.Platform(13 * ss.tile_size, ss.SCREEN_HEIGHT - 9 * ss.tile_size, 1))
        self.platform_group.add(po.Platform(25 * ss.tile_size, ss.SCREEN_HEIGHT - 6 * ss.tile_size, 1))
        self.platform_group.add(po.Platform(30 * ss.tile_size, ss.SCREEN_HEIGHT - 13 * ss.tile_size, 1))
        self.platform_group.add(po.Platform(35 * ss.tile_size, ss.SCREEN_HEIGHT - 7 * ss.tile_size, 1))
        self.platform_group.add(po.Platform(53 * ss.tile_size, ss.SCREEN_HEIGHT - 9 * ss.tile_size, 4, False))
        self.platform_group.add(po.Platform(69 * ss.tile_size, ss.SCREEN_HEIGHT - 6 * ss.tile_size, 1))
        self.platform_group.add(po.Platform(76 * ss.tile_size, ss.SCREEN_HEIGHT - 11 * ss.tile_size, 7, False))
        self.platform_group.add(po.Platform(84 * ss.tile_size, ss.SCREEN_HEIGHT - 6 * ss.tile_size, 7, False))
        self.platform_group.add(po.Platform(92 * ss.tile_size, ss.SCREEN_HEIGHT - 11 * ss.tile_size, 1))
        self.platform_group.add(po.Platform(97 * ss.tile_size, ss.SCREEN_HEIGHT - 15 * ss.tile_size, 1))
        self.platform_group.add(po.Platform(102 * ss.tile_size, ss.SCREEN_HEIGHT - 11 * ss.tile_size, 2, False))
        self.platform_group.add(po.Platform(105 * ss.tile_size, ss.SCREEN_HEIGHT - 6 * ss.tile_size, 1, False))
        self.platform_group.add(po.Platform(106 * ss.tile_size, ss.SCREEN_HEIGHT - 4 * ss.tile_size, 6, False))

        self.obstruct_group.add(po.Obstacle(17 * ss.tile_size, ss.SCREEN_HEIGHT - 4 * ss.tile_size,
                                            "spikes", w=ss.tile_size * 2, h=ss.tile_size))
        self.obstruct_group.add(po.Obstacle(42 * ss.tile_size, ss.SCREEN_HEIGHT - 4 * ss.tile_size,
                                            "spikes", w=ss.tile_size * 2, h=ss.tile_size))
        self.obstruct_group.add(po.Obstacle(50 * ss.tile_size, ss.SCREEN_HEIGHT - 5 * ss.tile_size,
                                            "snowman", w=ss.tile_size * 2, h=ss.tile_size * 2))
        self.obstruct_group.add(po.Obstacle(63 * ss.tile_size, ss.SCREEN_HEIGHT - 5 * ss.tile_size,
                                            "tree", w=ss.tile_size * 2 / 1.7, h=ss.tile_size * 2))
        self.obstruct_group.add(po.Obstacle(78 * ss.tile_size, ss.SCREEN_HEIGHT - 12 * ss.tile_size,
                                            "spikes", w=ss.tile_size * 2, h=ss.tile_size))
        self.obstruct_group.add(po.Obstacle(87 * ss.tile_size, ss.SCREEN_HEIGHT - 8 * ss.tile_size,
                                            "snowman", w=ss.tile_size * 2, h=ss.tile_size * 2))
        self.obstruct_group.add(po.Obstacle(109 * ss.tile_size, ss.SCREEN_HEIGHT - 6 * ss.tile_size,
                                            "tree", w=ss.tile_size * 2 / 1.7, h=ss.tile_size * 2))

    def make_power_ups(self):
        self.power_up_group.add(pu.DoubleJumpPowerUp(46 * ss.tile_size, ss.SCREEN_HEIGHT - 4 * ss.tile_size))
        self.power_up_group.add(pu.DoubleJumpPowerUp(71 * ss.tile_size, ss.SCREEN_HEIGHT - 7 * ss.tile_size))
        self.power_up_group.add(pu.DoubleJumpPowerUp(90 * ss.tile_size, ss.SCREEN_HEIGHT - 7 * ss.tile_size))


class Level3(Level):
    def __init__(self):
        super(Level3, self).__init__(random.choice(background_list), 91, "level3")
        self.no_of_letter = 10
        self.stars = 35
        self.time = 75

    def make_letters(self):
        self.letter_group.add(letter.Letter(self.letter_list[0], 3 * ss.tile_size,  # tile_size = 200
                                            ss.SCREEN_HEIGHT - 6 * ss.tile_size))  # 1 is the original +3 ground platform+1 bouncing=5 normally, 5
        self.letter_group.add(letter.Letter(self.letter_list[1], 14 * ss.tile_size,
                                            ss.SCREEN_HEIGHT - 8 * ss.tile_size))
        self.letter_group.add(letter.Letter(self.letter_list[2], 20 * ss.tile_size,
                                            ss.SCREEN_HEIGHT - 5 * ss.tile_size))
        self.letter_group.add(letter.MysteryLetter(53 * ss.tile_size,
                                                   ss.SCREEN_HEIGHT - 10 * ss.tile_size))
        self.letter_group.add(letter.Letter(self.letter_list[3], 28 * ss.tile_size,
                                            ss.SCREEN_HEIGHT - 11 * ss.tile_size))
        self.letter_group.add(letter.Letter(self.letter_list[4], 34 * ss.tile_size,
                                            ss.SCREEN_HEIGHT - 5 * ss.tile_size))
        self.letter_group.add(letter.Letter(self.letter_list[5], 59 * ss.tile_size,
                                            ss.SCREEN_HEIGHT - 11 * ss.tile_size))
        self.letter_group.add(letter.Letter(self.letter_list[6], 64 * ss.tile_size,
                                            ss.SCREEN_HEIGHT - 11 * ss.tile_size))
        self.letter_group.add(letter.Letter(self.letter_list[7], 72 * ss.tile_size,
                                            ss.SCREEN_HEIGHT - 5 * ss.tile_size))
        self.letter_group.add(letter.MysteryLetter(79 * ss.tile_size,
                                                   ss.SCREEN_HEIGHT - 13 * ss.tile_size))
        self.letter_group.add(letter.Letter(self.letter_list[8], 82 * ss.tile_size,
                                            ss.SCREEN_HEIGHT - 9 * ss.tile_size))
        self.letter_group.add(letter.Letter(self.letter_list[9], 87 * ss.tile_size,
                                            ss.SCREEN_HEIGHT - 7 * ss.tile_size))

    def make_platforms_objects(self):
        for j in range(1, 3):
            self.platform_group.add(
                po.Platform(0 * ss.tile_size, ss.SCREEN_HEIGHT - j * ss.tile_size, self.tiles, False,
                            (platforms_obstacles_images.base_platform)))
        # # ground row
        self.platform_group.add(po.Platform(0, ss.SCREEN_HEIGHT - 3 * ss.tile_size, self.tiles, False))  # 0+3
        # the upper stuff should be copied

        self.platform_group.add(po.Platform(0 * ss.tile_size, ss.SCREEN_HEIGHT - 4 * ss.tile_size, 8,
                                            False))  # x, y, no_of_tiles, rectangle or curve
        self.platform_group.add(po.Platform(7 * ss.tile_size, ss.SCREEN_HEIGHT - 6 * ss.tile_size, 1, False))
        self.platform_group.add(po.Platform(9 * ss.tile_size, ss.SCREEN_HEIGHT - 8 * ss.tile_size, 1, False))
        self.platform_group.add(po.Platform(11 * ss.tile_size, ss.SCREEN_HEIGHT - 6 * ss.tile_size, 3))
        self.platform_group.add(po.Platform(23 * ss.tile_size, ss.SCREEN_HEIGHT - 7 * ss.tile_size, 2))
        self.platform_group.add(po.Platform(27 * ss.tile_size, ss.SCREEN_HEIGHT - 9 * ss.tile_size, 3))
        self.platform_group.add(po.Platform(32 * ss.tile_size, ss.SCREEN_HEIGHT - 6 * ss.tile_size, 1, False))
        self.platform_group.add(po.Platform(44 * ss.tile_size, ss.SCREEN_HEIGHT - 7 * ss.tile_size, 1, False))
        self.platform_group.add(po.Platform(46 * ss.tile_size, ss.SCREEN_HEIGHT - 9 * ss.tile_size, 1, False))
        self.platform_group.add(po.Platform(48 * ss.tile_size, ss.SCREEN_HEIGHT - 7 * ss.tile_size, 1, False))
        self.platform_group.add(po.Platform(49 * ss.tile_size, ss.SCREEN_HEIGHT - 6 * ss.tile_size, 1, False))
        self.platform_group.add(po.Platform(50 * ss.tile_size, ss.SCREEN_HEIGHT - 5 * ss.tile_size, 1, False))
        self.platform_group.add(po.Platform(52 * ss.tile_size, ss.SCREEN_HEIGHT - 7 * ss.tile_size, 3))
        self.platform_group.add(po.Platform(56 * ss.tile_size, ss.SCREEN_HEIGHT - 9 * ss.tile_size, 3))
        self.platform_group.add(po.Platform(61.5 * ss.tile_size, ss.SCREEN_HEIGHT - 7 * ss.tile_size, 2, False))
        self.platform_group.add(po.Platform(64 * ss.tile_size, ss.SCREEN_HEIGHT - 9 * ss.tile_size, 0))
        self.platform_group.add(po.Platform(66.5 * ss.tile_size, ss.SCREEN_HEIGHT - 7 * ss.tile_size, 2, False))
        self.platform_group.add(po.Platform(69 * ss.tile_size, ss.SCREEN_HEIGHT - 5 * ss.tile_size, 0))
        self.platform_group.add(po.Platform(75 * ss.tile_size, ss.SCREEN_HEIGHT - 5 * ss.tile_size, 0))
        self.platform_group.add(po.Platform(79 * ss.tile_size, ss.SCREEN_HEIGHT - 10 * ss.tile_size, 0))
        self.platform_group.add(po.Platform(82 * ss.tile_size, ss.SCREEN_HEIGHT - 7 * ss.tile_size, 0))
        self.platform_group.add(po.Platform(85 * ss.tile_size, ss.SCREEN_HEIGHT - 5 * ss.tile_size, 4, False))

        self.obstruct_group.add(po.Obstacle(26 * ss.tile_size, ss.SCREEN_HEIGHT - 4 * ss.tile_size,
                                            "spikes", w=ss.tile_size * 2, h=ss.tile_size))
        self.obstruct_group.add(po.Obstacle(12 * ss.tile_size, ss.SCREEN_HEIGHT - 7 * ss.tile_size,
                                            "spikes", w=ss.tile_size * 2, h=ss.tile_size))
        self.obstruct_group.add(po.Obstacle(46 * ss.tile_size, ss.SCREEN_HEIGHT - 4 * ss.tile_size,
                                            "spikes", w=ss.tile_size * 2, h=ss.tile_size))
        self.obstruct_group.add(po.Obstacle(37 * ss.tile_size, ss.SCREEN_HEIGHT - 5 * ss.tile_size,
                                            "snowman", w=ss.tile_size * 2, h=ss.tile_size * 2))
        self.obstruct_group.add(po.Obstacle(43 * ss.tile_size, ss.SCREEN_HEIGHT - 5 * ss.tile_size,
                                            "tree", w=ss.tile_size * 2 / 1.7, h=ss.tile_size * 2))
        self.obstruct_group.add(po.Obstacle(56 * ss.tile_size, ss.SCREEN_HEIGHT - 10 * ss.tile_size,
                                            "spikes", w=ss.tile_size * 2, h=ss.tile_size))
        self.obstruct_group.add(po.Obstacle(61.5 * ss.tile_size, ss.SCREEN_HEIGHT - 8 * ss.tile_size,
                                            "spikes", w=ss.tile_size * 2, h=ss.tile_size))
        self.obstruct_group.add(po.Obstacle(66.5 * ss.tile_size, ss.SCREEN_HEIGHT - 8 * ss.tile_size,
                                            "spikes", w=ss.tile_size * 2, h=ss.tile_size))
        self.obstruct_group.add(po.Obstacle(71 * ss.tile_size, ss.SCREEN_HEIGHT - 4 * ss.tile_size,
                                            "spikes", w=ss.tile_size * 2, h=ss.tile_size))
        self.obstruct_group.add(po.Obstacle(73 * ss.tile_size, ss.SCREEN_HEIGHT - 4 * ss.tile_size,
                                            "spikes", w=ss.tile_size * 2, h=ss.tile_size))
        self.obstruct_group.add(po.Obstacle(85 * ss.tile_size, ss.SCREEN_HEIGHT - 7 * ss.tile_size,
                                            "snowman", w=ss.tile_size * 2, h=ss.tile_size * 2))

    def make_power_ups(self):
        # self.power_up_group.add(pu.PowerUp(17 * ss.tile_size, ss.SCREEN_HEIGHT - 4 * ss.tile_size))
        self.power_up_group.add(pu.DoubleJumpPowerUp(39 * ss.tile_size, ss.SCREEN_HEIGHT - 4 * ss.tile_size))
        # self.power_up_group.add(pu.PowerUp(69 * ss.tile_size, ss.SCREEN_HEIGHT - 6 * ss.tile_size))


class Level4(Level):
    def __init__(self):
        super(Level4, self).__init__(random.choice(background_list), 119, "level4")
        self.no_of_letter = 13
        self.stars = 40
        self.time = 75

    def make_letters(self):
        self.letter_group.add(letter.Letter(self.letter_list[0], 3 * ss.tile_size,  # tile_size = 200
                                            ss.SCREEN_HEIGHT - 6 * ss.tile_size))  # 1 is the original +3 ground platform+1 bouncing=5 normally, 5
        self.letter_group.add(letter.Letter(self.letter_list[1], 18 * ss.tile_size,
                                            ss.SCREEN_HEIGHT - 9 * ss.tile_size))

        self.letter_group.add(letter.Letter(self.letter_list[2], 37 * ss.tile_size,
                                            ss.SCREEN_HEIGHT - 8 * ss.tile_size))
        self.letter_group.add(letter.Letter(self.letter_list[3], 46 * ss.tile_size,
                                            ss.SCREEN_HEIGHT - 8 * ss.tile_size))
        self.letter_group.add(letter.Letter(self.letter_list[4], 54 * ss.tile_size,
                                            ss.SCREEN_HEIGHT - 9 * ss.tile_size))

        self.letter_group.add(letter.MysteryLetter(57 * ss.tile_size,
                                                   ss.SCREEN_HEIGHT - 11.5 * ss.tile_size))

        self.letter_group.add(letter.Letter(self.letter_list[5], 66 * ss.tile_size,
                                            ss.SCREEN_HEIGHT - 12 * ss.tile_size))
        self.letter_group.add(letter.Letter(self.letter_list[6], 70 * ss.tile_size,
                                            ss.SCREEN_HEIGHT - 10 * ss.tile_size))
        self.letter_group.add(letter.Letter(self.letter_list[7], 76 * ss.tile_size,
                                            ss.SCREEN_HEIGHT - 5 * ss.tile_size))
        self.letter_group.add(letter.Letter(self.letter_list[8], 79 * ss.tile_size,
                                            ss.SCREEN_HEIGHT - 8 * ss.tile_size))

        self.letter_group.add(letter.MysteryLetter(83 * ss.tile_size,
                                                   ss.SCREEN_HEIGHT - 12.5 * ss.tile_size))

        self.letter_group.add(letter.Letter(self.letter_list[9], 86 * ss.tile_size,
                                            ss.SCREEN_HEIGHT - 9 * ss.tile_size))
        self.letter_group.add(letter.Letter(self.letter_list[10], 96 * ss.tile_size,
                                            ss.SCREEN_HEIGHT - 11 * ss.tile_size))
        self.letter_group.add(letter.Letter(self.letter_list[11], 103 * ss.tile_size,
                                            ss.SCREEN_HEIGHT - 5 * ss.tile_size))
        self.letter_group.add(letter.Letter(self.letter_list[12], 109 * ss.tile_size,
                                            ss.SCREEN_HEIGHT - 5 * ss.tile_size))

    def make_platforms_objects(self):
        for j in range(1, 3):
            self.platform_group.add(po.Platform(0 * ss.tile_size, ss.SCREEN_HEIGHT - j * ss.tile_size, 119, False,
                                                (platforms_obstacles_images.base_platform)))
        # # ground row
        self.platform_group.add(po.Platform(0, ss.SCREEN_HEIGHT - 3 * ss.tile_size, 119, False))  # 0+3
        # the upper stuff should be copied

        self.platform_group.add(po.Platform(0 * ss.tile_size, ss.SCREEN_HEIGHT - 4 * ss.tile_size, 8, False))
        self.platform_group.add(po.Platform(18 * ss.tile_size, ss.SCREEN_HEIGHT - 7 * ss.tile_size, 0))
        self.platform_group.add(po.Platform(21 * ss.tile_size, ss.SCREEN_HEIGHT - 9 * ss.tile_size, 1, False))
        self.platform_group.add(po.Platform(22 * ss.tile_size, ss.SCREEN_HEIGHT - 10 * ss.tile_size, 1, False))
        self.platform_group.add(po.Platform(24 * ss.tile_size, ss.SCREEN_HEIGHT - 8 * ss.tile_size, 1))
        self.platform_group.add(po.Platform(28 * ss.tile_size, ss.SCREEN_HEIGHT - 6 * ss.tile_size, 1, False))
        self.platform_group.add(po.Platform(29 * ss.tile_size, ss.SCREEN_HEIGHT - 5 * ss.tile_size, 1, False))
        self.platform_group.add(po.Platform(30 * ss.tile_size, ss.SCREEN_HEIGHT - 4 * ss.tile_size, 1, False))
        self.platform_group.add(po.Platform(32 * ss.tile_size, ss.SCREEN_HEIGHT - 6 * ss.tile_size, 5))
        self.platform_group.add(po.Platform(40 * ss.tile_size, ss.SCREEN_HEIGHT - 8 * ss.tile_size, 3))
        self.platform_group.add(po.Platform(46 * ss.tile_size, ss.SCREEN_HEIGHT - 6 * ss.tile_size, 0))
        self.platform_group.add(po.Platform(54 * ss.tile_size, ss.SCREEN_HEIGHT - 7 * ss.tile_size, 0))
        self.platform_group.add(po.Platform(57 * ss.tile_size, ss.SCREEN_HEIGHT - 9 * ss.tile_size, 0))
        self.platform_group.add(po.Platform(60 * ss.tile_size, ss.SCREEN_HEIGHT - 7 * ss.tile_size, 1, False))
        self.platform_group.add(po.Platform(61 * ss.tile_size, ss.SCREEN_HEIGHT - 6 * ss.tile_size, 1, False))
        self.platform_group.add(po.Platform(63 * ss.tile_size, ss.SCREEN_HEIGHT - 8 * ss.tile_size, 1, False))
        self.platform_group.add(po.Platform(64 * ss.tile_size, ss.SCREEN_HEIGHT - 9 * ss.tile_size, 1, False))
        self.platform_group.add(po.Platform(65 * ss.tile_size, ss.SCREEN_HEIGHT - 10 * ss.tile_size, 1))
        self.platform_group.add(po.Platform(69 * ss.tile_size, ss.SCREEN_HEIGHT - 8 * ss.tile_size, 1))
        self.platform_group.add(po.Platform(73 * ss.tile_size, ss.SCREEN_HEIGHT - 6 * ss.tile_size, 0))
        self.platform_group.add(po.Platform(79 * ss.tile_size, ss.SCREEN_HEIGHT - 6 * ss.tile_size, 0))
        self.platform_group.add(po.Platform(83 * ss.tile_size, ss.SCREEN_HEIGHT - 10 * ss.tile_size, 0))
        self.platform_group.add(po.Platform(86 * ss.tile_size, ss.SCREEN_HEIGHT - 7 * ss.tile_size, 0))
        self.platform_group.add(po.Platform(89 * ss.tile_size, ss.SCREEN_HEIGHT - 9 * ss.tile_size, 7))
        self.platform_group.add(po.Platform(99 * ss.tile_size, ss.SCREEN_HEIGHT - 7 * ss.tile_size, 1, False))
        self.platform_group.add(po.Platform(100 * ss.tile_size, ss.SCREEN_HEIGHT - 6 * ss.tile_size, 1, False))
        self.platform_group.add(po.Platform(101 * ss.tile_size, ss.SCREEN_HEIGHT - 5 * ss.tile_size, 1, False))
        self.platform_group.add(po.Platform(106 * ss.tile_size, ss.SCREEN_HEIGHT - 6 * ss.tile_size, 0))
        self.platform_group.add(po.Platform(114 * ss.tile_size, ss.SCREEN_HEIGHT - 7 * ss.tile_size, 0))
        self.platform_group.add(po.Platform(117 * ss.tile_size, ss.SCREEN_HEIGHT - 5 * ss.tile_size, 0))

        # Added platforms for jump test

        self.obstruct_group.add(po.Obstacle(32 * ss.tile_size, ss.SCREEN_HEIGHT - 4 * ss.tile_size,
                                            "spikes", w=ss.tile_size * 2, h=ss.tile_size))

        self.obstruct_group.add(po.Obstacle(62 * ss.tile_size, ss.SCREEN_HEIGHT - 4 * ss.tile_size,
                                            "spikes", w=ss.tile_size * 2, h=ss.tile_size))

        self.obstruct_group.add(po.Obstacle(9 * ss.tile_size, ss.SCREEN_HEIGHT - 5 * ss.tile_size,
                                            "snowman", w=ss.tile_size * 2, h=ss.tile_size * 2))
        self.obstruct_group.add(po.Obstacle(34 * ss.tile_size, ss.SCREEN_HEIGHT - 8 * ss.tile_size,
                                            "snowman", w=ss.tile_size * 2, h=ss.tile_size * 2))
        self.obstruct_group.add(po.Obstacle(51 * ss.tile_size, ss.SCREEN_HEIGHT - 5 * ss.tile_size,
                                            "snowman", w=ss.tile_size * 2, h=ss.tile_size * 2))
        self.obstruct_group.add(po.Obstacle(90 * ss.tile_size, ss.SCREEN_HEIGHT - 11 * ss.tile_size,
                                            "snowman", w=ss.tile_size * 2, h=ss.tile_size * 2))

        self.obstruct_group.add(po.Obstacle(16 * ss.tile_size, ss.SCREEN_HEIGHT - 5 * ss.tile_size,
                                            "tree", w=ss.tile_size * 2 / 1.7, h=ss.tile_size * 2))
        self.obstruct_group.add(po.Obstacle(41 * ss.tile_size, ss.SCREEN_HEIGHT - 10 * ss.tile_size,
                                            "tree", w=ss.tile_size * 2 / 1.7, h=ss.tile_size * 2))
        self.obstruct_group.add(po.Obstacle(94 * ss.tile_size, ss.SCREEN_HEIGHT - 11 * ss.tile_size,
                                            "tree", w=ss.tile_size * 2 / 1.7, h=ss.tile_size * 2))
        self.obstruct_group.add(po.Obstacle(112 * ss.tile_size, ss.SCREEN_HEIGHT - 5 * ss.tile_size,
                                            "tree", w=ss.tile_size * 2 / 1.7, h=ss.tile_size * 2))

    def make_power_ups(self):
        self.power_up_group.add(pu.DoubleJumpPowerUp(13 * ss.tile_size, ss.SCREEN_HEIGHT - 4 * ss.tile_size))
        # self.power_up_group.add(pu.PowerUp(43 * ss.tile_size, ss.SCREEN_HEIGHT - 9 * ss.tile_size))
        # self.power_up_group.add(pu.PowerUp(73 * ss.tile_size, ss.SCREEN_HEIGHT - 7 * ss.tile_size))
        # self.power_up_group.add(pu.PowerUp(106 * ss.tile_size, ss.SCREEN_HEIGHT - 7 * ss.tile_size))


class Level5(Level):
    def __init__(self):
        super(Level5, self).__init__(random.choice(background_list), 175, "level5")
        self.no_of_letter = 17
        self.stars = 40
        self.time = 90

    def make_letters(self):
        self.letter_group.add(letter.Letter(self.letter_list[0], 2 * ss.tile_size,
                                            ss.SCREEN_HEIGHT - 5 * ss.tile_size))
        self.letter_group.add(letter.Letter(self.letter_list[1], 9 * ss.tile_size,
                                            ss.SCREEN_HEIGHT - 9 * ss.tile_size))
        self.letter_group.add(letter.Letter(self.letter_list[2], 22 * ss.tile_size,
                                            ss.SCREEN_HEIGHT - 9 * ss.tile_size))

        self.letter_group.add(letter.MysteryLetter(28 * ss.tile_size,
                                                   ss.SCREEN_HEIGHT - 9.5 * ss.tile_size))

        self.letter_group.add(letter.Letter(self.letter_list[3], 35 * ss.tile_size,
                                            ss.SCREEN_HEIGHT - 5 * ss.tile_size))
        self.letter_group.add(letter.Letter(self.letter_list[4], 53 * ss.tile_size,
                                            ss.SCREEN_HEIGHT - 5 * ss.tile_size))
        self.letter_group.add(letter.Letter(self.letter_list[5], 60 * ss.tile_size,
                                            ss.SCREEN_HEIGHT - 5 * ss.tile_size))
        self.letter_group.add(letter.Letter(self.letter_list[6], 70 * ss.tile_size,
                                            ss.SCREEN_HEIGHT - 7 * ss.tile_size))

        self.letter_group.add(letter.MysteryLetter(78 * ss.tile_size,
                                                   ss.SCREEN_HEIGHT - 11.5 * ss.tile_size))

        self.letter_group.add(letter.Letter(self.letter_list[7], 87 * ss.tile_size,
                                            ss.SCREEN_HEIGHT - 9 * ss.tile_size))
        self.letter_group.add(letter.Letter(self.letter_list[8], 100 * ss.tile_size,
                                            ss.SCREEN_HEIGHT - 11 * ss.tile_size))
        self.letter_group.add(letter.Letter(self.letter_list[9], 108 * ss.tile_size,
                                            ss.SCREEN_HEIGHT - 7 * ss.tile_size))

        self.letter_group.add(letter.Letter(self.letter_list[10], 118 * ss.tile_size,
                                            ss.SCREEN_HEIGHT - 9 * ss.tile_size))
        self.letter_group.add(letter.Letter(self.letter_list[11], 131 * ss.tile_size,
                                            ss.SCREEN_HEIGHT - 8 * ss.tile_size))

        self.letter_group.add(letter.MysteryLetter(136 * ss.tile_size,
                                                   ss.SCREEN_HEIGHT - 11.5 * ss.tile_size))

        self.letter_group.add(letter.Letter(self.letter_list[12], 139 * ss.tile_size,
                                            ss.SCREEN_HEIGHT - 8 * ss.tile_size))
        self.letter_group.add(letter.Letter(self.letter_list[13], 151 * ss.tile_size,
                                            ss.SCREEN_HEIGHT - 7 * ss.tile_size))
        self.letter_group.add(letter.Letter(self.letter_list[14], 157 * ss.tile_size,
                                            ss.SCREEN_HEIGHT - 5 * ss.tile_size))

        self.letter_group.add(letter.MysteryLetter(163 * ss.tile_size,
                                                   ss.SCREEN_HEIGHT - 9.5 * ss.tile_size))

        self.letter_group.add(letter.Letter(self.letter_list[15], 167 * ss.tile_size,
                                            ss.SCREEN_HEIGHT - 8 * ss.tile_size))
        self.letter_group.add(letter.Letter(self.letter_list[16], 173 * ss.tile_size,
                                            ss.SCREEN_HEIGHT - 5 * ss.tile_size))

    def make_platforms_objects(self):
        for j in range(1, 3):
            self.platform_group.add(
                po.Platform(0 * ss.tile_size, ss.SCREEN_HEIGHT - j * ss.tile_size, self.tiles, False,
                            (platforms_obstacles_images.base_platform)))
        # # ground row
        self.platform_group.add(po.Platform(0, ss.SCREEN_HEIGHT - 3 * ss.tile_size, self.tiles, False))  # 0+3
        # the upper stuff should be copied

        self.platform_group.add(po.Platform(6 * ss.tile_size, ss.SCREEN_HEIGHT - 5 * ss.tile_size,
                                            0))  # x, y, no_of_tiles, rectangle or curve
        self.platform_group.add(po.Platform(9 * ss.tile_size, ss.SCREEN_HEIGHT - 7 * ss.tile_size, 0))
        self.platform_group.add(po.Platform(12 * ss.tile_size, ss.SCREEN_HEIGHT - 9 * ss.tile_size, 0))
        self.platform_group.add(po.Platform(15 * ss.tile_size, ss.SCREEN_HEIGHT - 7 * ss.tile_size, 2, False))
        self.platform_group.add(po.Platform(17 * ss.tile_size, ss.SCREEN_HEIGHT - 6 * ss.tile_size, 2, False))
        self.platform_group.add(po.Platform(19 * ss.tile_size, ss.SCREEN_HEIGHT - 5 * ss.tile_size, 2, False))
        self.platform_group.add(po.Platform(22 * ss.tile_size, ss.SCREEN_HEIGHT - 7 * ss.tile_size, 8, False))
        self.platform_group.add(po.Platform(31 * ss.tile_size, ss.SCREEN_HEIGHT - 5 * ss.tile_size, 0))
        self.platform_group.add(po.Platform(41 * ss.tile_size, ss.SCREEN_HEIGHT - 7 * ss.tile_size, 0))
        self.platform_group.add(po.Platform(44 * ss.tile_size, ss.SCREEN_HEIGHT - 9 * ss.tile_size, 0))
        self.platform_group.add(po.Platform(47 * ss.tile_size, ss.SCREEN_HEIGHT - 7 * ss.tile_size, 1, False))
        self.platform_group.add(po.Platform(48 * ss.tile_size, ss.SCREEN_HEIGHT - 6 * ss.tile_size, 1, False))
        self.platform_group.add(po.Platform(49 * ss.tile_size, ss.SCREEN_HEIGHT - 5 * ss.tile_size, 3, False))
        self.platform_group.add(po.Platform(64 * ss.tile_size, ss.SCREEN_HEIGHT - 5 * ss.tile_size, 9, False))
        self.platform_group.add(po.Platform(75 * ss.tile_size, ss.SCREEN_HEIGHT - 9 * ss.tile_size, 5, False))
        self.platform_group.add(po.Platform(82 * ss.tile_size, ss.SCREEN_HEIGHT - 6 * ss.tile_size, 1, False))
        self.platform_group.add(po.Platform(83 * ss.tile_size, ss.SCREEN_HEIGHT - 7 * ss.tile_size, 1, False))
        self.platform_group.add(po.Platform(84 * ss.tile_size, ss.SCREEN_HEIGHT - 8 * ss.tile_size, 1, False))
        self.platform_group.add(po.Platform(86 * ss.tile_size, ss.SCREEN_HEIGHT - 7 * ss.tile_size, 3, False))
        self.platform_group.add(po.Platform(89 * ss.tile_size, ss.SCREEN_HEIGHT - 6 * ss.tile_size, 1, False))
        self.platform_group.add(po.Platform(90 * ss.tile_size, ss.SCREEN_HEIGHT - 5 * ss.tile_size, 1, False))
        self.platform_group.add(po.Platform(92 * ss.tile_size, ss.SCREEN_HEIGHT - 7 * ss.tile_size, 2))
        self.platform_group.add(po.Platform(97 * ss.tile_size, ss.SCREEN_HEIGHT - 9 * ss.tile_size, 6, False))
        self.platform_group.add(po.Platform(103 * ss.tile_size, ss.SCREEN_HEIGHT - 7 * ss.tile_size, 1))
        self.platform_group.add(po.Platform(108 * ss.tile_size, ss.SCREEN_HEIGHT - 5 * ss.tile_size, 2, False))
        self.platform_group.add(po.Platform(117 * ss.tile_size, ss.SCREEN_HEIGHT - 7 * ss.tile_size, 1))
        self.platform_group.add(po.Platform(121 * ss.tile_size, ss.SCREEN_HEIGHT - 9 * ss.tile_size, 2, False))
        self.platform_group.add(po.Platform(124 * ss.tile_size, ss.SCREEN_HEIGHT - 7 * ss.tile_size, 3, False))
        self.platform_group.add(po.Platform(127 * ss.tile_size, ss.SCREEN_HEIGHT - 6 * ss.tile_size, 1, False))
        self.platform_group.add(po.Platform(128 * ss.tile_size, ss.SCREEN_HEIGHT - 5 * ss.tile_size, 1, False))
        self.platform_group.add(po.Platform(129 * ss.tile_size, ss.SCREEN_HEIGHT - 4 * ss.tile_size, 1, False))
        self.platform_group.add(po.Platform(131 * ss.tile_size, ss.SCREEN_HEIGHT - 6 * ss.tile_size, 2, False))
        self.platform_group.add(po.Platform(135 * ss.tile_size, ss.SCREEN_HEIGHT - 9 * ss.tile_size, 3, False))
        self.platform_group.add(po.Platform(139 * ss.tile_size, ss.SCREEN_HEIGHT - 6 * ss.tile_size, 0))
        self.platform_group.add(po.Platform(142 * ss.tile_size, ss.SCREEN_HEIGHT - 5 * ss.tile_size, 1))
        self.platform_group.add(po.Platform(146 * ss.tile_size, ss.SCREEN_HEIGHT - 7 * ss.tile_size, 1))
        self.platform_group.add(po.Platform(150 * ss.tile_size, ss.SCREEN_HEIGHT - 5 * ss.tile_size, 1))
        self.platform_group.add(po.Platform(160 * ss.tile_size, ss.SCREEN_HEIGHT - 7 * ss.tile_size, 6, False))
        self.platform_group.add(po.Platform(167 * ss.tile_size, ss.SCREEN_HEIGHT - 6 * ss.tile_size, 0))
        self.platform_group.add(po.Platform(170 * ss.tile_size, ss.SCREEN_HEIGHT - 5 * ss.tile_size, 0))

        self.obstruct_group.add(po.Obstacle(9 * ss.tile_size, ss.SCREEN_HEIGHT - 4 * ss.tile_size,
                                            "spikes", w=ss.tile_size * 2, h=ss.tile_size))

        self.obstruct_group.add(po.Obstacle(21 * ss.tile_size, ss.SCREEN_HEIGHT - 4 * ss.tile_size,
                                            "spikes", w=ss.tile_size * 2, h=ss.tile_size))
        self.obstruct_group.add(po.Obstacle(29 * ss.tile_size, ss.SCREEN_HEIGHT - 4 * ss.tile_size,
                                            "spikes", w=ss.tile_size * 2, h=ss.tile_size))
        self.obstruct_group.add(po.Obstacle(74 * ss.tile_size, ss.SCREEN_HEIGHT - 4 * ss.tile_size,
                                            "spikes", w=ss.tile_size * 2, h=ss.tile_size))
        self.obstruct_group.add(po.Obstacle(91 * ss.tile_size, ss.SCREEN_HEIGHT - 4 * ss.tile_size,
                                            "spikes", w=ss.tile_size * 2, h=ss.tile_size))
        self.obstruct_group.add(po.Obstacle(166 * ss.tile_size, ss.SCREEN_HEIGHT - 4 * ss.tile_size,
                                            "spikes", w=ss.tile_size * 2, h=ss.tile_size))

        self.obstruct_group.add(po.Obstacle(25 * ss.tile_size, ss.SCREEN_HEIGHT - 9 * ss.tile_size,
                                            "snowman", w=ss.tile_size * 2, h=ss.tile_size * 2))
        self.obstruct_group.add(po.Obstacle(38 * ss.tile_size, ss.SCREEN_HEIGHT - 5 * ss.tile_size,
                                            "snowman", w=ss.tile_size * 2, h=ss.tile_size * 2))
        self.obstruct_group.add(po.Obstacle(68 * ss.tile_size, ss.SCREEN_HEIGHT - 7 * ss.tile_size,
                                            "snowman", w=ss.tile_size * 2, h=ss.tile_size * 2))
        self.obstruct_group.add(po.Obstacle(98 * ss.tile_size, ss.SCREEN_HEIGHT - 11 * ss.tile_size,
                                            "snowman", w=ss.tile_size * 2, h=ss.tile_size * 2))
        self.obstruct_group.add(po.Obstacle(104 * ss.tile_size, ss.SCREEN_HEIGHT - 9 * ss.tile_size,
                                            "snowman", w=ss.tile_size * 2, h=ss.tile_size * 2))
        self.obstruct_group.add(po.Obstacle(154 * ss.tile_size, ss.SCREEN_HEIGHT - 5 * ss.tile_size,
                                            "snowman", w=ss.tile_size * 2, h=ss.tile_size * 2))
        self.obstruct_group.add(po.Obstacle(160 * ss.tile_size, ss.SCREEN_HEIGHT - 9 * ss.tile_size,
                                            "snowman", w=ss.tile_size * 2, h=ss.tile_size * 2))

        self.obstruct_group.add(po.Obstacle(57 * ss.tile_size, ss.SCREEN_HEIGHT - 5 * ss.tile_size,
                                            "tree", w=ss.tile_size * 2 / 1.7, h=ss.tile_size * 2))
        self.obstruct_group.add(po.Obstacle(116 * ss.tile_size, ss.SCREEN_HEIGHT - 5 * ss.tile_size,
                                            "tree", w=ss.tile_size * 2 / 1.7, h=ss.tile_size * 2))

    def make_power_ups(self):
        self.power_up_group.add(pu.DoubleJumpPowerUp(31 * ss.tile_size, ss.SCREEN_HEIGHT - 6 * ss.tile_size))
        # self.power_up_group.add(pu.PowerUp(50 * ss.tile_size, ss.SCREEN_HEIGHT - 6 * ss.tile_size))
        self.power_up_group.add(pu.DoubleJumpPowerUp(112 * ss.tile_size, ss.SCREEN_HEIGHT - 4 * ss.tile_size))
        self.power_up_group.add(pu.DoubleJumpPowerUp(156 * ss.tile_size, ss.SCREEN_HEIGHT - 4 * ss.tile_size))


level1 = Level1()
level2 = Level2()
level3 = Level3()
level4 = Level4()
level5 = Level5()
level_list = [level1, level2, level3, level4, level5]
