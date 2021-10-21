import pygame as pg
from vec2 import Vec2


class Particle:

	def __init__(self, x, y):
		self.pos = Vec2(x, y)
		self.vel = Vec2(0, 0)
		self.acc = Vec2(0, 0)
		self.color = (255, 255, 255)
		self.size = 5

	def set_pos(self, pos):
		self.pos = pos

	def set_vel(self, vel):
		self.vel = vel

	def set_color(self, color):
		self.color = color

	def set_size(self, size):
		self.size = size

	def apply_force(self, vec):
		self.acc += vec

	def update(self):
		self.vel += self.acc
		self.pos += self.vel
		self.acc *= 0

	def draw(self, surface):
		pg.draw.circle(surface, self.color, self.pos, self.size)


if __name__ == '__main__':
	particle = Particle(5, 5)
