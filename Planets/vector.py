import math
import random


class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def copy(self):
        return Vector(self.x, self.y)

    def __str__(self):
        return "Vector ({}, {})".format(str(self.x), str(self.y))

    def __getitem__(self, i):
        if i == 0:
            return self.x
        elif i == 1:
            return self.y
        else:
            raise IndexError("Index out of range")

    def __mul__(self, a):
        self.x *= a
        self.y *= a
        return self

    def __truediv__(self, a):
        self.x /= a
        self.y /= a
        return self

    def __add__(self, vect):
        self.x += vect.x
        self.y += vect.y
        return self

    def __sub__(self, vect):
        self.x -= vect.x
        self.y -= vect.y
        return self

    def dot(self, vect):
        return self.x * vect.x + self.y * vect.y

    def cross(self, vect):
        print("idk, do it yourself")

    def random2D():
        angle = random.uniform(0, 2 * math.pi)
        return Vector(math.sin(angle), math.cos(angle))

    def rotate(self, angle):
        self.x = self.x * math.cos(angle) - self.y * math.sin(angle)
        self.y = self.x * math.sin(angle) + self.y * math.cos(angle)
        return self

    def set_angle(self, angle):
        self.x = self.x * math.cos(angle) - self.y * math.sin(angle)
        self.y = self.x * math.sin(angle) + self.y * math.cos(angle)
        return self

    def set(self, x, y):
        self.x = x
        self.y = y

    def normalize(self):
        len = math.sqrt(self.x**2 + self.y**2)
        self.x /= len
        self.y /= len
        return self

    def set_mag(self, a):
        normalized = self.normalize()
        self.x = normalized.x * a
        self.y = normalized.y * a
        return self

    def get_mag(self):
        return math.sqrt(self.x**2 + self.y**2)

    def limit(self, value):
        if self.get_mag() > value:
            self.set_mag(value)
        return self

    def lerp(self, vect, value):
        self.x += (vect.x - self.x) * value
        self.y += (vect.y - self.y) * value
        return self

    def dist(p1, p2):
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

    def distSq(p1, p2):
        return (p1.x - p2.x)**2 + (p1.y - p2.y)**2


# Testing area
if __name__ == "__main__":
    v = Vector(2, 1.5)
    a = Vector(0, 1)
    b = Vector(25, 5)

    print(v)
    print(v.normalize())
    print(v.set_mag(5))
    print(v[1])
