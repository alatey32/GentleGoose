import pygame
import random

class ggGameObject:
    def __init__(self, surface, rect, speed): 
        self.surface = surface
        self.rect = rect
        self.speed = speed

class enemy_rocket:
    def __init__(self, engine, surface): 
        self.surface = surface
        start_rect = self.surface.get_rect()
        enemy_creation_limit = start_rect.size[1]
        self.rect = pygame.Rect(engine.gameInfo.screen.width, random.randint(enemy_creation_limit, engine.gameInfo.screen.heigth - (enemy_creation_limit * 2)), *start_rect.size)     #set start position and size on screen
        # enemy_speed = random.randint(2, 5)                  #set move speed
        self.speed = random.randint(4, 6)                  #set move speed
        
