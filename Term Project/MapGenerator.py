import random
from TileClass import *

#Creates a non-procedurally generated map
def createBasicMap(self):
    grid = []
    for row in range(self.rows):
        newRow = []
        for col in range(self.cols):
            if row in range(0, 3) and col in range(10, 25):
                newRow.append(Sand(None, (row,col)))
            else: 
                newRow.append(Field(None, (row,col)))
        grid.append(newRow)

    grid[16][18] = Mountain(None, (16, 18))
    grid[17][17] = Mountain(None, (17, 17))
    grid[17][18] = Mountain(None, (17, 18))
    grid[17][19] = Mountain(None, (17, 19))
    grid[18][17] = Mountain(None, (18, 17))
    grid[18][18] = Mountain(None, (18, 18))
    grid[18][19] = Mountain(None, (18, 19))
    grid[19][18] = Mountain(None, (19, 18))
    return grid

#procedurally creates a map
def proceduralMap(self):
    grid = []
    for row in range(self.rows):
        newRow = []
        for col in range(self.cols):
            newRow.append(None)
        grid.append(newRow)
    numOfMouns = random.randint(1, 6)
    mounTotal = 0
    for mountain in range(numOfMouns):
        mountainNum = random.randint(2, self.rows)
        mounTotal += mountainNum
        seedRow = random.randint(0, self.rows-1)
        seedCol = random.randint(0, self.cols-1)
        grid = createMountains(self, grid, seedRow, seedCol, mountainNum)
    grid = fieldFill(self, grid)
    if isSolvable(self, grid, mounTotal):
        numOfSand = random.randint(1,4)
        for sand in range(numOfSand):
            fillNum = random.randint(2, 5)
            seedRow = random.randint(0, self.rows-1)
            seedCol = random.randint(0, self.cols-1)
            while grid[seedRow][seedCol].movePenalty == None:
                seedRow = random.randint(0, self.rows-1)
                seedCol = random.randint(0, self.cols-1)
            grid = otherFill(self, grid, seedRow, seedCol, fillNum)
        return grid 
    else:
        return proceduralMap(self)

#Map is solvable if a unit can get to any tile that isn't a mountain
def isSolvable(self, grid, mounTotal):
    totalTiles = self.rows*self.cols
    fieldTotal = 0
    for row in range(self.rows):
        for col in range(self.cols):
            if isinstance(grid[row][col], Field):
                fieldTotal += 1
    return fieldTotal == totalTiles-mounTotal

#creates a mountain based on a seed location 
def createMountains(self, grid, seedRow, seedCol, mountainNum):
    dirs = [(1,0),(0,1),(-1,0),(0,-1)]
    extraDirs = [(1,1),(1,-1),(-1,1),(-1,-1)]
    if mountainNum >= 1:     
        grid[seedRow][seedCol] = Mountain(None, (seedRow, seedCol))
        randDir = None
        while randDir == None or seedRow+randDir[0] not in range(self.rows) or seedCol+randDir[1] \
        not in range(self.cols) or grid[seedRow+randDir[0]][seedCol+randDir[1]] != None:
            randDir = dirs[random.randint(0, 3)]
            if stuck(self, grid, seedRow, seedCol):
                seedRow = random.randint(0, self.rows-1)
                seedCol = random.randint(0, self.cols-1)

        return createMountains(self, grid, seedRow+randDir[0], seedCol+randDir[1], mountainNum-1)
    else:
        return grid

def stuck(self, grid, seedRow, seedCol):
    dirs = [(1,0),(0,1),(-1,0),(0,-1)]
    for dRow, dCol in dirs:
        if seedRow+dRow in range(self.rows) and seedCol+dCol in\
         range(self.cols) and grid[seedRow+dRow][seedCol+dCol] == None:
            return False
    return True

#uses flood fill algorithm to fill map with Field Tiles
def fieldFill(self, grid, position=None):
    dirs = [(1,0),(0,1),(-1,0),(0,-1)]

    if position == None:
        randRow, randCol = random.randint(0, self.rows-1), random.randint(0, self.cols-1)
        while grid[randRow][randCol] != None:
            randRow, randCol = random.randint(0, self.rows-1), random.randint(0, self.cols-1)
        position = (randRow, randCol)
    grid[position[0]][position[1]] = Field(None, (position[0], position[1]))

    for dRow, dCol in dirs:
        newRow, newCol = position[0]+dRow, position[1]+dCol
        if newRow not in range(self.rows) or newCol not in range(self.cols):
            continue
        if grid[newRow][newCol] != None:
            continue
        else:
            grid = fieldFill(self, grid, (newRow, newCol))
    return grid 
    
def otherFill(self, grid, seedRow, seedCol, fillNum):
    dirs = [(1,0),(0,1),(-1,0),(0,-1)]

    if fillNum >= 0:
        grid[seedRow][seedCol] = Sand(None, (seedRow, seedCol))
        for dRow, dCol in dirs: 
            newRow, newCol = seedRow+dRow, seedCol+dCol
            if newRow not in range(self.rows) or newCol not in range(self.cols):
                continue
            if grid[newRow][newCol].movePenalty == None:
                continue
            else:
                grid = otherFill(self, grid, newRow, newCol, fillNum-1)
    return grid