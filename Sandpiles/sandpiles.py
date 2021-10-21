import numpy as np
import pygame
import os
import sys


WIDTH = 100
HEIGHT = 100
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
TILE_WIDTH = int(SCREEN_WIDTH / WIDTH)
TILE_HEIGHT = int(SCREEN_HEIGHT / HEIGHT)

sandpiles = np.zeros((WIDTH, HEIGHT), dtype="int")
sandpiles[int(WIDTH / 2), int(HEIGHT / 2)] = 10000

colors = [(11, 63, 255), (127, 190, 255), (255, 222, 0), (123, 0, 0), (63, 0, 0)]

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
camera = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

os.environ['SDL_VIDEO_CENTERED'] = "1"
pygame.display.set_caption("Sandpiles")


def main():
	run = True
	pause = step = False
	clicking = False
	viewport = Viewport(camera, view_size=(SCREEN_WIDTH, SCREEN_HEIGHT))
	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					run = False
				if event.key == pygame.K_SPACE:
					pause = not pause
				if event.key == pygame.K_RIGHT:
					step = True
			elif event.type == pygame.MOUSEBUTTONDOWN:
				viewport.zoom(event)
				clicking = True
			elif event.type == pygame.MOUSEBUTTONUP:
				clicking = False
			elif event.type == pygame.MOUSEMOTION:
				viewport.move(event, clicking)

		if not pause or step:
			update()
			draw(viewport.zoom_rect)
			step = False

		viewport.update(camera)
		viewport.draw(screen)
		pygame.display.flip()

		clock.tick(60)
		pygame.display.set_caption(f"Sandpiles, fps: {clock.get_fps():.0f}")


def draw(draw_rect):
	for x in range(int(draw_rect.x / TILE_WIDTH), int(draw_rect.x / TILE_WIDTH) + int(draw_rect.width / TILE_WIDTH) + 1):
		for y in range(int(draw_rect.y / TILE_HEIGHT), int(draw_rect.y / TILE_HEIGHT) + int(draw_rect.height / TILE_HEIGHT) + 1):
			pygame.draw.rect(camera, colors[min(sandpiles[x - 1, y - 1], 4)], ((x * TILE_WIDTH, y * TILE_HEIGHT), (TILE_WIDTH, TILE_HEIGHT)))


def update():
	global sandpiles
	nextpiles = np.array(sandpiles)

	for x in range(WIDTH):
		for y in range(HEIGHT):
			if sandpiles[x, y] >= 4:
				nextpiles[x, y] -= 4
				nextpiles[x - 1, y] += 1
				nextpiles[x + 1, y] += 1
				nextpiles[x, y - 1] += 1
				nextpiles[x, y + 1] += 1

	sandpiles = nextpiles


# Shamelessly stolen from https://github.com/iminurnamez/viewport/blob/master/viewport.py and adapted

class Viewport(object):
	"""A simple viewport/camera to handle scrolling and zooming a surface."""

	def __init__(self, base_map, view_size=(600, 600)):
		"""The base_map argument should be a pygame.Surface object.
						Works best with view_size[0] == view_size[1]"""
		self.base_map = base_map
		self.base_rect = self.base_map.get_rect()
		self.zoom_levels = {}
		for i in range(5):
			self.zoom_levels[i] = (self.base_rect.width // 2**i, self.base_rect.height // 2**i)
		self.zoom_level = 0
		self.max_zoom = len(self.zoom_levels) - 1
		self.view_size = view_size
		self.zoom_rect = pygame.Rect((0, 0), self.zoom_levels[self.zoom_level])
		self.scroll([0, 0])

	def scroll(self, offset):
		"""Move self.room_rect by offset and update image."""
		self.zoom_rect.move_ip(offset)
		self.zoom_rect.clamp_ip(self.base_rect)
		self.zoom_image()

	def zoom_image(self):
		"""Set self.zoomed_image to the properly scaled subsurface."""
		subsurface = self.base_map.subsurface(self.zoom_rect)
		self.zoomed_image = pygame.transform.scale(subsurface, self.view_size)

	def get_map_pos(self, screen_pos):
		"""Takes in a tuple of screen coordinates and returns a tuple of
						the screen_position translated to the proper map coordinates
						for the current zoom level."""
		view_width, view_height = self.view_size
		x, y = screen_pos
		x_scale = self.zoom_levels[self.zoom_level][0] / float(view_width)
		y_scale = self.zoom_levels[self.zoom_level][1] / float(view_height)
		mapx = self.zoom_rect.left + (x * x_scale)
		mapy = self.zoom_rect.top + (y * y_scale)
		return mapx, mapy

	def get_zoom_rect(self, mapx, mapy):
		"""Return a Rect of the current zoom resolution centered at mapx, mapy."""
		zoom_rect = pygame.Rect((0, 0), self.zoom_levels[self.zoom_level])
		zoom_rect.center = (int(mapx), int(mapy))
		zoom_rect.clamp_ip(self.base_rect)
		return zoom_rect

	def move(self, event, clicking):
		if clicking:
			offset = [0, 0]
			offset[0] -= event.rel[0] // (self.zoom_level + 1)
			offset[1] -= event.rel[1] // (self.zoom_level + 1)
			if offset != [0, 0]:
				self.scroll(offset)

	def zoom(self, event):
		if event.button == 4:
			if self.zoom_level < self.max_zoom:
				mapx, mapy = self.get_map_pos(event.pos)
				self.zoom_level += 1
				self.zoom_rect = self.get_zoom_rect(mapx, mapy)
				self.zoom_image()

		elif event.button == 5:
			if self.zoom_level > 0:
				mapx, mapy = self.get_map_pos(event.pos)
				self.zoom_level -= 1
				self.zoom_rect = self.get_zoom_rect(mapx, mapy)
				self.zoom_image()

	def update(self, surface=None):
		if surface:
			self.base_map = surface

		self.zoom_image()

	def draw(self, surface):
		surface.blit(self.zoomed_image, (0, 0))


if __name__ == "__main__":
	main()
	pygame.quit()
	sys.exit()
