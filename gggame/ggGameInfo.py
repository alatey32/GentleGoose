class Size:
    def __init__(self, width: int, heigth: int):
        self.width = width
        self.heigth = heigth

    def toCoordinate(self):
        return (self.width, self.heigth)

class ggGameInfo:
    name = "Gentle Goose"
    version = "1.1"

    def __init__(self):
        self.screen = Size(1024, 768)

    def toString(self):
        return self.name + self.version