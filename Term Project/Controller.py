import pygame, random

from UnitClasses import *
from WeaponsClasses import *
from TileClass import *

def setUnits(self):
    for row in range(self.rows):
        for col in range(self.cols):
            if self.grid[row][col].unit != None:
                if self.grid[row][col].unit.stats["HP"] <= 0: 
                    Unit.teams[self.grid[row][col].unit.team].remove(self.grid[row][col].unit)
                    self.grid[row][col].unit = None
                elif not self.grid[row][col].unit.drawAttacks and not self.grid[row][col].unit.optionsOn:
                    self.grid[row][col].unit.setLegalMovesAndAttack((row,col), self.grid)

def isPlayerPhase():
    for unit in Unit.teams["Player"]:
        if not unit.turnUsed:
            return True
    return False

def init(self):
    setUnits(self)
    if not isPlayerPhase():
        moveEnemies(self)

def moveEnemies(self):
    for row in range(self.rows):
        for col in range(self.cols):
            unit = self.grid[row][col].unit
            if unit != None and unit.team == "Enemy":
                unit.select(row, col)
                moveList = list(unit.legalRange) 
                randMove = moveList[random.randint(0, len(moveList)-1)]
                self.grid[Unit.selectedUnit.position[0]][Unit.selectedUnit.position[1]].unit = None
                while True:
                    if self.grid[randMove[0]][randMove[1]].unit == None:
                        self.grid[randMove[0]][randMove[1]].unit = Unit.selectedUnit
                        break
                    else:
                        randMove = moveList[random.randint(0, len(moveList)-1)]
                unit.selected = False
                Unit.selectedUnit = None
                self.turnUsed = True

    for unit in Unit.teams["Player"]:
        unit.turnUsed = False
        pass

def mousePressed(self, x, y):
    pass

def mouseReleased(self, x, y):
    pass

def mouseMotion(self, x, y):
    pass

def mouseDrag(self, x, y):
    pass

def keyPressed(self, keyCode, modifier):
    if Unit.selectedUnit != None and Unit.selectedUnit.optionsOn:
        menuKeysPressed(self, keyCode, modifier)
    elif Unit.selectedUnit != None and Unit.selectedUnit.drawAttacks:
        attackKeysPressed(self, keyCode, modifier)
    else:
        gameKeyPressed(self, keyCode, modifier)

def attackKeysPressed(self, keyCode, modifier):
    attackList = list(Unit.selectedUnit.attackOptions)
    if keyCode == pygame.K_1:
        enemy = attackList[0]
        Unit.selectedUnit.battle(enemy)
        if enemy.stats["HP"] > 0:
            enemy.battle(Unit.selectedUnit)
            #Double attack if speed is high enough!
            if Unit.selectedUnit.stats["HP"] > 0 and \
             Unit.selectedUnit.stats["Speed"] > (3+enemy.stats["Speed"]):
                Unit.selectedUnit.battle(enemy)

    if keyCode == pygame.K_2:
        enemy = attackList[1]
        Unit.selectedUnit.battle(enemy)
        if enemy.stats["HP"] > 0:
            enemy.battle(Unit.selectedUnit)
            #Double attack if speed is high enough!
            if Unit.selectedUnit.stats["HP"] > 0 and \
             Unit.selectedUnit.stats["Speed"] > (3+enemy.stats["Speed"]):
                Unit.selectedUnit.battle(enemy)

    if keyCode == pygame.K_3 and len(Unit.selectedUnit.optionStr) >= 3:
        enemy = attackList[2]
        Unit.selectedUnit.battle(enemy)
        if enemy.stats["HP"] > 0:
            enemy.battle(Unit.selectedUnit)
            #Double attack if speed is high enough!
            if Unit.selectedUnit.stats["HP"] > 0 and \
             Unit.selectedUnit.stats["Speed"] > (3+enemy.stats["Speed"]):
                Unit.selectedUnit.battle(enemy)

    if keyCode == pygame.K_4 and len(Unit.selectedUnit.optionStr) >= 4:
        enemy = attackList[3]
        Unit.selectedUnit.battle(enemy)
        if enemy.stats["HP"] > 0:
            enemy.battle(Unit.selectedUnit)
            #Double attack if speed is high enough!
            if Unit.selectedUnit.stats["HP"] > 0 and \
             Unit.selectedUnit.stats["Speed"] > (3+enemy.stats["Speed"]):
                Unit.selectedUnit.battle(enemy)

    if keyCode == pygame.K_5 and len(Unit.selectedUnit.optionStr) >= 5:
        enemy = attackList[4]
        Unit.selectedUnit.battle(enemy)
        if enemy.stats["HP"] > 0:
            enemy.battle(Unit.selectedUnit)
            #Double attack if speed is high enough!
            if Unit.selectedUnit.stats["HP"] > 0 and \
             Unit.selectedUnit.stats["Speed"] > (3+enemy.stats["Speed"]):
                Unit.selectedUnit.battle(enemy)

    if keyCode == pygame.K_6 and len(Unit.selectedUnit.optionStr) >= 6:
        enemy = attackList[5]
        Unit.selectedUnit.battle(enemy)
        if enemy.stats["HP"] > 0:
            enemy.battle(Unit.selectedUnit)
            #Double attack if speed is high enough!
            if Unit.selectedUnit.stats["HP"] > 0 and \
             Unit.selectedUnit.stats["Speed"] > (3+enemy.stats["Speed"]):
                Unit.selectedUnit.battle(enemy)

    if keyCode == pygame.K_7 and len(Unit.selectedUnit.optionStr) >= 7:
        enemy = attackList[6]
        Unit.selectedUnit.battle(enemy)
        if enemy.stats["HP"] > 0:
            enemy.battle(Unit.selectedUnit)
            #Double attack if speed is high enough!
            if Unit.selectedUnit.stats["HP"] > 0 and \
             Unit.selectedUnit.stats["Speed"] > (3+enemy.stats["Speed"]):
                Unit.selectedUnit.battle(enemy)

    if keyCode == pygame.K_8 and len(Unit.selectedUnit.optionStr) >= 8:
        enemy = attackList[7]
        Unit.selectedUnit.battle(enemy)
        if enemy.stats["HP"] > 0:
            enemy.battle(Unit.selectedUnit)
            #Double attack if speed is high enough!
            if Unit.selectedUnit.stats["HP"] > 0 and \
             Unit.selectedUnit.stats["Speed"] > (3+enemy.stats["Speed"]):
                Unit.selectedUnit.battle(enemy)

    if keyCode == pygame.K_9 and len(Unit.selectedUnit.optionStr) >= 9:
        enemy = attackList[8]
        Unit.selectedUnit.battle(enemy)
        if enemy.stats["HP"] > 0:
            enemy.battle(Unit.selectedUnit)
            #Double attack if speed is high enough!
            if Unit.selectedUnit.stats["HP"] > 0 and \
             Unit.selectedUnit.stats["Speed"] > (3+enemy.stats["Speed"]):
                Unit.selectedUnit.battle(enemy)

def menuKeysPressed(self, keyCode, modifier):
    if keyCode == pygame.K_1:
        action = Unit.selectedUnit.optionStr[0]
        Unit.selectedUnit.doAction(action, self.grid)
    if keyCode == pygame.K_2:
        action = Unit.selectedUnit.optionStr[1]
        Unit.selectedUnit.doAction(action, self.grid)
    if keyCode == pygame.K_3 and len(Unit.selectedUnit.optionStr) >= 3:
        action = Unit.selectedUnit.optionStr[2]
        Unit.selectedUnit.doAction(action, self.grid)
    if keyCode == pygame.K_4 and len(Unit.selectedUnit.optionStr) >= 4:
        action = Unit.selectedUnit.optionStr[3]
        Unit.selectedUnit.doAction(action, self.grid)


def gameKeyPressed(self, keyCode, modifier):
    if keyCode == pygame.K_x:
        if self.grid[self.curRow][self.curCol].unit != None:
            print(self.grid[self.curRow][self.curCol].unit.stats)

    if keyCode == pygame.K_RIGHT:
        self.curCol += 1
        if self.curCol >= self.cols:
            self.curCol -= 1

    if keyCode == pygame.K_LEFT:
        self.curCol -= 1
        if self.curCol < 0:
            self.curCol += 1
        
    if keyCode == pygame.K_UP:
        self.curRow -= 1
        if self.curRow < 0:
            self.curRow += 1

    if keyCode == pygame.K_DOWN:
        self.curRow += 1
        if self.curRow >= self.rows:
            self.curRow -= 1

    if keyCode == pygame.K_SPACE:
        if Unit.selectedUnit == None:
            if self.grid[self.curRow][self.curCol].unit != None \
            and self.grid[self.curRow][self.curCol].unit.team == "Player" \
                and not self.grid[self.curRow][self.curCol].unit.turnUsed:
                #Selects unit and displays legal moves
                self.grid[self.curRow][self.curCol].unit.select(self.curRow, self.curCol)

        elif (self.curRow, self.curCol) in Unit.selectedUnit.legalRange:
            if (Unit.selectedUnit.position[0], Unit.selectedUnit.position[1]) \
                != (self.curRow, self.curCol):
                self.grid[Unit.selectedUnit.position[0]][Unit.selectedUnit.position[1]].unit = None
                self.grid[self.curRow][self.curCol].unit = Unit.selectedUnit
            Unit.selectedUnit.options(self.curRow, self.curCol, self.grid)

def keyReleased(self, keyCode, modifier):
    pass

def timerFired(self, dt):
    pass