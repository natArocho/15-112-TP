class Tile(object):

    tiles = []

    #Note, the tileSprite will be a sprite eventually, for now it is just 
    # a tuple w/ RGB values
    def __init__(self, position, movePenalty, tileSprite, sideEffects, unit=None):
        self.movePenalty = movePenalty
        self.tileSprite = tileSprite
        self.sideEffects = sideEffects
        self.unit = unit
        self.parent = None
        self.children = []
        self.position = position
        Tile.tiles.append(self)

    @staticmethod 
    def removeParentChild():
        #After pathfinding is done, sets all tiles
        #parents and children to None again
        for tile in Tile.tiles:
            tile.parent = None
            tile.children = []

    def gCost(self):
        g = self.movePenalty
        if self.parent != None:
            g += self.parent.gCost()
        return g

class Field(Tile):
    def __init__(self, unit, position):
        tileSprite = (0, 200, 0)
        movePenalty = 1
        sideEffects = None
        super().__init__(position, movePenalty, tileSprite, sideEffects)

class Sand(Tile):
    def __init__(self, unit, position):
        tileSprite = (255, 214, 151)
        movePenalty = 1.5
        sideEffects = None
        super().__init__(position, movePenalty, tileSprite, sideEffects)

#Note: a move penalty of None means the terrain cannot be crossed
class Mountain(Tile):
    def __init__(self, unit, position):
        tileSprite = (86, 90, 86)
        movePenalty = None
        sideEffects = None
        super().__init__(position, movePenalty, tileSprite, sideEffects)



