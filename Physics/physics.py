import numpy as np
import math
import pygame
import os
import sys


SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


class PhysicsObject:

	def __init__(self, x, y, w, h, mass=1):
		self.vel = np.zeros(2)
		self.acc = np.zeros(2)
		self.mass = mass

		self.rect = pygame.Rect(x, y, w, h)

		self.selected = False
		self.stick_point = np.zeros(2)

	def gravity(self, g):
		self.acc[1] += g

	def stick(self, point):
		dist = ((point[0] - self.rect.center[0]) ** 2 + (point[1] - self.rect.center[1]) ** 2) ** 0.5
		norm = pygame.math.Vector2(point[0] - self.rect.center[0], point[1] - self.rect.center[1])
		if norm.length() != 0:
			norm.normalize_ip()
		self.acc += norm * dist ** 0.5
		self.stick_point = point

	def update(self):
		self.vel += self.acc
		self.rect.center += self.vel.astype(np.int32)
		self.acc *= 0
		self.vel *= 0.99

		if not self.selected:
			if self.rect.top <= 0:
				self.vel[1] *= -1
				self.rect.top = 0

			if self.rect.bottom >= SCREEN_HEIGHT:
				self.vel[1] *= -1
				self.rect.bottom = SCREEN_HEIGHT

			if self.rect.left <= 0:
				self.vel[0] *= -1
				self.rect.left = 0

			if self.rect.right >= SCREEN_WIDTH:
				self.vel[0] *= -1
				self.rect.right = SCREEN_WIDTH

	def draw(self, surf):
		pygame.draw.rect(surf, BLACK if not self.selected else RED, self.rect)
		if self.selected:
			pygame.draw.line(surf, RED, self.rect.center, self.stick_point.astype(np.int32))


class Pendulum:

	def __init__(self, x, y, length, theta, angular_vel=0, size=10):
		self.bob_size = size
		self.origin = np.array((x, y))
		self.bob_pos = np.array((math.cos(theta), math.sin(theta))) * length + self.origin
		self.length = length
		self.angle = theta
		self.ang_vel = angular_vel

		self.vel = np.zeros(2)
		self.acc = np.zeros(2)

		self.rect = pygame.Rect(self.bob_pos - (self.bob_size / 2), (self.bob_size, self.bob_size))
		self.selected = False

	def gravity(self, g):
		self.acc[1] += g

	def update(self):
		pass

	def draw(self, surf):
		pygame.draw.line(surf, BLACK, self.origin, self.bob_pos)
		pygame.draw.circle(surf, BLACK, self.bob_pos.astype(np.int32), self.bob_size)


class World:

	def __init__(self, fps=60):

		self.pause = False
		self.mouse_click = False
		self.mouse_move = False
		self.mouse_rel = np.zeros(2)
		self.mouse_pos = np.zeros(2)
		self.world_mouse_pos = np.zeros(2)
		self.mouse_scroll = 0  # 1 is scroll in, -1 is scroll out
		self.is_selecting = False

		self.run = True
		self.fps = fps

		pygame.init()
		self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		self.view_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
		self.grid_surface = pygame.Surface(
			(SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
		self.clock = pygame.time.Clock()

		for x, y in zip(range(SCREEN_WIDTH // 10), range(SCREEN_HEIGHT // 10)):
			pygame.draw.line(self.grid_surface, (127, 127, 127), (x * 10, 0), (x * 10, SCREEN_HEIGHT))
			pygame.draw.line(self.grid_surface, (127, 127, 127), (0, y * 10), (SCREEN_WIDTH, y * 10))

		os.environ['SDL_VIDEO_CENTERED'] = "1"
		pygame.display.set_caption("Physics")

		self.viewport = Viewport(
			self.view_surface, view_size=(SCREEN_WIDTH, SCREEN_HEIGHT))

		self.physics_objects = [Pendulum(250, 0, 100, 0)]  # [PhysicsObject(250, 250, 20, 20)]

		self.main()

	def events(self):
		self.mouse_move = False
		self.mouse_rel *= 0
		self.mouse_scroll = 0
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.run = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.run = False
				if event.key == pygame.K_SPACE:
					self.pause = not self.pause
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					self.mouse_click = True
				elif event.button == 4:
					self.mouse_scroll = 1
				elif event.button == 5:
					self.mouse_scroll = -1
			elif event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1:
					self.mouse_click = False
			elif event.type == pygame.MOUSEMOTION:
				self.mouse_move = True
				self.mouse_pos = np.array(event.pos)
				self.world_mouse_pos = np.array(self.mouse_pos) / (2 ** self.viewport.zoom_level) + self.viewport.zoom_rect.topleft
				self.mouse_rel = np.array(event.rel)

	def update(self):
		if self.mouse_click and self.mouse_move and not self.is_selecting:
			self.viewport.move(self.mouse_rel)

		if self.mouse_scroll != 0:
			self.viewport.zoom(self.mouse_scroll, self.mouse_pos)

		if not self.pause:
			for i in range(len(self.physics_objects)):
				self.physics_objects[i].gravity(2)
				if self.mouse_click:
					if self.physics_objects[i].rect.collidepoint(self.world_mouse_pos.astype(np.int32)):
						self.physics_objects[i].selected = True
						self.is_selecting = True
					if self.physics_objects[i].selected:
						self.physics_objects[i].stick(self.world_mouse_pos)
				elif self.physics_objects[i].selected:
					self.physics_objects[i].selected = False
					self.is_selecting = False
				self.physics_objects[i].update()

	def draw(self):
		"""
				Viewport boundaries (in global pixels):
										viewport.zoom_rect.x 	 viewport.zoom_rect.x + viewport.zoom_rect.width + 1
				viewport.zoom_rect.y 	-------------------------
										|						|
										|						|
										|						|
										|						|
										|						|
										-------------------------
				viewport.zoom_rect.y + viewport.zoom_rect.height + 1
		"""

		self.view_surface.fill(WHITE)
		self.view_surface.blit(self.grid_surface, (0, 0))

		for i in self.physics_objects:
			i.draw(self.view_surface)

		self.viewport.update(self.view_surface)
		self.viewport.draw(self.screen)
		pygame.display.flip()

	def main(self):
		while self.run:
			self.events()

			self.update()

			self.draw()

			self.clock.tick(self.fps)
			pygame.display.set_caption(f"Physics, fps: {self.clock.get_fps():.0f}, paused: {self.pause}")


# Shamelessly stolen from https://github.com/iminurnamez/viewport/blob/master/viewport.py and adapted


class Viewport(object):
	"""A simple viewport/camera to handle scrolling and zooming a surface."""

	def __init__(self, base_map, view_size=(600, 600)):
		"""The base_map argument should be a pygame.Surface object.
										Works best with view_size[0] == view_size[1]"""
		self.base_map = base_map
		self.base_rect = self.base_map.get_rect()
		self.zoom_levels = {}
		for i in range(3):
			self.zoom_levels[i] = (
				self.base_rect.width // 2**i, self.base_rect.height // 2**i)
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

	def move(self, rel):
		offset = [0, 0]
		offset[0] -= rel[0] // (self.zoom_level + 1)
		offset[1] -= rel[1] // (self.zoom_level + 1)
		if offset != [0, 0]:
			self.scroll(offset)

	def zoom(self, direction, pos):
		if direction == 1:
			if self.zoom_level < self.max_zoom:
				mapx, mapy = self.get_map_pos(pos)
				self.zoom_level += 1
				self.zoom_rect = self.get_zoom_rect(mapx, mapy)
				self.zoom_image()

		elif direction == -1:
			if self.zoom_level > 0:
				mapx, mapy = self.get_map_pos(pos)
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
	World()
	pygame.quit()
	sys.exit()
