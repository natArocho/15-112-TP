import pygame, random

from UnitClasses import *
from WeaponsClasses import *
from TileClass import *

def redrawAll(self, screen):
    yDist = self.height//self.rows
    xDist = self.width//self.cols
    for row in range(self.rows):
        for col in range(self.cols): 
            pygame.draw.rect(screen, self.grid[row][col].tileSprite, (xDist*col, yDist*row\
            , xDist, yDist))
            if self.grid[row][col].unit != None and not self.grid[row][col].unit.turnUsed:
                pygame.draw.circle(screen, self.grid[row][col].unit.color, \
                    (xDist*col+xDist//2, yDist*row+yDist//2), xDist//2)
            elif self.grid[row][col].unit != None and self.grid[row][col].unit.turnUsed:
                pygame.draw.circle(screen, (178, 178, 178), \
                    (xDist*col+xDist//2, yDist*row+yDist//2), xDist//2)
 
    for row in range(self.rows):
        for col in range(self.cols):
            if self.grid[row][col].unit != None and self.grid[row][col].unit.selected:
                for move in self.grid[row][col].unit.attackMoves:
                        if move in self.grid[row][col].unit.legalRange:
                            if move != self.grid[row][col].unit.position:
                                pygame.draw.rect(screen, (0,0,255), \
                                (xDist*move[1], yDist*move[0], xDist, yDist))
                        else:
                            pygame.draw.rect(screen, (255,0,0), \
                            (xDist*move[1], yDist*move[0], xDist, yDist))
                if self.grid[row][col].unit.optionsOn:
                    self.grid[row][col].unit.drawOptions(screen, xDist, yDist, row, col)
                elif self.grid[row][col].unit.drawAttacks:
                    self.grid[row][col].unit.drawAttackMenu(screen, xDist, yDist, row, col)
                elif self.grid[row][col].unit.inventoryOn:
                    self.grid[row][col].unit.drawInventory(screen, xDist, yDist, row, col)
            
    #Cursor
    if (Unit.selectedUnit != None and not Unit.selectedUnit.optionsOn) and \
        (Unit.selectedUnit != None and not Unit.selectedUnit.drawAttacks) and \
        (Unit.selectedUnit != None and not Unit.selectedUnit.inventoryOn) \
            or Unit.selectedUnit == None:

        pygame.draw.line(screen, (255, 255 ,0), (xDist*self.curCol, yDist*self.curRow), \
        (xDist*self.curCol+xDist, yDist*self.curRow), 5)
        pygame.draw.line(screen, (255, 255 ,0), (xDist*self.curCol+xDist, yDist*self.curRow), \
        (xDist*self.curCol+xDist, yDist*self.curRow+xDist), 5)
        pygame.draw.line(screen, (255, 255 ,0), (xDist*self.curCol+xDist, yDist*self.curRow+yDist), \
        (xDist*self.curCol, yDist*self.curRow+yDist), 5)
        pygame.draw.line(screen, (255, 255 ,0), (xDist*self.curCol, yDist*self.curRow+yDist), \
        (xDist*self.curCol, yDist*self.curRow), 5)
