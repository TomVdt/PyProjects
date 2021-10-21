import pygame as pg
from numpy import sqrt


class Point:

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def move(self, dx, dy):
		self.x += dx
		self.y += dy

	def set(self, x, y):
		self.x = x
		self.y = y

	def __repr__(self):
		return f"Point({self.x}, {self.y})"


class Circle(Point):

	def __init__(self, x, y, size):
		super().__init__(x, y)
		self.size = size
		self.selected = False
		self.hovering = False

	def collide(self, mx, my):
		if sqrt((self.x - mx) ** 2 + (self.y - my) ** 2) <= self.size:
			return True
		else:
			return False

	def select(self):
		self.selected = True

	def deselect(self):
		self.selected = False

	def hover(self):
		self.hovering = True

	def dehover(self):
		self.hovering = False

	def draw(self, surface):
		if self.selected:
			pg.draw.circle(surface, (255, 0, 0), (self.x, self.y), self.size, 1)
		elif self.hovering:
			pg.draw.circle(surface, (255, 255, 0), (self.x, self.y), self.size, 1)
		else:
			pg.draw.circle(surface, (255, 255, 255), (self.x, self.y), self.size, 1)