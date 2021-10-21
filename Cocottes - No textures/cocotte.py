from vars import *
from drop import Drop

class Cocotte:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 40
        self.pondu = []

    def pondre(self, weights = [70,20,5]):
        roll = random.choices([0,1,2], weights)[0]
        if roll == 0:
            self.pondu.append(Drop(self.x, self.y, 'egg'))
        elif roll == 1:
            self.pondu.append(Drop(self.x, self.y, 'poop'))
        elif roll == 2:
            self.pondu.append(Drop(self.x, self.y, 'gold_egg'))

    def get_caught(self, x, y, w, h):
        for i in self.pondu:
            if i.is_caught(x, y, w, h):
                return i.type

    def update(self, force):
        for i in self.pondu:
            i.apply_force(force)
            i.update()
            if (i.hit_ground() and i.lifespan < 0) or i.caught:
                self.pondu.pop(0)

    def show(self):
        for i in self.pondu:
            i.show()
        pygame.draw.rect(screen, (255,255,255), ((self.x - self.size, self.y - self.size), (self.size * 2, self.size * 2)))
