import math
import random
from vector import Vector


class Metaball:

    def __init__(self, width, height):
        self.pos = Vector(random.randint(0, width), random.randint(0, height))
        self.radius = random.randint(30, 50)
        self.width = width
        self.height = height
        self.dir = Vector.random2D()
        self.dir.mult(random.randint(2, 5))

    def update(self):
        self.pos.add(self.dir)

        if self.pos.x >= self.width or self.pos.x <= 0:
            self.dir.x *= -1
        if self.pos.y >= self.height or self.pos.y <= 0:
            self.dir.y *= -1
