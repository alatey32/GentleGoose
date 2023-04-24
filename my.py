import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT, K_SPACE, K_q
from gggame.ggGameInfo import *
from gggame.ggGameObject import *
from gggame.ggTexturesEngine import *
from gggame.ggPlayer import *


class GameEngine:
    destroyed_tanks = 0
    destroyed_rakets = 0

    destroyed_tanks_max = 100
    destroyed_rakets_max = 100

    def __init__(self): 
        self.gameInfo = ggGameInfo()
        self.texturesEngine = ggTexturesEngine()
        self.player = ggPlayer(self)

engine = GameEngine()

pygame.init()
pygame.display.set_caption(engine.gameInfo.toString())

#sound
pygame.mixer.init() # add this line
ouch = pygame.mixer.Sound('ga.wav')
bonus_sound = pygame.mixer.Sound('bonus.mp3')
exp_raket = pygame.mixer.Sound('exp_raket.mp3')
exp_tank = pygame.mixer.Sound('exp_tank.mp3')
crash_snd = pygame.mixer.Sound('crash.mp3')

FPS = pygame.time.Clock()

BLACK = 0,0,0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0

font = pygame.font.SysFont('Verdana', 20)

# setup screen
main_surface = pygame.display.set_mode(engine.gameInfo.screen.toCoordinate())
    

# setup player
engine.player.init()

bg = pygame.transform.scale(pygame.image.load('background.png').convert(), engine.gameInfo.screen.toCoordinate())
bgX = 0;
bgX2 = bg.get_width();
bg_speed = 3

scores = 0

rockets = [] # enemy collection
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
            if engine.destroyed_rakets < engine.destroyed_rakets_max:
                rockets.append(enemy_rocket(engine))

        elif event.type == CREATE_BONUS:        
            bonuses.append(bonus_brolly(engine))

        elif event.type == CREATE_TANK:
            if engine.destroyed_tanks < engine.destroyed_tanks_max:
                tanks.append(enemy_tank(engine))

        elif event.type == CHANGE_IMG:
            engine.player.nextImg()
            dX = engine.player.rect.x
            dY = engine.player.rect.y
            engine.player.rect = engine.player.surface.get_rect()
            engine.player.rect.x = dX
            engine.player.rect.y = dY
            

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
    main_surface.blit(engine.player.surface, engine.player.rect)

    
    
    # draw and processing rockets
    for enemy in rockets:
        enemy.move(-enemy.speed, 0) # move enemy
        main_surface.blit(enemy.surface, enemy.rect)  # draw enemy
        
        # delete escaped rockets
        if enemy.rect.right < 0:
            rockets.pop(rockets.index(enemy))

        # delete collision
        if engine.player.colliderect(enemy):
            if(scores >= live_score):
                pygame.mixer.Sound.play(crash_snd)
                scores -= live_score
                rockets.pop(rockets.index(enemy))

                if(scores <= 0):
                    engine.player.resize(0.1)
                else:
                    engine.player.resize(0.1 * scores)

            else:
                is_working = False

    # draw and processing bonuses
    for bonus in bonuses:
        bonus.move(0, bonus.speed) # move bonus
        main_surface.blit(bonus.surface, bonus.rect)  # draw bonus
        
        # delete escaped bonuses
        if bonus.rect.top > engine.gameInfo.screen.heigth:
            bonuses.pop(bonuses.index(bonus))

        # bonus collision
        if engine.player.colliderect(bonus):
            pygame.mixer.Sound.play(bonus_sound)
            bonuses.pop(bonuses.index(bonus)) # delete
            scores += 1            
            if(scores <= 0):
                engine.player.resize(0.1)
            else:
                engine.player.resize(0.1 * scores)

    # draw and processing tanks
    for tank in tanks:
        tank.move(-tank.speed, 0) # move tank
        main_surface.blit(tank.surface, tank.rect)  # draw tank
        
        # delete escaped enemies
        if tank.rect.right < 0:            
            tanks.pop(tanks.index(tank))

        # delete collision
        if engine.player.colliderect(tank):
            if(scores >= live_score):
                pygame.mixer.Sound.play(crash_snd)
                scores -= live_score
                tanks.pop(tanks.index(tank))

                if(scores <= 0):
                    engine.player.resize(0.1)
                else:
                    engine.player.resize(0.1 * scores)
            else:
                is_working = False

    # draw and processing bombas
    for bomba in bombas:
        bomba.move(0, bomba.speed) # move bonus
        main_surface.blit(bomba.surface, bomba.rect)  # draw bonus
        
        # delete escaped bombas
        if bomba.rect.top > engine.gameInfo.screen.heigth:
            bombas.pop(bombas.index(bomba))
        else:
            # destroing tanks
            if bomba in bombas:
                for tank in tanks:
                    if bomba.colliderect(tank):
                        pygame.mixer.Sound.play(exp_tank)
                        engine.destroyed_tanks += 1    
                        if bomba in bombas:
                            bombas.pop(bombas.index(bomba))
                        tanks.pop(tanks.index(tank))

            # destroing enemies
            if bomba in bombas:
                for rocket in rockets:
                    if bomba.colliderect(rocket):
                        pygame.mixer.Sound.play(exp_raket)
                        engine.destroyed_rakets += 1
                        bombas.pop(bombas.index(bomba))
                        rockets.pop(rockets.index(rocket))        

    # key control processing (WASD)
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[K_DOWN] and not engine.player.rect.bottom >= engine.gameInfo.screen.heigth:
        engine.player.move(0, engine.player.speed)

    if pressed_keys[K_UP] and engine.player.rect.top > 0:
        engine.player.move(0, -engine.player.speed)

    if pressed_keys[K_RIGHT] and engine.player.rect.right < engine.gameInfo.screen.width:
        engine.player.move(engine.player.speed, 0)

    if pressed_keys[K_LEFT] and engine.player.rect.left > 0:
        engine.player.move(-engine.player.speed, 0)

    if pressed_keys[K_SPACE]:
        if not space_pressed:
            space_pressed = True
            if scores > 0:
                pygame.mixer.Sound.play(ouch)
                bombas.append(weapon_bomb(engine))
                scores -= 1
            
                if(scores <= 0):
                    engine.player.resize(0.1)
                else:
                    engine.player.resize(0.1 * scores)
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
        bombas.append(weapon_bomb(engine))        
            
        if(scores <= 0):
            engine.player.resize(0.1)
        else:
            engine.player.resize(0.1 * scores)
                 

    # draw scores    
    main_surface.blit(font.render("Rakets: " + str(engine.destroyed_rakets) + " Tanks: " + str(engine.destroyed_tanks) + " Scores: " + str(scores), True, BLACK), (0, 0))

    # draw compleate
    pygame.display.flip()

pygame.quit()