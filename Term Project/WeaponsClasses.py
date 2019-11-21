class Weapon(object):
    def __init__(self, name, might, hit, crit, wRange, weight):
        self.name = name
        self.might = might
        self.hit = hit
        self.crit = crit
        self.range = wRange
        self.weight = weight

    def __hash__(self):
        return hash(self.name)

class Sword(Weapon):
    def __init__(self, name, might, hit, crit, weight):
        wRange = 1 
        self.type = "Sword"
        super().__init__(name, might, hit, crit, wRange, weight)

class Lance(Weapon):
    def __init__(self, name, might, hit, crit, weight):
        wRange = 1 
        self.type = "Lance"
        super().__init__(name, might, hit, crit, wRange, weight)

class Axe(Weapon):
    def __init__(self, name, might, hit, crit, weight):
        wRange = 1 
        self.type = "Axe"
        super().__init__(name, might, hit, crit, wRange, weight)

class Bow(Weapon):
    def __init__(self, name, might, hit, crit, weight):
        wRange = 2 
        self.type = "Bow"
        super().__init__(name, might, hit, crit, wRange, weight)
  