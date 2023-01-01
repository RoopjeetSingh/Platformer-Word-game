from player import *
import Level
import screen_size as ss
pygame.init()
screen = pygame.display.set_mode((ss.SCREEN_WIDTH, ss.SCREEN_HEIGHT))

# Set up the game clock
clock = pygame.time.Clock()
level1 = Level.Level1(["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"])
current_level = level1
# Set up the game loop
player = Player(200, 200)
while True:
    current_level.draw(screen)
    current_level.obstruct_group.draw(screen)
    current_level.platform_group.draw(screen)
    current_level.letter_group.draw(screen)
    for i in current_level.letter_group:
        i.bounce_brighten()
    screen.blit(player.image, player.rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if not player.kill_player and \
                    (event.key == pygame.K_UP or event.key == ord('w') or event.key == pygame.K_SPACE):
                if player.on_ground:
                    player.jumping = True
                else:
                    player.double_jump_bool = True
            if event.key in (ord('q'), pygame.K_ESCAPE):
                pygame.quit()
                exit()

    if not player.kill_player:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            player.move_right(current_level, "right")
        elif keys[pygame.K_LEFT]:
            player.move_right(current_level, "left")
        else:
            player.move_right(current_level, "")
    player.kill_self()
    player.gravity(current_level)
    player.jump(current_level)
    player.collect_letter(current_level)
    for i in player.letter_lis:
        i.collect_self(player, current_level)
        screen.blit(i.image, i.rect)
    pygame.display.update()
    clock.tick(60)
