import pygame
import Level
import screen_size as ss
import letter
from math import ceil
from decode_file import decode_file
import images_store 
import other_skins


# Set up the player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, skin: str):
        super().__init__()
        # Fall has to be tested
        match skin:
            case "santa":
                run_var_name = other_skins.Santa_Run
                dead_var_name = other_skins.Santa_Dead
                idle_var_name = other_skins.Santa_Idle
                fall = 2
            case "boy":
                run_var_name = images_store.Boy_Run
                dead_var_name = images_store.Boy_Dead
                idle_var_name = images_store.Boy_Idle
                fall = 3.5
            case "female_zombie":
                run_var_name = other_skins.Female_zombie_Run
                dead_var_name = other_skins.Female_zombie_Dead
                idle_var_name = other_skins.Female_zombie_Idle
                fall = 1.8
            case "male_zombie":
                run_var_name = other_skins.Male_zombie_Run
                dead_var_name = other_skins.Male_zombie_Dead
                idle_var_name = other_skins.Male_zombie_Idle
                fall = 3
            case "adventure_boy":
                run_var_name = images_store.Adventure_boy_Run
                dead_var_name = images_store.Adventure_boy_Dead
                idle_var_name = images_store.Adventure_boy_Idle
                fall = 3.8  # Fall is good
            case "adventure_girl":
                run_var_name = images_store.Adventure_boy_Run
                dead_var_name = images_store.Adventure_boy_Dead
                idle_var_name = images_store.Adventure_boy_Idle
                fall = 3.8
            case "cat":
                run_var_name = images_store.Cat_Run
                dead_var_name = images_store.Cat_Dead
                idle_var_name = images_store.Cat_Idle
                fall = 2.8  # Fall is good
            case "dinosaur":
                run_var_name = images_store.Dinosaur_Run
                dead_var_name = images_store.Dinosaur_Dead
                idle_var_name = images_store.Dinosaur_Idle
                fall = 5  # Fall is good
            case "dog":
                run_var_name = images_store.Dog_Run
                dead_var_name = images_store.Dog_Dead
                idle_var_name = images_store.Dog_Idle
                fall = 3.5  # Fall is good
            case "knight":
                run_var_name = images_store.Knight_Run
                dead_var_name = images_store.Knight_Dead
                idle_var_name = images_store.Knight_Idle
                fall = 3.5  # Fall is good
            case "ninja_girl":
                run_var_name = images_store.Ninja_girl_Run
                dead_var_name = images_store.Ninja_girl_Dead
                idle_var_name = images_store.Ninja_girl_Idle
                fall = 3.5  # Fall is good
            case "ninja_girl2":
                run_var_name = images_store.Ninja_girl2_Run
                dead_var_name = images_store.Ninja_girl2_Dead
                idle_var_name = images_store.Ninja_girl2_Idle
                fall = 3.5  # Fall is good
            case "pumpkin":
                run_var_name = other_skins.Pumpkin_Run
                dead_var_name = other_skins.Pumpkin_Dead
                idle_var_name = other_skins.Pumpkin_Idle
                fall = 3.5  # Fall is good
            case "robot":
                run_var_name = other_skins.Robot_Run
                dead_var_name = other_skins.Robot_Dead
                idle_var_name = other_skins.Robot_Idle
                fall = 4.4  # Fall is good
            case _:
                raise AttributeError("Invalid skin type " + skin)

        alpha = (0, 0, 0)
        self.idle_image = pygame.image.load(decode_file(idle_var_name)).convert()
        height = int(ss.SCREEN_WIDTH / 19.067)
        self.idle_image = pygame.transform.scale(self.idle_image, (
            self.idle_image.get_width() * height / self.idle_image.get_height(), height))
        self.idle_image.set_colorkey(alpha)
        self.idle_image_flipped = pygame.transform.flip(self.idle_image, True, False)
        self.idle_image_flipped.set_colorkey(alpha)
        self.right_images = []
        self.left_images = []
        self.collect_letter_sound = pygame.mixer.Sound("images/Menu_page/collectcoin-6075.mp3")
        self.jump_sound = pygame.mixer.Sound("images/Menu_page/Jump-SoundBible.com-1007297584.wav")
        self.land_on_ground = pygame.mixer.Sound("images/Menu_page/human-impact-on-ground-6982.mp3")
        self.land_on_ground.set_volume(0.01)
        self.jump_sound.set_volume(0.01)
        for i in run_var_name:
            img = pygame.image.load(decode_file(i)).convert()
            img = pygame.transform.scale(img, (
                img.get_width() * height / img.get_height(), height))
            img.set_colorkey(alpha)
            self.right_images.append(img)
            img_left = pygame.transform.flip(img, True, False)
            img_left.set_colorkey(alpha)
            self.left_images.append(img_left)

        self.death_images = []
        for i in dead_var_name:
            img = pygame.image.load(decode_file(i)).convert()
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
        self.completed = False

    def update_player(self, screen, current_level, pressed, stop_working=False):
        killed = False
        if not stop_working:
            killed = self.kill_self()
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
            self.jump(current_level)

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

        return pressed, killed

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
                    if self.rect.x + self.move_speed > ss.SCREEN_WIDTH:
                        self.completed = True
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
        collided = self.obstruct_platforms(level, "gravity")
        self.obstruct_obstacles(level)
        if not collided:
            if self.rect.y >= ss.SCREEN_HEIGHT - 2*ss.tile_size:
                for p in level.platform_group:  # moves platforms
                    p.rect.y -= self.velocity_y
                for p in level.obstruct_group:  # moves obstacles like snowman
                    p.rect.y -= self.velocity_y
                for a in level.letter_group:
                    a.start_y -= self.velocity_y
                    a.pos[1] = a.start_y
                    a.going_down = False
                for p in level.power_up_group:
                    p.rect.y -= self.velocity_y
            else:
                self.rect.y += self.velocity_y
            self.rect.y = ceil(self.rect.y - self.velocity_y)

    def jump(self, level: Level.Level):
        if self.double_jump_power_up:
            if not self.kill_player:
                if (self.color and self.color_num % 5 == 0) or (not self.color and self.color_num % 5 != 0):
                    self.image = pygame.mask.from_surface(self.image).to_surface()
                    self.image.set_colorkey((0, 0, 0))
                    self.color = False
                elif self.color_num % 5 == 0:
                    self.image.set_colorkey((0, 0, 0))
                    self.color = True
                if self.jumping:
                    if self.on_ground:
                        pygame.mixer.Sound.play(self.jump_sound)
                        pygame.mixer.music.stop()
                    self.double_jump(level)
            self.color_num += 1
        elif self.jumping:
            self.rect.y -= int(ss.tile_size/4)
            # self.jumping = True
            if self.on_ground:
                pygame.mixer.Sound.play(self.jump_sound)
                pygame.mixer.music.stop()
            self.on_ground = False
            self.obstruct_platforms(level, "jump")
            self.obstruct_obstacles(level)
            self.num_jumps += 1

    def double_jump(self, level: Level.Level):
        self.rect.y -= int(ss.tile_size/3)
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
            if process == "gravity" and 0 < self.rect.bottom - collided.rect.y <= int(ss.SCREEN_WIDTH / 28.6):
                if self.velocity_y > 10:
                    pygame.mixer.Sound.play(self.land_on_ground)
                    pygame.mixer.music.stop()
                self.velocity_y = 0
                self.rect.bottom = collided.rect.top
                self.jumping = False
                self.on_ground = True
                return True
            elif process == "jump" and 0 > self.rect.y - collided.rect.bottom > -int(ss.SCREEN_WIDTH / 28.6):
                self.jumping = False
                self.rect.top = collided.rect.bottom
                return True

            # addressing the point where the object is on the space is causing the error
            elif process == "right" and 0 < self.rect.right - collided.rect.x < int(ss.SCREEN_WIDTH / 143) and not \
                    (0 < self.rect.bottom - collided.rect.y < 5):
                self.rect.right = collided.rect.x + 1
                return True
            elif process == "left" and 0 > self.rect.x - collided.rect.right > -int(ss.SCREEN_WIDTH / 143) and not \
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
        if collided_list and isinstance(collided_list[0], letter.Letter):
            pygame.mixer.Sound.play(self.collect_letter_sound)
            pygame.mixer.music.stop()
            if isinstance(collided_list[0], letter.Letter):
                self.letter_lis.append(collided_list[0])
            collided_list[0].collecting_animation = True
        elif collided_list and isinstance(collided_list[0], letter.MysteryLetter):
            pygame.mixer.Sound.play(self.collect_letter_sound)
            pygame.mixer.music.stop()
            self.mystery_letter_lis.append(collided_list[0])
            collided_list[0].collecting_animation = True

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
            else:
                return True
        return False
