import pygame
import Level
import screen_size as ss
import letter
import numpy


def grayscale(img):
    arr = pygame.surfarray.array3d(img)
    # luminosity filter
    avgs = [[(r * 0.298 + g * 0.587 + b * 0.114) for (r, g, b) in col] for col in arr]
    arr = numpy.array([[[avg, avg, avg] for avg in col] for col in avgs])
    return pygame.surfarray.make_surface(arr)


# Set up the game window

# Set up the player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, skin: str):
        super().__init__()
        match skin:
            case "santa":
                run_max_index = 12
                death_max_index = 16
                run = "Run"
                fall = 2
            case "boy":
                run_max_index = 8
                death_max_index = 10
                run = "Run"
                fall = 3.5
            case "female_zombie" | "male_zombie":
                run_max_index = 10
                death_max_index = 12
                run = "Walk"
                fall = 3
            case _:
                raise AttributeError("Invalid skin type " + skin)

        if skin == "female_zombie":
            fall = 1.8
        self.idle_image = pygame.image.load(rf"images/{skin.capitalize()}/Idle (1).png").convert()
        height = 75
        self.idle_image = pygame.transform.scale(self.idle_image, (
            self.idle_image.get_width() * height / self.idle_image.get_height(), height))
        alpha = (0, 0, 0)
        self.idle_image.set_colorkey(alpha)
        self.idle_image_flipped = pygame.transform.flip(self.idle_image, True, False)
        self.idle_image_flipped.set_colorkey(alpha)
        self.right_images = []
        self.left_images = []
        for i in range(1, run_max_index):
            img = pygame.image.load(fr"images/{skin.title()}/{run} ({i}).png").convert()
            img = pygame.transform.scale(img, (
                img.get_width() * height / img.get_height(), height))
            img.set_colorkey(alpha)
            self.right_images.append(img)
            img_left = pygame.transform.flip(img, True, False)
            img_left.set_colorkey(alpha)
            self.left_images.append(img_left)

        self.death_images = []
        for i in range(1, death_max_index):
            img = pygame.image.load(fr"images/{skin.title()}/Dead ({i}).png").convert()
            img = pygame.transform.scale(img, (
                img.get_width() * height / img.get_height(), height))
            img.set_colorkey(alpha)
            self.death_images.append(img)
            height -= fall

        self.image = self.idle_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity_y = 0
        self.index = 0
        self.index_dead = 0
        self.jumping = False
        self.on_ground = True
        self.double_jump_power_up = False
        self.old_list = "right"
        self.move_speed = 7
        self.num_jumps = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.kill_player = False
        self.obstacle_collided_with = None
        self.letter_lis = []
        self.mystery_letter_lis = []
        self.power_up_lis = []
        self.process = "right"
        self.start_pos = 6 * ss.tile_size
        self.color = True
        self.color_num = 0
        self.current_image = None

    def update_player(self, screen, current_level, pressed):
        self.kill_self()
        self.jump(current_level)
        self.gravity(current_level)
        self.collect_letter(current_level)
        self.collect_power_up(current_level)

        if not self.kill_player:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.move_right(current_level, "right")
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.move_right(current_level, "left")
            else:
                self.move_right(current_level, "")

            if keys[pygame.K_UP] or keys[pygame.K_SPACE] or keys[pygame.K_w]:
                if self.on_ground or pressed:
                    self.jumping = True
                    pressed = True
            else:
                pressed = False
        for i in self.letter_lis:
            i.collect_self(self, current_level)
            screen.blit(i.image, i.rect)
        for i in self.mystery_letter_lis:
            i.collect_self(self, current_level)
            screen.blit(i.image, i.rect)
        for i in self.power_up_lis:
            i.collect_self(self, current_level)
            screen.blit(i.image, i.rect)
            i.time_bar(screen, self, current_level)
        return pressed

    def move_right(self, level: Level.Level, direction: str = ""):
        if direction == "right":
            self.image = self.right_images[int(self.index)]
            # self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
            self.rect.x += self.move_speed  # to check if after increasing 5 pixels, object touches it
            if not self.obstruct_platforms(level, "right"):
                if level.start - self.move_speed > ss.SCREEN_WIDTH - level.width and not self.rect.x <= self.start_pos:
                    level.start -= self.move_speed  # moves background
                    for p in level.platform_group:  # moves platforms
                        p.rect.x -= self.move_speed
                    for p in level.obstruct_group:  # moves obstacles like snowman
                        p.rect.x -= self.move_speed
                    for a in level.letter_group:
                        a.rect_original.x -= self.move_speed
                    for p in level.power_up_group:  # moves obstacles like snowman
                        p.rect.x -= self.move_speed
                else:
                    # if self.rect.x + self.move_speed <= ss.SCREEN_WIDTH - self.image.get_width():
                    self.rect.x += self.move_speed
            self.rect.x -= self.move_speed
            self.obstruct_obstacles(level)
            self.old_list = "right"

        elif direction == "left":
            self.image = self.left_images[int(self.index)]
            # self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
            self.rect.x -= self.move_speed  # to check if after decreasing 5 pixels, object touches it
            if not self.obstruct_platforms(level, "left"):
                if level.start + self.move_speed <= 0 and not self.rect.x >= self.start_pos:
                    level.start += self.move_speed  # moves background
                    for p in level.platform_group:  # moves platforms
                        p.rect.x += self.move_speed
                    for p in level.obstruct_group:  # moves obstacles like snowman
                        p.rect.x += self.move_speed
                    for a in level.letter_group:
                        a.rect_original.x += self.move_speed
                    for p in level.power_up_group:  # moves obstacles like snowman
                        p.rect.x += self.move_speed
                else:
                    if self.rect.x - self.move_speed >= 0:
                        self.rect.x -= self.move_speed
            self.rect.x += self.move_speed
            self.obstruct_obstacles(level)
            self.old_list = "left"

        else:
            self.index = 0
            if self.old_list == "right":
                self.image = self.idle_image
                # self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
            else:
                self.image = self.idle_image_flipped
                # self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)

        self.index += 0.33  # image will change around every 3 times the function is called
        if self.index >= len(self.right_images) or self.old_list != direction:
            self.index = 0

    def gravity(self, level: Level.Level):
        self.velocity_y += 0.4
        self.rect.y += self.velocity_y
        self.obstruct_platforms(level, "gravity")
        self.obstruct_obstacles(level)
        # if self.rect.y > ss.SCREEN_HEIGHT:
        #     self.next_screen

    def jump(self, level: Level.Level):
        if self.double_jump_power_up:
            if not self.kill_player:
                if self.color and self.color_num % 3 == 0:
                    self.image = pygame.mask.from_surface(self.image).to_surface()
                    self.image.set_colorkey((0, 0, 0))
                    self.color = False
                elif self.color_num % 3 == 0:
                    self.image.set_colorkey((0, 0, 0))
                    self.color = True
                if self.jumping:
                    self.double_jump(level)
            self.color_num += 1
        elif self.jumping:
            self.rect.y -= 11.2
            # self.jumping = True
            self.on_ground = False
            self.obstruct_platforms(level, "jump")
            self.obstruct_obstacles(level)
            self.num_jumps += 1

    def double_jump(self, level: Level.Level):
        self.rect.y -= 16
        self.jumping = True
        self.on_ground = False
        self.obstruct_platforms(level, "jump")
        self.obstruct_obstacles(level)
        self.num_jumps = 0

    def obstruct_platforms(self, level: Level.Level, process: str):
        collided_list = pygame.sprite.spritecollide(self, level.platform_group, False)
        # if collided_list:
        #     collided_list = pygame.sprite.spritecollide(self, level.obstruct_group, False, pygame.sprite.collide_mask)
        for collided in collided_list:
            if process == "gravity" and 0 < self.rect.bottom - collided.rect.y <= 50:
                self.velocity_y = 0
                self.rect.bottom = collided.rect.top
                self.jumping = False
                self.on_ground = True
                return True
            elif process == "jump" and 0 > self.rect.y - collided.rect.bottom > -50:
                self.jumping = False
                self.rect.top = collided.rect.bottom
                return True

            # addressing the point where the object is on the space is causing the error
            elif process == "right" and 0 < self.rect.right - collided.rect.x < 10 and not \
                    (0 < self.rect.bottom - collided.rect.y < 5):
                self.rect.right = collided.rect.x + 1
                return True
            elif process == "left" and 0 > self.rect.x - collided.rect.right > -10 and not \
                    (0 < self.rect.bottom - collided.rect.y < 5):
                self.rect.left = collided.rect.right - 1
                return True
        return False

    def rope(self):
        pass

    def obstruct_obstacles(self, level: Level.Level):
        collided_list = pygame.sprite.spritecollide(self, level.obstruct_group, False)
        if collided_list:
            collide_mask = pygame.sprite.collide_mask(self, collided_list[0])
            if collide_mask:
                self.kill_player = True
                self.obstacle_collided_with = collided_list[0]

    def collect_letter(self, level: Level.Level):
        collided_list = pygame.sprite.spritecollide(self, level.letter_group, False)
        if collided_list:
            collided = collided_list[0]
            if isinstance(collided, letter.Letter):
                self.letter_lis.append(collided)
            elif isinstance(collided, letter.MysteryLetter):
                self.mystery_letter_lis.append(collided)
            collided.collecting_animation = True

    def collect_power_up(self, level: Level.Level):
        collided_list = pygame.sprite.spritecollide(self, level.power_up_group, False)
        if collided_list:
            collided = collided_list[0]
            self.power_up_lis.append(collided)
            self.double_jump_power_up = True
            collided.collecting_animation = True

    def kill_self(self):
        """Kill animation"""
        if self.kill_player:
            self.obstacle_collided_with.die(self.old_list)
            if self.old_list == "right":
                self.image = self.death_images[int(self.index_dead)]
            else:
                self.image = pygame.transform.flip(self.death_images[int(self.index_dead)], True, False)
                self.image.set_colorkey((0, 0, 0))
            self.rect = self.image.get_rect(center=self.rect.center)
            if not self.index_dead + 0.33 >= len(self.death_images):
                self.index_dead += 0.33  # image will change around every 3 times the function is called
