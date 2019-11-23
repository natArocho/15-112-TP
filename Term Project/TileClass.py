class Tile(object):
    #Note, the tileSprite will be a sprite eventually, for now it is just 
    # a tuple w/ RGB values
    def __init__(self, movePenalty, tileSprite, sideEffects):
        self.movePenalty = movePenalty
        self.tileSprite = tileSprite
        self.sideEffects = sideEffects

class Field(Tile):
    def __init__(self):
        tileSprite = (0, 200, 0)
        movePenalty = 1
        sideEffects = None
        super().__init__(movePenalty, tileSprite, sideEffects)

class Sand(Tile):
    def __init__(self):
        tileSprite = (255, 214, 151)
        movePenalty = 2
        sideEffects = None
        super().__init__(movePenalty, tileSprite, sideEffects)

#Note: a move penalty of None means the terrain cannot be crossed
class Mountain(Tile):
    def __init__(self):
        tileSprite = (86, 90, 86)
        movePenalty = None
        sideEffects = None
        super().__init__(movePenalty, tileSprite, sideEffects)



