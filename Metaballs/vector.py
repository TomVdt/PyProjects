import math
import random


class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def random2D():
        angle = random.uniform(0, 2 * math.pi)
        return Vector(math.sin(angle), math.cos(angle))

    def mult(self, amount):
        self.x *= amount
        self.y *= amount

    def add(self, vect):
        self.x += vect.x
        self.y += vect.y

    def rotate(self, angle):
        self.x = self.x * math.cos(angle) - self.y * math.sin(angle)
        self.y = self.x * math.sin(angle) + self.y * math.cos(angle)
