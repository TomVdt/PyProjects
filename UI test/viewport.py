import pygame as pg
import numpy as np


class Viewport:

	"""
		Object that helps with a 2D camera system
		Params:
		- surface: surface that should get scaled according to zoom_level
		- pos (optional): starting world position of the viewport
		offset represents by how much the world has been moved
		zoom_rect is the portion of the inputed surface that should get scaled to screen size
		zoom_surf is the scaled surface that gets blited on the inputed surface of the draw() method
	"""

	def __init__(self, surface, pos=(0, 0)):
		self.offset = np.array(pos)
		self.size = np.array(surface.get_size())
		self.zoom_factor = 1
		self.target_zoom_factor = 1
		self.zoom_rect = pg.Rect((0, 0), self.size)
		self.zoom_surf = surface.subsurface(self.zoom_rect)

		self.controls = {
			pg.K_w: np.array((0, -1)),
			pg.K_a: np.array((-1, 0)),
			pg.K_s: np.array((0, 1)),
			pg.K_d: np.array((1, 0))
		}

	def get_mouse_pos(self, pos):
		return np.array(pos / self.zoom_factor + self.offset)

	def zoom(self, value, point):
		if 1 <= self.target_zoom_factor + value <= 10:
			self.target_zoom_factor += value
			self.offset = self.offset + ((point - self.offset) / self.target_zoom_factor * (value / abs(value)))

	def scroll(self, offset):
		self.offset = self.offset + offset

	def update(self):
		self.zoom_factor = self.target_zoom_factor

		self.zoom_rect.size = (self.size / self.zoom_factor).astype(int)

	def draw(self, objects, surf):
		for object in objects:
			object.draw(self.offset, surf)

		self.zoom_surf = surf.subsurface(self.zoom_rect)
		self.zoom_surf = pg.transform.scale(self.zoom_surf, self.size)
		surf.blit(self.zoom_surf, (0, 0))
