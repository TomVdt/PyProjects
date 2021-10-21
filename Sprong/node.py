import pygame as pg
import numpy as np


class Node:

	def __init__(self, x, y, anchored=False):
		self.pos = np.array([x, y], dtype=np.float)
		self.vel = np.zeros(2, dtype=np.float)
		self.acc = np.zeros(2, dtype=np.float)
		self.anchored = anchored

	def apply_force(self, force):
		self.acc += np.array(force)

	def update(self):
		if not self.anchored:
			self.vel += self.acc
			self.pos += self.vel
			self.acc *= 0
			self.vel *= 0.99

	def show(self, surf):
		pg.draw.circle(surf, (255, 255, 0), self.pos, 10)
