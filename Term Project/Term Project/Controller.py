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
        moveEnemiesAI(self)

def moveEnemiesAI(self): 
    for row in range(self.rows):
        for col in range(self.cols):
            unit = self.grid[row][col].unit
            if unit != None and unit.team == "Enemy" and not unit.turnUsed:
                unit.position = (row, col)
                attackList = []
                for mRow, mCol in unit.attackMoves:
                    if self.grid[mRow][mCol].unit != None and \
                     self.grid[mRow][mCol].unit.team == "Player":
                        attackList.append(self.grid[mRow][mCol].unit)
                if len(attackList) > 0:
                    weakestUnit = getWeakestUnit(attackList)
                    weakPath = findShortestPath(self, unit, weakestUnit.position, row, col)
                    self.grid[weakPath[1][0]][weakPath[1][1]].unit = unit
                    self.grid[row][col].unit = None
                    unit.battle(weakestUnit, self.grid)
                    if weakestUnit.stats["HP"] > 0:
                        weakestUnit.battle(unit, self.grid)
                        #Double attack if speed is high enough!
                        if unit.stats["HP"] > 0 and \
                         unit.stats["Speed"] > (3+weakestUnit.stats["Speed"]):
                            unit.battle(weakestUnit, self.grid)
                else:
                    paths = []
                    for playerUnit in Unit.teams["Player"]:
                        path = findShortestPath(self, unit, playerUnit.position, row, col)
                        paths.append(path)
                    closestUnitPath = getClosest(paths)
                    for node in closestUnitPath:
                        if node in unit.legalRange and self.grid[node[0]][node[1]].unit == None:
                            unit.position = node
                            self.grid[node[0]][node[1]].unit = unit
                            unit.turnUsed = True
                            self.grid[row][col].unit = None
                            break

    for unit in Unit.teams["Player"]:
        unit.turnUsed = False
    for unit in Unit.teams["Enemy"]:
        unit.turnUsed = False

def getWeakestUnit(aList):
    weakest = None
    for unit in aList:
        if weakest == None or unit.stats["Defense"] < weakest.stats["Defense"]:
            weakest = unit
    return unit

def getClosest(paths):
    shortestPath = None
    for path in paths:
        if path == None:
            continue
        if shortestPath == None or len(path) < len(shortestPath):
            shortestPath = path
    return shortestPath

#Adds possible movement options,
#so long as they are in bounds and are passable by unit
def moveOptions(self, row, col):
    moveOp = []
    dirs = [(1,0) , (0,1), (-1,0), (0,-1)]
    for dRow, dCol in dirs:
        newRow = row+dRow
        newCol = col+dCol
        if newRow < self.rows and newRow >= 0 \
         and newCol < self.cols and newCol >= 0 \
         and self.grid[newRow][newCol].movePenalty != None:
            moveOp.append((newRow, newCol))
    self.grid[row][col].children = moveOp
            

#Note: this implements the a* search algorithm
def findShortestPath(self, enemy, position, row, col, openS=None, closedS=None):
    if closedS == None:
        closedS = set()
        openS = set()
        openS.add((row, col))
    
    while len(openS) != 0:
        curNode = smallestCost(self, openS, position)
        openS.remove(curNode)
        closedS.add(curNode)

        if curNode == position:
            path = []
            path.append(curNode)
            while self.grid[curNode[0]][curNode[1]].parent != None:
                parent = self.grid[curNode[0]][curNode[1]].parent
                path.append(parent.position)
                curNode = parent.position
            Tile.removeParentChild()
            return path

        moveOptions(self, curNode[0], curNode[1])
        for node in self.grid[curNode[0]][curNode[1]].children:
            newG = self.grid[node[0]][node[1]].movePenalty + self.grid[curNode[0]][curNode[1]].gCost()
            if node in closedS: 
                continue
            if (node in openS and self.grid[node[0]][node[1]].gCost() < newG) or node not in openS:
                self.grid[node[0]][node[1]].parent = self.grid[curNode[0]][curNode[1]]
                if node not in openS:
                    openS.add(node)
            

#Finds node w/ smallest f cost  
def smallestCost(self, openS, position):
    fSet = {}
    for node in openS:
        fSet[node] = (fCost(self, node, position))

    lowest = None
    for key in fSet:
        if lowest == None or fSet[key] < fSet[lowest]:
            lowest = key
    return lowest

def fCost(self, node, position):
    g = self.grid[node[0]][node[1]].gCost()
    h = disBtwnNodes(node, position)
    return g + h

def disBtwnNodes(n1, n2):
    xDist = abs(n1[0] - n2[0])
    yDist = abs(n1[1] - n2[1])
    return xDist + yDist

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
    elif Unit.selectedUnit != None and Unit.selectedUnit.inventoryOn:
        inventoryKeysPressed(self, keyCode, modifier)
    else:
        gameKeyPressed(self, keyCode, modifier)

def inventoryKeysPressed(self, keyCode, modifier):
    if keyCode == pygame.K_b:
        Unit.selectedUnit.goBackToOps()

def attackKeysPressed(self, keyCode, modifier):
    attackList = list(Unit.selectedUnit.attackOptions)
    if keyCode == pygame.K_1:
        enemy = attackList[0]
        Unit.selectedUnit.battle(enemy, self.grid)
        if enemy.stats["HP"] > 0:
            enemy.battle(Unit.selectedUnit, self.grid)
            #Double attack if speed is high enough!
            if Unit.selectedUnit.stats["HP"] > 0 and \
             Unit.selectedUnit.stats["Speed"] > (3+enemy.stats["Speed"]):
                Unit.selectedUnit.battle(enemy, self.grid)

    if keyCode == pygame.K_2 and len(Unit.selectedUnit.optionList) >= 2:
        enemy = attackList[1]
        Unit.selectedUnit.battle(enemy, self.grid)
        if enemy.stats["HP"] > 0:
            enemy.battle(Unit.selectedUnit, self.grid)
            #Double attack if speed is high enough!
            if Unit.selectedUnit.stats["HP"] > 0 and \
             Unit.selectedUnit.stats["Speed"] > (3+enemy.stats["Speed"]):
                Unit.selectedUnit.battle(enemy, self.grid)

    if keyCode == pygame.K_3 and len(Unit.selectedUnit.optionList) >= 3:
        enemy = attackList[2]
        Unit.selectedUnit.battle(enemy, self.grid)
        if enemy.stats["HP"] > 0:
            enemy.battle(Unit.selectedUnit, self.grid)
            #Double attack if speed is high enough!
            if Unit.selectedUnit.stats["HP"] > 0 and \
             Unit.selectedUnit.stats["Speed"] > (3+enemy.stats["Speed"]):
                Unit.selectedUnit.battle(enemy, self.grid)

    if keyCode == pygame.K_4 and len(Unit.selectedUnit.optionList) >= 4:
        enemy = attackList[3]
        Unit.selectedUnit.battle(enemy, self.grid)
        if enemy.stats["HP"] > 0:
            enemy.battle(Unit.selectedUnit, self.grid)
            #Double attack if speed is high enough!
            if Unit.selectedUnit.stats["HP"] > 0 and \
             Unit.selectedUnit.stats["Speed"] > (3+enemy.stats["Speed"]):
                Unit.selectedUnit.battle(enemy, self.grid)

    if keyCode == pygame.K_5 and len(Unit.selectedUnit.optionList) >= 5:
        enemy = attackList[4]
        Unit.selectedUnit.battle(enemy, self.grid)
        if enemy.stats["HP"] > 0:
            enemy.battle(Unit.selectedUnit, self.grid)
            #Double attack if speed is high enough!
            if Unit.selectedUnit.stats["HP"] > 0 and \
             Unit.selectedUnit.stats["Speed"] > (3+enemy.stats["Speed"]):
                Unit.selectedUnit.battle(enemy, self.grid)

    if keyCode == pygame.K_6 and len(Unit.selectedUnit.optionList) >= 6:
        enemy = attackList[5]
        Unit.selectedUnit.battle(enemy, self.grid)
        if enemy.stats["HP"] > 0:
            enemy.battle(Unit.selectedUnit, self.grid)
            #Double attack if speed is high enough!
            if Unit.selectedUnit.stats["HP"] > 0 and \
             Unit.selectedUnit.stats["Speed"] > (3+enemy.stats["Speed"]):
                Unit.selectedUnit.battle(enemy, self.grid)

    if keyCode == pygame.K_7 and len(Unit.selectedUnit.optionList) >= 7:
        enemy = attackList[6]
        Unit.selectedUnit.battle(enemy, self.grid)
        if enemy.stats["HP"] > 0:
            enemy.battle(Unit.selectedUnit, self.grid)
            #Double attack if speed is high enough!
            if Unit.selectedUnit.stats["HP"] > 0 and \
             Unit.selectedUnit.stats["Speed"] > (3+enemy.stats["Speed"]):
                Unit.selectedUnit.battle(enemy, self.grid)

    if keyCode == pygame.K_8 and len(Unit.selectedUnit.optionList) >= 8:
        enemy = attackList[7]
        Unit.selectedUnit.battle(enemy, self.grid)
        if enemy.stats["HP"] > 0:
            enemy.battle(Unit.selectedUnit, self.grid)
            #Double attack if speed is high enough!
            if Unit.selectedUnit.stats["HP"] > 0 and \
             Unit.selectedUnit.stats["Speed"] > (3+enemy.stats["Speed"]):
                Unit.selectedUnit.battle(enemy, self.grid)

    if keyCode == pygame.K_9 and len(Unit.selectedUnit.optionList) >= 9:
        enemy = attackList[8]
        Unit.selectedUnit.battle(enemy, self.grid)
        if enemy.stats["HP"] > 0:
            enemy.battle(Unit.selectedUnit, self.grid)
            #Double attack if speed is high enough!
            if Unit.selectedUnit.stats["HP"] > 0 and \
             Unit.selectedUnit.stats["Speed"] > (3+enemy.stats["Speed"]):
                Unit.selectedUnit.battle(enemy, self.grid)
    
    if keyCode == pygame.K_b:
        Unit.selectedUnit.goBackToOps()

def menuKeysPressed(self, keyCode, modifier):
    if keyCode == pygame.K_1:
        action = Unit.selectedUnit.optionList[0]
        Unit.selectedUnit.doAction(action, (self.curRow, self.curCol))
    if keyCode == pygame.K_2:
        action = Unit.selectedUnit.optionList[1]
        Unit.selectedUnit.doAction(action, (self.curRow, self.curCol))
    if keyCode == pygame.K_3 and len(Unit.selectedUnit.optionList) >= 3:
        action = Unit.selectedUnit.optionList[2]
        Unit.selectedUnit.doAction(action, (self.curRow, self.curCol))
    if keyCode == pygame.K_4 and len(Unit.selectedUnit.optionList) >= 4:
        action = Unit.selectedUnit.optionList[3]
        Unit.selectedUnit.doAction(action, (self.curRow, self.curCol))
    if keyCode == pygame.K_b:
        oldRow, oldCol = Unit.selectedUnit.position
        self.grid[oldRow][oldCol].unit = Unit.selectedUnit
        if (oldRow, oldCol) != (self.curRow, self.curCol):
            self.grid[self.curRow][self.curCol].unit = None
        Unit.selectedUnit.goBack()

def gameKeyPressed(self, keyCode, modifier):
    if keyCode == pygame.K_x:
        if self.grid[self.curRow][self.curCol].unit != None:
            print(self.grid[self.curRow][self.curCol].unit.stats)

    if keyCode == pygame.K_z:
        if self.displayEnemyAttacks:
            self.displayEnemyAttacks = False
        else:
            self.displayEnemyAttacks = True

    if keyCode == pygame.K_t:
        if self.drawTime:
            self.drawTime = False
        else:
            self.drawTime = True

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
    if not self.gameOver:
        self.curTime += 4
        if self.curTime == 60:
            self.seconds += 1
            self.curTime = 0
        if self.seconds == 60:
            self.minutes += 1
            self.seconds = 0