import pygame as pg
import numpy as np


class Link:

	def __init__(self, a, b, length, strength):
		self.a = a
		self.b = b
		self.length = length
		self.strength = strength

	def normalize(self, v):
		norm = np.linalg.norm(v)
		if norm == 0:
			return v
		return v / norm

	def update(self):
		force = self.b.pos - self.a.pos
		x = (force[0] ** 2 + force[1] ** 2) ** 0.5 - self.length
		force = self.normalize(force)
		force *= (self.strength * x)
		self.a.apply_force(force)
		self.b.apply_force(-force)

	def show(self, surf):
		pg.draw.line(surf, (255, 255, 255), self.a.pos, self.b.pos)
