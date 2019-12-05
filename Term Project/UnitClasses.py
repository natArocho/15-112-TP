import random, pygame
from WeaponsClasses import * 
from TileClass import *

class Unit(object):

    selectedUnit = None
    teams = {}
    xDist = None
    yDist = None

    def __init__(self, name, stats, inventory, skills, classWeapons, move, team, color):
        if Unit.teams.get(team, 0) == 0:
            Unit.teams[team] = [self]
        else:
            Unit.teams[team].append(self)

        self.name = name
        self.stats = stats
        self.inventory = inventory
        self.skills = skills
        self.equipped = inventory[0]
        self.move = move
        self.accuracy = self.stats["Skill"]*1.5 + self.equipped.hit
        self.power = self.stats["Strength"] + self.equipped.might
        self.crit = self.stats["Skill"]/2 + self.equipped.crit
        self.avoid = self.stats["Speed"]*1.5 
        self.attackSpeed = self.stats["Speed"] - self.equipped.weight
        self.selected = False
        self.team = team
        self.color = color
        self.turnUsed = False
        self.tradeOptions = set()
        self.attackOptions = set()
        self.optionsOn = False
        self.drawAttacks = False
        self.inventoryOn = False

    def __eq__(self, other):
        return isinstance(other, Unit) and self.name == other.name

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def battle(self, enemy, grid):
        pAvoBuff, pDefBuf = Unit.applyBuffs(self, grid)
        eAvoBuff, eDefBuf = Unit.applyBuffs(enemy, grid)

        hitChance = self.accuracy + pAvoBuff - enemy.avoid - eAvoBuff 
        critRate = self.crit - enemy.stats["Luck"]
        if hitChance > 100: hitChance = 100
        battleRoll = random.randint(1,100)
        if battleRoll <= hitChance:
            damage = self.power + pDefBuf - enemy.stats["Defense"] - eDefBuf
            if damage < 0: damage = 0
            enemy.stats["HP"] = enemy.stats.get("HP", 0) - damage
        self.turnUsed = True
        self.drawAttacks = False
        self.wait()

    @staticmethod
    def applyBuffs(unit, grid):
        avoBuff = 0
        defBuff = 0

        if grid[unit.position[0]][unit.position[1]].sideEffects != None:
            if grid[unit.position[0]][unit.position[1]].sideEffects[0] == "Avoid":
                avoBuff = grid[unit.position[0]][unit.position[1]].sideEffects[1]

            if grid[unit.position[0]][unit.position[1]].sideEffects[0] == "Protection":
                defBuff = grid[unit.position[0]][unit.position[1]].sideEffects[1]

        return avoBuff, defBuff

    #Sets movement and attack range
    def setLegalMovesAndAttack(self, position, grid):
        self.position = position
        self.legalRange = self.legalMoves(position, grid, self.move)
        self.attackMoves = self.attackRange(position, grid)

    #Legal moves are calculated recursively, by going in all 4 directions
    #from each tile until you can make no more moves
    def legalMoves(self, position, grid, movesLeft, legalMoves = None):
        if legalMoves == None:
            legalMoves = set()
            legalMoves.add(position)
        dirs = [(0, 1), (1, 0), (0,-1), (-1,0)]

        curRow, curCol = position[0], position[1]
        for dRow, dCol in dirs:
            newRow = dRow + curRow
            newCol = dCol + curCol
            if newRow >= len(grid) or newRow < 0 or newCol >= len(grid[0])  \
                or newCol < 0:
                continue
            newTile = grid[newRow][newCol]
            if newTile.movePenalty == None:
                continue
            newMoves = movesLeft - newTile.movePenalty
            if newMoves < 0 or (newTile.unit != None and newTile.unit.team != self.team):
                continue
            else:
                legalMoves.add((newRow, newCol))
                legalMoves | self.legalMoves((newRow, newCol), grid, newMoves, legalMoves)

        return legalMoves

    #Note: Attack Range is just movement range but w/ 
    # the weapon's attack range considered, it also
    # does not mind if units are in a tile
    def attackRange(self, position, grid, movesLeft = None, attackRange=None):
        if attackRange == None:
            attackRange = set()
            attackRange.add(position)
            movesLeft = self.move + self.equipped.range

        dirs = [(0, 1), (1, 0), (0,-1), (-1,0)]
        curRow, curCol = position[0], position[1]
        for dRow, dCol in dirs:
            newRow = dRow + curRow
            newCol = dCol + curCol
            if newRow >= len(grid) or newRow < 0 or newCol >= len(grid[0])  \
                or newCol < 0:
                continue
            newTile = grid[newRow][newCol]
            if newTile.movePenalty == None:
                attackRange.add((newRow, newCol))
                continue
            newMoves = movesLeft - newTile.movePenalty
            if newMoves == 0:
                attackRange.add((newRow, newCol))
                continue
            if newMoves < 0:
                if newTile.movePenalty > 1:
                    attackRange.add((newRow, newCol))
                continue
            if newTile.unit != None and newTile.unit.team != self.team:
                attackRange.add((newRow, newCol))
                continue
            else:
                attackRange.add((newRow, newCol))
                attackRange | self.attackRange((newRow, newCol), grid, newMoves, attackRange)

        return attackRange

    def select(self, newRow, newCol):
        self.tradeOptions = set()
        self.attackOptions = set()
        self.selected = True
        Unit.selectedUnit = self
        self.position = (newRow, newCol)

    #Displays the options a unit can take
    def options(self, newX, newY, grid):
        options = ["Items", "Wait"]
        dirs = [(0, 1), (1, 0), (0,-1), (-1,0)]
        for dRow, dCol in dirs:
            if grid[newX+dRow][newY+dCol].unit != None \
            and grid[newX+dRow][newY+dCol].unit.team == self.team:
                self.tradeOptions.add(grid[newX+dRow][newY+dCol].unit)
                if "Trade" not in options: options.insert(0, "Trade")

        for dRow in range(-1*self.equipped.range, self.equipped.range+1):
            for dCol in range(-1*self.equipped.range, self.equipped.range+1):
                distance = abs(dRow+dCol)
                if grid[newX+dRow][newY+dCol].unit != None and distance <= self.equipped.range\
                and grid[newX+dRow][newY+dCol].unit.team != self.team:
                    self.attackOptions.add(grid[newX+dRow][newY+dCol].unit)
                    if "Attack" not in options: options.insert(0, "Attack")

        self.optionList = options
        self.optionsOn = True

    def drawOptions(self, screen, xDist, yDist, row, col):
        pygame.draw.rect(screen, (198, 157, 77), (xDist*col, yDist*row, xDist*2.5, yDist*len(self.optionList)))
        for i in range(len(self.optionList)):
            self.drawFont(screen, str(i+1)+": "+self.optionList[i], (xDist*col, yDist*(row+i)))

    def drawFont(self, screen, text, location):
        pygame.font.init()
        textFont = pygame.font.SysFont("Arial", 20)
        textSurface = textFont.render(text, True, (0,0,0))
        screen.blit(textSurface, location)

    def drawAttackMenu(self, screen, xDist, yDist, row, col):
        attackList = list(self.attackOptions)
        pygame.draw.rect(screen, (198, 157, 77), (xDist*col, yDist*row, xDist*2.5, yDist*len(attackList)))
        for i in range(len(list(attackList))):
            self.drawFont(screen, str(i+1)+": "+attackList[i].name, (xDist*col, yDist*(row+i)))

    def drawInventory(self, screen, xDist, yDist, row, col):
        pygame.draw.rect(screen, (198, 157, 77), (xDist*col, yDist*row, xDist*2.5, yDist*len(self.inventory)))
        for i in range(len(self.inventory)):
            if isinstance(self.inventory[i], Weapon):
                self.drawFont(screen, str(i+1)+": "+self.inventory[i].name, (xDist*col, yDist*(row+i)))
            else:
                 self.drawFont(screen, str(i+1)+": ", (xDist*col, yDist*(row+i)))

    def doAction(self, action, newPos):
        if action == "Attack":
            self.drawAttacks = True
            self.optionsOn = False
        elif action == "Trade":
            #UNFINISHED
            self.trade()
        elif action == "Items":
            self.inventoryOn = True
            self.optionsOn = False
        elif action == "Wait":
            self.postion = newPos
            self.optionsOn = False
            self.wait()

    def trade(self):
        pass

    def goBackToOps(self):
        self.inventoryOn = False
        self.optionsOn = True
        self.drawAttacks = False

    def goBack(self):        
        self.optionsOn = False
        self.selected = False
        Unit.selectedUnit = None

    def wait(self):
        self.selected = False
        Unit.selectedUnit = None
        self.turnUsed = True

class Archer(Unit):
    
    playerSprite = None
    enemySprite = None

    def __init__(self, name, stats, inventory, team, color):
        skills = ["Temp"]
        classWeapons = ["Bow"]
        move = 4
        super().__init__(name, stats, inventory, skills, classWeapons, move, team, color)

class Soldier(Unit):
    
    playerSprite = None
    enemySprite = None

    def __init__(self, name, stats, inventory, team, color):
        skills = ["Temp"]
        classWeapons = ["Lance"]
        move = 5
        super().__init__(name, stats, inventory, skills, classWeapons, move, team, color)

class Mercenary(Unit):

    playerSprite = None
    enemySprite = None

    def __init__(self, name, stats, inventory, team, color):
        skills = ["Temp"]
        classWeapons = ["Sword"]
        move = 5
        super().__init__(name, stats, inventory, skills, classWeapons, move, team, color)

class Bandit(Unit):
    
    playerSprite = None
    enemySprite = None

    def __init__(self, name, stats, inventory, team, color):
        skills = ["Temp"]
        classWeapons = ["Axe"]
        move = 4
        super().__init__(name, stats, inventory, skills, classWeapons, move, team, color)



