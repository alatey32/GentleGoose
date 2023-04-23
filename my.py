import random
import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT, K_SPACE, K_q
from os import listdir
import os

pygame.init()

pygame.display.set_caption('Gentle Goose v 1.0')

#sound
pygame.mixer.init() # add this line
ouch = pygame.mixer.Sound('ga.wav')
bonus_sound = pygame.mixer.Sound('bonus.mp3')
exp_raket = pygame.mixer.Sound('exp_raket.mp3')
exp_tank = pygame.mixer.Sound('exp_tank.mp3')
crash_snd = pygame.mixer.Sound('crash.mp3')

FPS = pygame.time.Clock()

# screen = width, heigth = 800, 600
screen = width, heigth = 1024, 768

print(screen)

BLACK = 0,0,0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0

font = pygame.font.SysFont('Verdana', 20)

# setup screen
main_surface = pygame.display.set_mode(screen)

def my_load_texture(file_name, zoom):
    surface = pygame.image.load(file_name).convert_alpha()
    surface = pygame.transform.smoothscale_by(surface, zoom)
    return surface

def load_player_textures(koef):
    return [my_load_texture(IMGS_PATH + '/' + file, koef) for file in listdir(IMGS_PATH)]

# setup ball (player)
IMGS_PATH = 'goose'
player_imgs = load_player_textures(0.1)
img_index = 0
ball = player_imgs[img_index]

# ball = my_load_texture('enemy.png', 0.5)
ball_rect = ball.get_rect()     #set screen start position and size on screen
ball_speed = 5                  #set move speed

def create_enemy():
    # setup enemy
    enemy = my_load_texture('enemy.png', 0.5) # load texture
    start_rect = enemy.get_rect()
    enemy_creation_limit = start_rect.size[1]
    enemy_rect = pygame.Rect(width, random.randint(enemy_creation_limit, heigth - (enemy_creation_limit * 2)), *start_rect.size)     #set start position and size on screen
    # enemy_speed = random.randint(2, 5)                  #set move speed
    enemy_speed = random.randint(4, 6)                  #set move speed
    return [enemy, enemy_rect, enemy_speed]

def create_enemy_tank():
    # setup enemy
    enemy = my_load_texture('tank.png', 0.15) # load texture
    start_rect = enemy.get_rect()
    enemy_creation_limit = start_rect.size[1]
    enemy_rect = pygame.Rect(width, random.randint(heigth - (enemy_creation_limit * 2), heigth - enemy_creation_limit), *start_rect.size)     #set start position and size on screen
    enemy_speed = random.randint(1, 3)                  #set move speed
    return [enemy, enemy_rect, enemy_speed]

def create_bonus():
    # setup bonus
    bonus = my_load_texture('bonus.png', 0.5) # load texture
    start_rect = bonus.get_rect()
    bonus_creation_limit = start_rect.size[0]
    bonus_rect = pygame.Rect(random.randint(0, width - bonus_creation_limit), 0 - start_rect.height, *start_rect.size)     #set start position and size on screen
    bonus_speed = random.randint(1, 5)                  #set move speed
    return [bonus, bonus_rect, bonus_speed]

def create_bomba():
    # setup bonus
    bonus = my_load_texture('bomba.png', 1) # load texture
    start_rect = bonus.get_rect()    
    bonus_rect = pygame.Rect(ball_rect.centerx - 40, ball_rect.centery, *start_rect.size)     #set start position and size on screen
    bonus_speed = random.randint(1, 6)                  #set move speed
    return [bonus, bonus_rect, bonus_speed]

bg = pygame.transform.scale(pygame.image.load('background.png').convert(), screen)
bgX = 0;
bgX2 = bg.get_width();
bg_speed = 3

scores = 0
destroyed_tanks = 0
destroyed_rakets = 0

enemies = [] # enemy collection
bonuses = [] # bonuses collection
tanks = [] # bonuses collection
bombas = [] 

#create enemy event
CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

#create bonus event
CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 1500)

# change player image
CHANGE_IMG = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMG, 125)

CREATE_TANK = pygame.USEREVENT + 4
pygame.time.set_timer(CREATE_TANK, 1500)

is_working = True

live_score = 1

serrial_bomb = 0

space_pressed = False
q_pressed = False

# game cycle
while is_working:
    FPS.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:            
            is_working = False

        elif event.type == CREATE_ENEMY:
            enemies.append(create_enemy())

        elif event.type == CREATE_BONUS:        
            bonuses.append(create_bonus())

        elif event.type == CHANGE_IMG:        
            img_index += 1
            if img_index == len(player_imgs):
                img_index = 0
            ball = player_imgs[img_index]
            dX = ball_rect.x
            dY = ball_rect.y
            ball_rect = ball.get_rect()
            ball_rect.x = dX
            ball_rect.y = dY

        elif event.type == CREATE_TANK:        
            tanks.append(create_enemy_tank())
            

    # Draw background
    
    # main_surface.fill(BLACK)
    # main_surface.blit(bg, (0, 0))

    bgX -= bg_speed
    bgX2 -= bg_speed

    if bgX < - bg.get_width():
        bgX = bg.get_width()

    if bgX2 < - bg.get_width():
        bgX2 = bg.get_width()

    main_surface.blit(bg, (bgX, 0))
    main_surface.blit(bg, (bgX2, 0))

    # draw 'ball'    
    main_surface.blit(ball, ball_rect)

    # draw scores    
    main_surface.blit(font.render("Rakets: " + str(destroyed_rakets) + " Tanks: " + str(destroyed_tanks) + " Scores: " + str(scores), True, BLACK), (0, 0))
    
    # draw and processing enemies
    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2], 0) # move enemy
        main_surface.blit(enemy[0], enemy[1])  # draw enemy
        
        # delete escaped enemies
        if enemy[1].right < 0:
            enemies.pop(enemies.index(enemy))

        # delete collision
        if ball_rect.colliderect(enemy[1]):
            if(scores >= live_score):
                pygame.mixer.Sound.play(crash_snd)
                scores -= live_score
                enemies.pop(enemies.index(enemy))

                if(scores <= 0):
                    player_imgs = load_player_textures(0.1)
                else:
                    player_imgs = load_player_textures(0.1 * scores)

            else:
                is_working = False

    # draw and processing bonuses
    for bonus in bonuses:
        bonus[1] = bonus[1].move(0, bonus[2]) # move bonus
        main_surface.blit(bonus[0], bonus[1])  # draw bonus
        
        # delete escaped bonuses
        if bonus[1].top > heigth:
            bonuses.pop(bonuses.index(bonus))

        # bonus collision
        if ball_rect.colliderect(bonus[1]):
            pygame.mixer.Sound.play(bonus_sound)
            bonuses.pop(bonuses.index(bonus)) # delete
            scores += 1            
            if(scores <= 0):
                player_imgs = load_player_textures(0.1)
            else:
                player_imgs = load_player_textures(0.1 * scores)

    # draw and processing tanks
    for tank in tanks:
        tank[1] = tank[1].move(-tank[2], 0) # move tank
        main_surface.blit(tank[0], tank[1])  # draw tank
        
        # delete escaped enemies
        if tank[1].right < 0:            
            tanks.pop(tanks.index(tank))

        # delete collision
        if ball_rect.colliderect(tank[1]):
            if(scores >= live_score):
                pygame.mixer.Sound.play(crash_snd)
                scores -= live_score
                tanks.pop(tanks.index(tank))

                if(scores <= 0):
                    player_imgs = load_player_textures(0.1)
                else:
                    player_imgs = load_player_textures(0.1 * scores)
            else:
                is_working = False

    # draw and processing bombas
    for bomba in bombas:
        bomba[1] = bomba[1].move(0, bomba[2]) # move bonus
        main_surface.blit(bomba[0], bomba[1])  # draw bonus
        
        # delete escaped bombas
        if bomba[1].top > heigth:
            bombas.pop(bombas.index(bomba))
        else:
            # destroing tanks
            for tank in tanks:
                if bomba[1].colliderect(tank[1]):
                    pygame.mixer.Sound.play(exp_tank)
                    destroyed_tanks += 1    
                    bombas.pop(bombas.index(bomba))
                    tanks.pop(tanks.index(tank))

            # destroing enemies
            if bomba in bombas:
                for enemy in enemies:
                    if bomba[1].colliderect(enemy[1]):
                        pygame.mixer.Sound.play(exp_raket)
                        destroyed_rakets += 1
                        bombas.pop(bombas.index(bomba))
                        enemies.pop(enemies.index(enemy))        

    # key control processing (WASD)
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[K_DOWN] and not ball_rect.bottom >= heigth:
        ball_rect = ball_rect.move(0, ball_speed)

    if pressed_keys[K_UP] and ball_rect.top > 0:
        ball_rect = ball_rect.move(0, -ball_speed)

    if pressed_keys[K_RIGHT] and ball_rect.right < width:
        ball_rect = ball_rect.move(ball_speed, 0)

    if pressed_keys[K_LEFT] and ball_rect.left > 0:
        ball_rect = ball_rect.move(-ball_speed, 0)

    if pressed_keys[K_SPACE]:
        if not space_pressed:
            space_pressed = True
            if scores > 0:
                pygame.mixer.Sound.play(ouch)
                bombas.append(create_bomba())
                scores -= 1
            
                if(scores <= 0):
                    player_imgs = load_player_textures(0.1)
                else:
                    player_imgs = load_player_textures(0.1 * scores)
    else:
        space_pressed = False

    if pressed_keys[K_q]:
        if serrial_bomb == 0 and not q_pressed:
            q_pressed = True
            if scores > 5:
                serrial_bomb = 5
                scores -= 5
    else:
        q_pressed = False

    if serrial_bomb > 0:
        serrial_bomb -= 1
        pygame.mixer.Sound.play(ouch)
        bombas.append(create_bomba())        
            
        if(scores <= 0):
            player_imgs = load_player_textures(0.1)
        else:
            player_imgs = load_player_textures(0.1 * scores)
                 


    # print(len(bonuses))

    # draw compleate
    pygame.display.flip()

pygame.quit()