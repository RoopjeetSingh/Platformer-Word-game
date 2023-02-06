import time
import pygame
import screen_size as ss
from decode_file import decode_file
import extra_images


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(PowerUp, self).__init__()
        self.distance = None
        self.end_pos = (0, 0)
        self.image1 = pygame.image.load(decode_file(extra_images.power_up)).convert_alpha()
        self.image1 = pygame.transform.scale(self.image1, (ss.tile_size, ss.tile_size))
        self.image2 = self.image1.copy()
        brighten = 255
        self.image2.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_ADD)
        self.image = self.image1
        self.rect = self.image.get_rect(topleft=(x, y))
        self.pos = [x, y]
        self.start_y = y
        self.num = 0
        self.gravity = 0
        self.collecting_animation = False
        self.brighten = True
        self.num_collect_anim = 0
        self.start = None
        self.start_track = None
        self.green_rect = pygame.Rect((0, 0, ss.tile_size, ss.tile_size/2.5))
        self.red_rect = pygame.Rect((0, 0, 0, ss.tile_size/2.5))
        self.green_pos = [0, 0]
        self.red_pos = [0, 0]
        self.times = 0
        self.first_time = True

    def bounce_brighten(self):
        if self.brighten:
            # produces the brightening effect
            if self.image == self.image1 and self.num >= 30:
                self.image = self.image2
                self.num = 0
            elif self.image == self.image2 and self.num >= 30:
                self.image = self.image1
                self.num = 0
            self.num += 1

            # produces the going up effect
            self.gravity -= 0.4
            self.pos[1] -= self.gravity + 8
            self.rect.y = round(self.pos[1])

            if self.start_y <= self.rect.y:
                self.rect.y = self.start_y
                self.gravity = 0

    def collect_self(self, player, level):
        if self.collecting_animation:
            if self.num_collect_anim == 0:
                level.power_up_group.remove(self)
                self.image = self.image1
                self.brighten = False
                self.end_pos = (
                    (ss.SCREEN_WIDTH - ((len(player.power_up_lis) - 1) * (ss.tile_size + ss.tile_size/2.5))
                     - ss.tile_size/2.5 - self.rect.w, ss.tile_size/2.5),
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
                self.start = time.time()
                self.start_track = self.start
            self.num_collect_anim += 1
            self.rect = self.rect.copy()

    def time_bar(self, screen, player, level):
        if isinstance(self.start, float):
            player.double_jump_power_up = True
            if self.first_time:
                self.green_rect.topleft = (self.rect.x, self.rect.bottom + ss.tile_size/2.5)
                self.red_rect.topleft = (self.rect.right, self.rect.bottom + ss.tile_size/2.5)
                self.green_pos = [self.green_rect.x, self.green_rect.w]
                self.red_pos = [self.red_rect.x, self.red_rect.w]
                self.first_time = False

            if self.times == 5:
                player.power_up_lis.remove(self)
                level.power_up_group.remove(self)
                player.double_jump_power_up = False
            elif time.time() - self.start >= 0.25:
                self.green_pos[1] -= ss.tile_size / 20
                self.red_pos[0] -= ss.tile_size / 20
                self.red_pos[1] += ss.tile_size / 20
                self.red_rect.x = round(self.red_pos[0])
                self.red_rect.w = round(self.red_pos[1])
                self.green_rect.w = round(self.green_pos[1])
                self.start = time.time()
            if time.time() - self.start_track >= 1:
                self.times += 1
                self.start_track = time.time()
            pygame.draw.rect(screen, (255, 0, 0), self.red_rect)
            pygame.draw.rect(screen, (0, 255, 0), self.green_rect)
