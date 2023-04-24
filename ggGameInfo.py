class Size:
    def __init__(self, width, heigth):        
        self.width = width
        self.heigth = heigth

class ggGameInfo:
    name = "Gentle Goose"
    version = "1.0"

    def __init__(self):
        self.screen = Size(1024, 768)

    def toString(self):
        return self.name + self.version