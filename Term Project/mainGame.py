###########
#
# Name: Nataniel Arocho-Nieves
# Andrew ID: narochon
#
###########


import pygame, random, copy

from UnitClasses import *
from WeaponsClasses import *
from TileClass import *
import Controller, View

#Starter code borrowed from 15-112 PyGame optional lecture notes
class PygameGame(object):
    def isKeyPressed(self, key):
        return self._keys.get(key, False)

    def __init__(self, width=800, height=800, fps=60, title="112 Pygame Game"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.rows = 25
        self.cols = 25

        self.grid = []
        for row in range(self.rows):
            newRow = []
            for col in range(self.cols):
                if row in range(0, 3) and col in range(10, 25):
                    newRow.append(Sand(None, (row,col)))
                else: 
                    newRow.append(Field(None, (row,col)))
            self.grid.append(newRow)

        self.grid[16][18] = Mountain(None, (16, 18))
        self.grid[17][17] = Mountain(None, (17, 17))
        self.grid[17][18] = Mountain(None, (17, 18))
        self.grid[17][19] = Mountain(None, (17, 19))
        self.grid[18][17] = Mountain(None, (18, 17))
        self.grid[18][18] = Mountain(None, (18, 18))
        self.grid[18][19] = Mountain(None, (18, 19))
        self.grid[19][18] = Mountain(None, (19, 18))

        tempStats = {"HP": 10, "Strength": 15, "Defense": 10, "Speed": 10, "Skill": 10, "Luck":10}
        archer = Archer("Archer", copy.copy(tempStats), [Bow("Bow", 5, 100, 5, 0), 0, 0 ,0, 0], "Player", (0,0,255))
        soldier = Soldier("Soldier", copy.copy(tempStats), [Lance("Lance", 5, 100, 5, 0), 0, 0, 0, 0], "Player", (0,0,255))
        merc = Mercenary("Merc", copy.copy(tempStats), [Sword("Sword", 5, 100, 5, 0), 0, 0, 0, 0], "Player", (0,0,255))
        bandit = Bandit("Bandit", copy.copy(tempStats), [Axe("Axe", 5, 100, 5, 0), 0 ,0 ,0 ,0], "Player", (0,0,255))
        self.grid[0][2].unit = archer
        self.grid[0][4].unit = soldier
        self.grid[15][15].unit = merc
        self.grid[0][8].unit = bandit

        archer = Archer("Archer", copy.copy(tempStats), [Bow("Bow", 5, 100, 5, 0), 0, 0 ,0, 0], "Enemy", (255,0,0))
        soldier = Soldier("Soldier", copy.copy(tempStats), [Lance("Lance", 5, 100, 5, 0), 0, 0, 0, 0], "Enemy", (255,0,0))
        merc = Mercenary("Merc", copy.copy(tempStats), [Sword("Sword", 5, 100, 5, 0), 0, 0, 0, 0], "Enemy", (255,0,0))
        bandit = Bandit("Bandit", copy.copy(tempStats), [Axe("Axe", 5, 100, 5, 0), 0 ,0 ,0 ,0], "Enemy", (255,0,0))
        self.grid[10][2].unit = archer
        self.grid[10][4].unit = soldier
        self.grid[10][16].unit = merc
        self.grid[10][8].unit = bandit

        self.curRow = 0
        self.curCol = 0


    def run(self):
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()

        playing = True
        while playing:
            Controller.init(self)
            time = clock.tick(self.fps)
            Controller.timerFired(self, time)
            if Controller.isPlayerPhase():
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        Controller.mousePressed(self, *(event.pos))
                    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        Controller.mouseReleased(self, *(event.pos))
                    elif (event.type == pygame.MOUSEMOTION and
                        event.buttons == (0, 0, 0)):
                        Controller.mouseMotion(self, *(event.pos))
                    elif (event.type == pygame.MOUSEMOTION and
                        event.buttons[0] == 1):
                        Controller.mouseDrag(self, *(event.pos))
                    elif event.type == pygame.KEYDOWN:
                         Controller.keyPressed(self, event.key, event.mod)
                    elif event.type == pygame.KEYUP:
                        self._keys[event.key] = False
                        Controller.keyReleased(self, event.key, event.mod)
                    elif event.type == pygame.QUIT:
                        playing = False
            View.redrawAll(self, screen)
            pygame.display.flip()
        pygame.quit()


def main():
    game = PygameGame()
    game.run()

if __name__ == '__main__':
    main()