from vars import *

class Drop:

    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.caught = False
        self.splat = False
        self.lifespan = 30
        self.size = 7
        self.vel = 0
        self.acc = 0
        self.type = type

    def apply_force(self, force):
        self.acc += force

    def hit_ground(self):
        if self.y >= height:
            self.splat = True
            return True

    def is_caught(self, x, y, w, h):
        if x <= self.x <= x + w and y + h/2 <= self.y <= y + h:
            self.caught = True
            return True
        else:
            return False

    def update(self):
        if not self.splat:
            self.vel += self.acc
            self.y += self.vel
            self.acc = 0
        elif self.lifespan >= 0:
            self.lifespan -= 1
            self.size += 1

    def show(self):
        if self.type == 'egg':
            pygame.draw.circle(screen, (255,255,255), (self.x, int(self.y)), int(self.size))
        elif self.type == 'poop':
            pygame.draw.circle(screen, (102, 51, 0 ), (self.x, int(self.y)), int(self.size))
        elif self.type == 'gold_egg':
            pygame.draw.circle(screen, (255, 153, 0), (self.x, int(self.y)), int(self.size))
