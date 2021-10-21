import random, vars, math
from vector import Vector

class Particle:
    def __init__(self, x, y, col, is_firework):
        self.pos = Vector(x,y)
        self.color = col
        self.lifespan = 1
        self.acc = Vector(0,0)
        self.firework = is_firework
        self.counter = 0
        if self.firework:
            self.vel = Vector(0, -random.uniform(4,10))
        else:
            angle = random.random() * 360
            self.vel = Vector(math.sin(angle),math.cos(angle))
            self.vel.mult(random.uniform(1,15))

    def apply_force(self, vector):
        self.acc.add(vector)

    def update(self):
        if not self.firework:
            self.vel.mult(0.9)
            self.lifespan -= 0.015
            self.acc.rotate(math.sin(self.counter))
            self.counter += 0.4
        self.vel.add(self.acc)
        self.pos.add(self.vel)
        self.acc.mult(0)

    def finished(self):
        if self.lifespan <= 0:
            return True
        else:
            return False

    def show(self):
        if self.firework:
            vars.pygame.draw.circle(vars.screen, self.color, (math.floor(self.pos.x), math.floor(self.pos.y)), 3)
        else:
            vars.pygame.draw.circle(vars.screen, self.color, (math.floor(self.pos.x), math.floor(self.pos.y)), 1)
