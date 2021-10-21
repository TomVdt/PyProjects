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

	def __init__(self, x, y, surface):
		self.offset = np.array((x, y))
		self.size = np.array(surface.get_size())
		self._zoom_factor = 1
		self._zoom_rect = pg.Rect(0, 0, *self.size)
		self._zoom_surf = surface.subsurface(self._zoom_rect)

	def _clamp(self, value, mini, maxi):
		return min(max(value, mini), maxi)

	@property
	def rect(self):
		return self._zoom_rect.move(-self.offset).inflate((10, 10))
	
	def move(self, dx, dy):
		self.offset[0] += dx
		self.offset[1] += dy

	def set_offset(self, x, y):
		self.offset = np.array((x, y))

	def zoom(self, value):
		self._zoom_factor = self._clamp(self._zoom_factor + value, 1, 10)

	def update(self):
		center = self._zoom_rect.center
		self._zoom_rect.size = (self.size / self._zoom_factor).astype(int)
		self._zoom_rect.center = center

	def draw(self, surface):
		self._zoom_surf = surface.subsurface(self._zoom_rect)
		self._zoom_surf = pg.transform.scale(self._zoom_surf, self.size)
		surface.blit(self._zoom_surf, (0, 0))



if __name__ == '__main__':
	test = Viewport(0, 0, 50, 50)
	test.move(5, -5)
	print(test.pos)