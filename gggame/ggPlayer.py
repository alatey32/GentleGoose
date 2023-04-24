from os import listdir
from gggame.ggGameObject import *

class ggPlayer(ggGameObject):
    # IMGS_PATH = 'goose'
    IMGS_PATH = "goose_in_hut"
    animation_img_index = 0
    animation_imgs = []
    speed = 5 #set move speed

    def __init__(self, engine):
        self.engine = engine

    def init(self):
        self.resize(0.1)

        self.rect = self.surface.get_rect()
        self.rect.x = self.engine.gameInfo.screen.width / 2
        self.rect.y = self.engine.gameInfo.screen.heigth / 2

    def resize(self, koef):
        self.animation_imgs = [self.engine.texturesEngine.load(self.IMGS_PATH + '/' + file, koef) for file in listdir(self.IMGS_PATH)]
        self.nextImg()
    
    def nextImg(self):
        self.animation_img_index += 1
        if self.animation_img_index == len(self.animation_imgs):
            self.animation_img_index = 0

        self.surface = self.animation_imgs[self.animation_img_index]
        # self.rect = self.surface.get_rect()
