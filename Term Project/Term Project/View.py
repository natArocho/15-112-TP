import pygame, random

from UnitClasses import *
from WeaponsClasses import *
from TileClass import *

def redrawAll(self, screen):
    yDist = self.height//self.rows
    xDist = self.width//self.cols
    for row in range(self.rows):
        for col in range(self.cols):
            screen.blit(self.grid[row][col].tileSprite, (xDist*col, yDist*row))
            if self.grid[row][col].unit != None and not self.grid[row][col].unit.turnUsed:
                if self.grid[row][col].unit.team == "Player":  
                    screen.blit(self.grid[row][col].unit.playerSprite, (xDist*col, yDist*row))
                else:
                    screen.blit(self.grid[row][col].unit.enemySprite, (xDist*col, yDist*row))
            elif self.grid[row][col].unit != None and self.grid[row][col].unit.turnUsed:
                pygame.draw.circle(screen, (178, 178, 178), \
                    (xDist*col+xDist//2, yDist*row+yDist//2), xDist//2)
    
    moveSet = set()
    for row in range(self.rows):
        for col in range(self.cols):
            if self.grid[row][col].unit != None and (self.grid[row][col].unit.selected \
             or (self.grid[row][col].unit.team == "Enemy") and self.displayEnemyAttacks):
                for move in self.grid[row][col].unit.attackMoves:
                        if move in self.grid[row][col].unit.legalRange and self.grid[row][col].unit.team == "Player":
                            screen.blit(self.legalTile, (xDist*move[1], yDist*move[0]))
                        else:
                            if move not in moveSet:
                                screen.blit(self.attackTile, (xDist*move[1], yDist*move[0]))
                                moveSet.add(move)

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

    if self.drawTime:
        if self.seconds%10 == self.seconds:
            time = str(self.minutes)+":0"+str(self.seconds)
        else:
            time = str(self.minutes)+":"+str(self.seconds)
        Unit.drawFont(screen, time, (0,0))
