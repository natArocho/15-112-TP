import random, pygame, WeaponsClasses, TileClass

class Unit(object):
    selectedUnit = None
    teams = {}
    def __init__(self, stats, inventory, skills, classWeapons, move, team, color):
        if Unit.teams.get(team, 0) == 0:
            Unit.teams[team] = [self]
        else:
            Unit.teams[team].append(self)

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

    def battle(self, enemy):
        hitChance = self.accuracy - enemy.avoid
        critRate = self.crit - enemy.stats["Luck"]
        if hitChance > 100: hitChance = 100
        battleRoll = random.randint(1,100)
        if battleRoll <= hitChance:
            damage = self.power - enemy.stats["Defense"]
            if damage < 0: damage = 0
            enemy.stats["HP"] = enemy.stats.get("HP", 0) - damage
        self.turnUsed = True
        self.drawAttacks = False
        self.wait()

    #Sets movement and attack range
    def setLegalMovesAndAttack(self, position, grid):
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
        for dRow in range(self.equipped.range+1):
            for dCol in range(self.equipped.range+1):
                distance = dRow+dCol
                if grid[newX+dRow][newY+dCol].unit != None and distance <= self.equipped.range\
                and grid[newX+dRow][newY+dCol].unit.team != self.team:
                    self.attackOptions.add(grid[newX+dRow][newY+dCol].unit)
                    if "Attack" not in options: options.insert(0, "Attack")
        print(options)
        self.optionStr = options
        self.optionsOn = True

    def drawOptions(self, screen, xDist, yDist, row, col):
        pygame.draw.rect(screen, (198, 157, 77), (xDist*col, yDist*row, xDist*2.5, yDist*len(self.optionStr)))


    def drawAttackMenu(self, screen, xDist, yDist, row, col):
        attackList = list(self.attackOptions)
        pygame.draw.rect(screen, (198, 157, 77), (xDist*col, yDist*row, xDist*2.5, yDist*len(attackList)))

    def doAction(self, action, grid):
        if action == "Attack":
            self.drawAttacks = True
            self.optionsOn = False
        elif action == "Trade":
            #UNFINISHED
            self.trade()
        elif action == "Item":
            #UNFINISHED
            self.checkInvo()
        elif action == "Wait":
            self.optionsOn = False
            self.wait()

    def checkInvo(self):
        pass

    def trade(self):
        pass

    def wait(self):
        self.selected = False
        Unit.selectedUnit = None
        self.turnUsed = True

class Archer(Unit):
    def __init__(self, stats, inventory, team, color):
        skills = ["Temp"]
        classWeapons = ["Bow"]
        move = 4
        super().__init__(stats, inventory, skills, classWeapons, move, team, color)

class Soldier(Unit):
    def __init__(self, stats, inventory, team, color):
        skills = ["Temp"]
        classWeapons = ["Lance"]
        move = 5
        super().__init__(stats, inventory, skills, classWeapons, move, team, color)

class Mercenary(Unit):
    def __init__(self, stats, inventory, team, color):
        skills = ["Temp"]
        classWeapons = ["Sword"]
        move = 5
        super().__init__(stats, inventory, skills, classWeapons, move, team, color)

class Bandit(Unit):
    def __init__(self, stats, inventory, team, color):
        skills = ["Temp"]
        classWeapons = ["Axe"]
        move = 4
        super().__init__(stats, inventory, skills, classWeapons, move, team, color)



