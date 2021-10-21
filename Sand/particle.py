import pygame as pg
import numpy as np



class Particle:

	def __init__(self, x, y):
		self.pos = np.array((x, y))
		self.vel = np.zeros(2, dtype=np.float)
		self.acc = np.zeros(2, dtype=np.float)

	def apply_force(self, force):
		self.acc += force

	def update(self, particles):
		return particles

	def is_fluid(self):
		return False

	def is_air(self):
		return False

class Air(Particle):

	def __init__(self, x, y):
		super().__init__(x, y)
		self.color = (255, 0, 0)

	def is_fluid(self):
		return True

	def is_air(self):
		return True

class Sand(Particle):

	def __init__(self, x, y):
		super().__init__(x, y)
		self.color = (255, 255, 0)

	def update(self, particles):
		pass

class Water(Particle):

	def __init__(self, x, y):
		super().__init__(x, y)
		self.color = (0, 0, 255)

	def is_fluid(self):
		return True

	def update(self, particles):
		pass
