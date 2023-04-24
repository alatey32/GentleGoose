import pygame

class ggTexturesEngine:
    def __init__(self):
        self.loaded = dict()

    def load(self, file_name, zoom):

        if file_name in self.loaded and zoom in self.loaded[file_name]:
            surface = self.loaded[file_name][zoom]
        else:
            surface = pygame.image.load(file_name).convert_alpha()
            surface = pygame.transform.smoothscale_by(surface, zoom)

            if file_name not in self.loaded:
                self.loaded[file_name] = dict()
            self.loaded[file_name][zoom] = surface
            

        # surface = pygame.image.load(file_name).convert_alpha()
        # surface = pygame.transform.smoothscale_by(surface, zoom)
        return surface