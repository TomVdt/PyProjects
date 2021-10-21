from vars import *
from vector import Vector


class Planet:

    def __init__(self, x, y, mass):
        self.pos = Vector(x, y)
        self.vel = Vector(0, 0)
        self.acc = Vector(0, 0)
        self.mass = mass
        self.r = math.sqrt(mass)

    def attract(self, pos, mass):
        G = (pos.copy() - self.pos.copy()).normalize()
        self.acc += G * ((self.mass * mass) / Vector.distSq(self.pos, pos))

    def apply_force(self, force):
        f = force.copy()
        self.acc += f / self.mass

    def border(self):
        if self.pos.y >= height - self.r:
            self.pos.y = height - self.r
            self.vel.y *= -1
        elif self.pos.y <= self.r:
            self.pos.y = self.r
            self.vel.y *= -1
        if self.pos.x >= width - self.r:
            self.pos.x = width - self.r
            self.vel.x *= -1
        elif self.pos.x <= self.r:
            self.pos.x = self.r
            self.vel.x *= -1

    def update(self):
        self.vel += self.acc
        self.pos += self.vel
        self.acc *= 0

    def show(self, show_heading=False):
        pygame.draw.circle(camera, (255, 255, 255), (int(self.pos.x), int(self.pos.y)), int(self.r))
        if show_heading:
            pygame.draw.line(camera, (255, 0, 0), (self.pos.x, self.pos.y), (self.pos.x + self.vel.x, self.pos.y + self.vel.y), 3)
