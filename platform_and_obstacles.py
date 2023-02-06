import pygame
import cv2
import numpy as np
import screen_size as ss
from decode_file import decode_file
import images_store 
import smaller_store
import other_small_images


class Platform(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, num_inside: int = 0, start: bool = True,
                 img="images/platform/platform_sprites_(27).png", w=0, h=0,
                 set_colorkey: tuple[int, int, int] = None, new_img=False):
        super(Platform, self).__init__()
        if not new_img:
            image_lis = []
            if start:
                image_lis.append(cv2.imread("images/platform/platform_sprites_(3).png"))
            for a in range(num_inside):
                image_lis.append(cv2.imread(img))
            if start:
                image_lis.append(cv2.imread("images/platform/platform_sprites_(26).png"))
            image = np.concatenate(image_lis, axis=1)
            self.image = pygame.image.frombuffer(image.tostring(), image.shape[1::-1],
                                                 "RGB").convert_alpha()
            if start:
                self.image = pygame.transform.scale(self.image, (ss.tile_size * num_inside + ss.tile_size*2, ss.tile_size))
            else:
                self.image = pygame.transform.scale(self.image, (ss.tile_size * num_inside, ss.tile_size))
            self.image.set_colorkey((0, 0, 0))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
        else:
            self.image = pygame.image.load(img).convert_alpha()
            if w and h:
                self.image = pygame.transform.scale(self.image, (w, h))
            self.rect = self.image.get_rect(topleft=(x, y))
            self.set_colorkey = set_colorkey
            if set_colorkey:
                self.image.set_colorkey(set_colorkey)

        self.mask = pygame.mask.from_surface(self.image)


class Obstacle(Platform):
    def __init__(self, x: int, y: int, img_type: str, w=0, h=0, set_colorkey: tuple[int, int, int] = (0, 0, 0)):
        if img_type == "snowman":
            img = "images/platform/platform_sprites_(17).png"
        # spikes is causing huge error
        elif img_type == "spikes":
            img = "images/platform/spikes_2.png"
        else:
            img = "images/platform/platform_sprites_(8).png"

        self.img_type = img_type

        super(Obstacle, self).__init__(x, y, img=img, w=w, h=h,
                                       set_colorkey=set_colorkey, new_img=True)
        self.dead_images = []
        if img_type == "snowman":
            for i in range(2, 6):
                img = pygame.image.load(f"images/platform/platform_sprites_(17) ({i}).png").convert_alpha()
                img = pygame.transform.scale(img, (
                    self.image.get_width(), self.image.get_width() / img.get_width() * img.get_height()))
                if self.set_colorkey:
                    img.set_colorkey(self.set_colorkey)
                self.dead_images.append(img)
        self.death_index = 0
        self.angle = 0
        self.image_copy = self.image.copy()

    def die(self, process: str):
        if self.img_type == "snowman":
            self.image = self.dead_images[int(self.death_index)]
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
            if not self.death_index + 0.08 >= len(self.dead_images):
                self.death_index += 0.08  # image will change around every 3 times the function is called
        elif self.img_type == "tree":
            if not self.angle < -90:
                if self.angle % 30 == 0:
                    if process == "right":
                        self.image = pygame.transform.rotate(self.image_copy, self.angle)
                    else:
                        self.image = pygame.transform.rotate(self.image_copy, -self.angle)
                    self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
                    self.image.set_colorkey(self.set_colorkey)
                self.angle -= 7.5
