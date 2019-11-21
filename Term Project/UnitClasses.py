import random, WeaponsClasses

class Unit(object):
    def __init__(self, stats, inventory, skills, position, classWeapons, move):
        self.stats = stats
        self.inventory = inventory
        self.skills = skills
        self.equipped = inventory[0]
        self.position = position
        self.move = move
        self.accuracy = self.stats["Skill"]*1.5 + self.equipped.hit
        self.power = self.stats["Strength"] + self.equipped.might
        self.crit = self.stats["Skill"]/2 + self.equipped.crit
        self.avoid = self.stats["Speed"]*1.5 
        self.attackSpeed = self.stats["Speed"] - self.equipped.weight


    def battle(self, enemy):
        hitChance = self.accuracy - enemy.avoid
        critRate = self.crit - enemy.stats["Luck"]
        if hitChance > 100: hitChance = 100
        battleRoll = random.randint(1,100)
        if battleRoll <= hitChance:
            damage = self.power - enemy.stats["Defense"]
            if damage < 0: damage = 0
            enemy["HP"] = enemy.stats.get["HP"] - damage

class Archer(Unit):
    def __init__(self, stats, inventory, position):
        skills = ["Temp"]
        classWeapons = ["Bow"]
        move = 4
        super().__init__(stats, inventory, skills, position, classWeapons, move)

class Soldier(Unit):
    def __init__(self, stats, inventory, position):
        skills = ["Temp"]
        classWeapons = ["Lance"]
        move = 5
        super().__init__(stats, inventory, skills, position, classWeapons, move)

class Mercenary(Unit):
    def __init__(self, stats, inventory, position):
        skills = ["Temp"]
        classWeapons = ["Sword"]
        move = 5
        super().__init__(stats, inventory, skills, position, classWeapons, move)

class Bandit(Unit):
    def __init__(self, stats, inventory, position):
        skills = ["Temp"]
        classWeapons = ["Axe"]
        move = 4
        super().__init__(stats, inventory, skills, position, classWeapons, move)



