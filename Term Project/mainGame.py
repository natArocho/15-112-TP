###########
#
# Name: Nataniel Arocho-Nieves
# Andrew ID: narochon
#
###########


import pygame, random

from UnitClasses import *
from WeaponsClasses import *
from TileClass import *

#Starter code borrowed from 15-112 PyGame optional lecture notes
class PygameGame(object):

    def init(self):
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
        if keyCode == pygame.K_SPACE:
            if Unit.selectedUnit == None:
                for unit in self.players:
                    if unit.position == (self.curX, self.curY):
                        unit.select()
            else:
                if (self.curX, self.curY) in Unit.selectedUnit.legalMoves(self.cols, self.rows):
                    Unit.selectedUnit.options(self.curX, self.curY)

        if keyCode == pygame.K_x:
            for unit in self.players:
                if unit.position == (self.curX, self.curY):
                    print(unit.stats)

        if keyCode == pygame.K_RIGHT:
            self.curX += 1
            if self.curX >= self.cols:
                self.curX -= 1

        if keyCode == pygame.K_LEFT:
            self.curX -= 1
            if self.curX < 0:
                self.curX += 1
        
        if keyCode == pygame.K_UP:
            self.curY -= 1
            if self.curY < 0:
                self.curY += 1

        if keyCode == pygame.K_DOWN:
            self.curY += 1
            if self.curY >= self.rows:
                self.curY -= 1

    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt):
        pass

    def redrawAll(self, screen):
        yDist = self.height//self.rows
        xDist = self.width//self.cols
        for row in range(self.rows):
            for col in range(self.cols):
                pygame.draw.rect(screen, self.grid[row][col].tileSprite, (xDist*col, yDist*row\
                , xDist, yDist))

        for unit in self.players:
            if unit.stats["HP"] > 0:
                pygame.draw.circle(screen, (  0,   0, 255),(xDist*unit.position[0]+xDist//2\
                    , yDist*unit.position[1]+yDist//2), xDist//2)
                if unit.selected:
                    for move in unit.legalMoves(self.cols, self.rows):
                        if move !=  unit.position  :
                            pygame.draw.rect(screen, (0,0,255), \
                            (xDist*move[0], yDist*move[1], xDist, yDist))

        for unit in self.enemies:
            if unit.stats["HP"] > 0:
                pygame.draw.circle(screen, (255,  0,   0),(xDist*unit.position[0]+xDist//2\
                    , yDist*unit.position[1]+yDist//2), xDist//2)

        pygame.draw.line(screen, (255, 255 ,0), (xDist*self.curX, yDist*self.curY), \
            (xDist*self.curX+xDist, yDist*self.curY), 5)
        pygame.draw.line(screen, (255, 255 ,0), (xDist*self.curX+xDist, yDist*self.curY), \
            (xDist*self.curX+xDist, yDist*self.curY+xDist), 5)
        pygame.draw.line(screen, (255, 255 ,0), (xDist*self.curX+xDist, yDist*self.curY+yDist), \
            (xDist*self.curX, yDist*self.curY+yDist), 5)
        pygame.draw.line(screen, (255, 255 ,0), (xDist*self.curX, yDist*self.curY+yDist), \
            (xDist*self.curX, yDist*self.curY), 5)

    def isKeyPressed(self, key):
        return self._keys.get(key, False)

    def __init__(self, width=800, height=800, fps=60, title="112 Pygame Game"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.rows = 25
        self.cols = 25

        self.players = set()
        self.enemies = set()

        tempStats = {"HP": 10, "Strength": 15, "Defense": 10, "Speed": 10, "Skill": 10, "Luck":10}
        archer = Archer(tempStats, [Bow("Temp Bow", 5, 100, 5, 0), 0, 0 ,0, 0], (0,2))
        soldier = Soldier(tempStats, [Lance("Temp Lance", 5, 100, 5, 0), 0, 0, 0, 0], (0,4))
        merc = Mercenary(tempStats, [Sword("Temp Sword", 5, 100, 5, 0), 0, 0, 0, 0], (15,15))
        bandit = Bandit(tempStats, [Axe("Temp Axe", 5, 100, 5, 0), 0 ,0 ,0 ,0], (0,8))
        self.players.add(archer)
        self.players.add(soldier)
        self.players.add(merc)
        self.players.add(bandit)

        archer = Archer(tempStats, [Bow("Temp Bow", 5, 100, 5, 0), 0, 0 ,0, 0], (9,2))
        soldier = Soldier(tempStats, [Lance("Temp Lance", 5, 100, 5, 0), 0, 0, 0, 0], (9,4))
        merc = Mercenary(tempStats, [Sword("Temp Sword", 5, 100, 5, 0), 0, 0, 0, 0], (9,6))
        bandit = Bandit(tempStats, [Axe("Temp Axe", 5, 100, 5, 0), 0 ,0 ,0 ,0], (9,8))
        self.enemies.add(archer)
        self.enemies.add(soldier)
        self.enemies.add(merc)
        self.enemies.add(bandit)

        self.curX = 0
        self.curY = 0
        
        self.grid = []
        for row in range(self.rows):
            newRow = []
            for col in range(self.cols):
                newRow.append(Field())
            self.grid.append(newRow)

    def run(self):
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        self.init()
        playing = True
        while playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    playing = False
            self.redrawAll(screen)
            pygame.display.flip()
        pygame.quit()


def main():
    game = PygameGame()
    game.run()

if __name__ == '__main__':
    main()