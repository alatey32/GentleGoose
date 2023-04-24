from os import listdir
from ggGameObject import *

class ggPlayer(ggGameObject):
    IMGS_PATH = 'goose'
    animation_img_index = 0
    animation_imgs = []
    speed = 5 #set move speed

    def __init__(self, engine):
        self.engine = engine

    def resize(self, koef):
        self.animation_imgs = [self.engine.texturesEngine.load(self.IMGS_PATH + '/' + file, koef) for file in listdir(self.IMGS_PATH)]
        self.nextImg()
    
    def nextImg(self):
        self.animation_img_index += 1
        if self.animation_img_index == len(self.animation_imgs):
            self.animation_img_index = 0

        self.surface = self.animation_imgs[self.animation_img_index]
        # self.rect = self.surface.get_rect()
