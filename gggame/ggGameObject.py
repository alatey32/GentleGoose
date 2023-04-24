import pygame
import random

def my_load_texture(file_name, zoom):
    surface = pygame.image.load(file_name).convert_alpha()
    surface = pygame.transform.smoothscale_by(surface, zoom)
    return surface

class ggGameObject:
    def colliderect(self, gameObject):
        if self.rect.colliderect(gameObject.rect):
            return True
        return False
     
    def move(self, x, y):
        self.rect = self.rect.move(x, y)
        return self.rect

class enemy_rocket(ggGameObject):
    def __init__(self, engine): 
        self.surface = engine.texturesEngine.load('enemy.png', 0.5)
        start_rect = self.surface.get_rect()
        enemy_creation_limit = start_rect.size[1]
        # self.rect = pygame.Rect(engine.gameInfo.screen.width, random.randint(enemy_creation_limit, engine.gameInfo.screen.heigth - (enemy_creation_limit * 2)), *start_rect.size) 
        self.rect = pygame.Rect(engine.gameInfo.screen.width, random.randint(enemy_creation_limit, engine.gameInfo.screen.heigth - 200), *start_rect.size) 
        self.speed = random.randint(4, 6)                  #set move speed
        
class enemy_tank(ggGameObject):
    def __init__(self, engine): 
         # setup enemy
        self.surface = engine.texturesEngine.load('tank.png', 0.15) # load texture
        start_rect = self.surface.get_rect()
        enemy_creation_limit = start_rect.size[1]
        # self.rect = pygame.Rect(engine.gameInfo.screen.width, random.randint(engine.gameInfo.screen.heigth - (enemy_creation_limit * 2), engine.gameInfo.screen.heigth - enemy_creation_limit), *start_rect.size)
        self.rect = pygame.Rect(engine.gameInfo.screen.width, random.randint(engine.gameInfo.screen.heigth - 190, engine.gameInfo.screen.heigth - 80), *start_rect.size)
        self.speed = random.randint(1, 3)                  #set move speed              #set move speed

class bonus_brolly(ggGameObject):
    def __init__(self, engine):
        self.surface = engine.texturesEngine.load('bonus.png', 0.5) # load texture
        
        start_rect = self.surface.get_rect()
        bonus_creation_limit = start_rect.size[0]
        self.rect = pygame.Rect(random.randint(0, engine.gameInfo.screen.width - bonus_creation_limit), 0 - start_rect.height, *start_rect.size)     #set start position and size on screen
        
        self.speed = random.randint(1, 5)                  #set move speed

class weapon_bomb(ggGameObject):
    def __init__(self, engine):
        ball_rect = engine.player.rect
        self.surface = engine.texturesEngine.load('bomba.png', 1) # load texture

        start_rect = self.surface.get_rect()    
        self.rect = pygame.Rect(ball_rect.centerx - 40, ball_rect.centery, *start_rect.size)     #set start position and size on screen
        
        self.speed = random.randint(1, 6)                  #set move speed