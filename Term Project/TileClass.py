import pygame

class Tile(object):

    tiles = []
    xDist = None
    yDist = None

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
    tileSprite = None

    def __init__(self, unit, position):
        movePenalty = 1
        sideEffects = None
        super().__init__(position, movePenalty, Field.tileSprite, sideEffects)

class Tree(Tile):
    tileSprite = None

    def __init__(self, unit, position):
        movePenalty = 2
        sideEffects = ("Avoid", 30)
        super().__init__(position, movePenalty, Tree.tileSprite, sideEffects)

class Sand(Tile):
    tileSprite = None

    def __init__(self, unit, position):
        movePenalty = 1.5
        sideEffects = None
        super().__init__(position, movePenalty, Sand.tileSprite, sideEffects)

class Fort(Tile):
    tileSprite = None

    def __init__(self, unit, position):
        movePenalty = 1
        sideEffects = ("Protection", 10)
        super().__init__(position, movePenalty, Fort.tileSprite, sideEffects)


#Note: a move penalty of None means the terrain cannot be crossed
class Mountain(Tile):
    tileSprite = None

    def __init__(self, unit, position):
        movePenalty = None
        sideEffects = None
        super().__init__(position, movePenalty, Mountain.tileSprite, sideEffects)



