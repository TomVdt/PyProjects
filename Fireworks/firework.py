import random, math, vars
from particle import Particle
from vector import Vector

class Firework:
    def __init__(self, col, width, height, gravity):
        self.color = col
        self.gravity = gravity
        self.firework = Particle(random.randint(0,width), height, self.color, True)
        self.exploded = False
        self.particles = []

    def done(self):
        if self.exploded and len(self.particles) == 1:
            return True
        else:
            return False

    def update(self):
        if not self.exploded:
            self.firework.apply_force(self.gravity)
            self.firework.update()

            if self.firework.vel.y >= 0:
                self.exploded = True
                self.explode()

        for i in range(len(self.particles)-1, 0, -1):
            self.particles[i].apply_force(self.gravity)
            self.particles[i].update()

            if self.particles[i].finished():
                self.particles.pop(i)

    def explode(self):
        for i in range(random.randint(100, 250)):
            self.particles.append(Particle(self.firework.pos.x, self.firework.pos.y, self.color, False))

    def show(self):
        if not self.exploded:
            self.firework.show()
        for i in self.particles:
            i.show()
