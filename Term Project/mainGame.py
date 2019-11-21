###########
#
# Name: Nataniel Arocho-Nieves
# Andrew ID: narochon
#
###########


import pygame, random

from UnitClasses import *
from WeaponsClasses import *

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
            pass

        if keyCode == pygame.K_x:
            for unit in self.players:
                if unit.position == (self.curX, self.curY):
                    print(unit.stats)

        if keyCode == pygame.K_RIGHT:
            self.curX += 1

        if keyCode == pygame.K_LEFT:
            self.curX -= 1
        
        if keyCode == pygame.K_UP:
            self.curY -= 1

        if keyCode == pygame.K_DOWN:
            self.curY += 1

    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt):
        pass

    def redrawAll(self, screen):
        yDist = self.height//self.rows
        xDist = self.width//self.cols
        for row in range(self.rows):
            for col in range(self.cols):
                pygame.draw.rect(screen, self.bgColor, (xDist*col, yDist*row\
                , xDist, yDist))

        pygame.draw.rect(screen, (0, 0 ,0), (xDist*self.curX, yDist*self.curY\
            , xDist, yDist))

        for unit in self.players:
            if unit.stats["HP"] > 0:
                pygame.draw.circle(screen, (  0,   0, 255),(xDist*unit.position[0]+xDist//2\
                    , yDist*unit.position[1]+yDist//2), xDist//2)

        for unit in self.enemies:
            if unit.stats["HP"] > 0:
                pygame.draw.circle(screen, (255,  0,   0),(xDist*unit.position[0]+xDist//2\
                    , yDist*unit.position[1]+yDist//2), xDist//2)

    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

    def __init__(self, width=800, height=800, fps=60, title="112 Pygame Game"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (0, 200, 0)
        self.rows = 10
        self.cols = 10

        self.players = set()
        self.enemies = set()

        tempStats = {"HP": 10, "Strength": 15, "Defense": 10, "Speed": 10, "Skill": 10, "Luck":10}
        archer = Archer(tempStats, [Bow("Temp Bow", 5, 100, 5, 0), 0, 0 ,0, 0], (0,2))
        soldier = Soldier(tempStats, [Lance("Temp Lance", 5, 100, 5, 0), 0, 0, 0, 0], (0,4))
        merc = Mercenary(tempStats, [Sword("Temp Sword", 5, 100, 5, 0), 0, 0, 0, 0], (0,6))
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
            #screen.fill(self.bgColor)
            self.redrawAll(screen)
            pygame.display.flip()
        pygame.quit()


def main():
    game = PygameGame()
    game.run()

if __name__ == '__main__':
    main()