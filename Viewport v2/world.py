import pygame as pg
import numpy as np
import os
import sys
import random


# Constants
NAME = "Viewport v2"
WIDTH = 500
HEIGHT = 500
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RANDOM_COLORS = [(208, 155, 171), (191, 8, 173), (96, 156, 9), (235, 110, 239), (43, 182, 160), (116, 199, 94), (152, 168, 18), (66, 54, 252)]


class World:

	def __init__(self):

		# Init pygame, set screen surface, create a clock
		pg.init()
		self.screen = pg.display.set_mode((WIDTH, HEIGHT))
		self.clock = pg.time.Clock()
		os.environ['SDL_VIDEO_CENTERED'] = '1'
		pg.display.set_caption(f"{NAME}")

		# Programm vars
		self.grid = pg.Surface((WIDTH, HEIGHT), flags=pg.SRCALPHA)
		for i in range(0, WIDTH, 25):
			pg.draw.line(self.grid, (128, 128, 128, 128), (i, 0), (i, HEIGHT))
			pg.draw.line(self.grid, (128, 128, 128, 128), (0, i), (WIDTH, i))
		self.viewport = Viewport(self.grid)
		self.controls = {
			pg.K_a: (-1, 0),
			pg.K_d: (1, 0),
			pg.K_w: (0, -1),
			pg.K_s: (0, 1)
		}
		self.world_cursor_pos = np.array((0, 0))
		self.cursor_pos = np.array((0, 0))
		self.player = Player((250, 250), 8)
		self.particles = [Particle((random.randint(0, 500), random.randint(0, 500)), random.randint(0, 5), RANDOM_COLORS[random.randint(0, 7)]) for i in range(100)]
		self.spawn_time = 3000
		self.image = pg.image.load("cat.jpg")

		# Pygame vars
		self.fps = 120
		self.elapsed = 0
		self.pause = False
		self.run = True

		self.main()

	def events(self):
		# All event checks go here
		for event in pg.event.get():
			if event.type == pg.QUIT:
				self.run = False
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					self.run = False
				if event.key == pg.K_LCTRL:
					self.pause = not self.pause
				if event.key == pg.K_0:
					self.viewport.offset *= 0
			elif event.type == pg.MOUSEBUTTONDOWN:
				if event.button == 4:
					self.viewport.zoom(1, self.world_cursor_pos)
				if event.button == 5:
					self.viewport.zoom(-1, self.world_cursor_pos)

		self.cursor_pos = np.array(pg.mouse.get_pos())
		self.world_cursor_pos = self.cursor_pos / self.viewport.zoom_factor + self.viewport.offset

		pressed = pg.key.get_pressed()
		for key in self.controls:
			if pressed[key]:
				self.viewport.offset = self.viewport.offset + (np.array(self.controls[key]) * self.elapsed / self.viewport.zoom_factor)

	def update(self):
		return
		self.spawn_time -= self.elapsed
		if self.spawn_time <= 0 :
			self.spawn_time = random.randint(1000, 5000)
			self.particles.append(Particle((random.randint(0, 500), random.randint(0, 500)), random.randint(1, 4), RANDOM_COLORS[random.randint(0, 7)]))

		for i in range(len(self.particles) - 1, -1, -1):
			if np.linalg.norm(self.player.pos - self.particles[i].pos) <= self.player.r + 2:
				self.player.mass += self.particles[i].value
				self.particles.pop(i)

		self.player.update(self.world_cursor_pos, self.elapsed)
		# Autoscale according to player radius, should always represent 1/10 of the screen
		self.viewport.target_zoom_factor = 250 / (self.player.r * 10)
		self.viewport.offset = self.player.pos - (WIDTH // 2 / self.viewport.zoom_factor)

	def draw(self):
		# Draw everything

		self.screen.fill(WHITE)

		self.screen.blit(self.grid, (-self.viewport.offset % 25).astype(int))

		for part in self.particles:
			part.draw(self.screen, self.viewport.offset)

		self.player.draw(self.screen, self.viewport.offset)

		# self.screen.blit(self.image, -self.viewport.offset)

		self.viewport.update()
		self.viewport.draw(self.screen)

		pg.display.flip()

	def main(self):
		while self.run:
			# Get all events
			self.events()

			# Update if out of pause
			if not self.pause:
				self.update()

			# Always draw
			self.draw()

			# Tick the clock and get the elapsed time (ms), update fps display
			self.elapsed = self.clock.tick(self.fps)
			pg.display.set_caption(f"{NAME}, fps: {self.clock.get_fps():.0f}, paused: {self.pause}, {self.viewport.offset.astype(int)}, {self.viewport.zoom_factor}")


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
		self.zoom_rect = pg.Rect(0, 0, *self.size)
		self.zoom_surf = surface.subsurface(self.zoom_rect)

	def zoom(self, value, point):
		if 1 <= self.target_zoom_factor + value <= 10:
			self.target_zoom_factor += value
			self.offset = self.offset + ((point - self.offset) / self.target_zoom_factor * (value / abs(value)))

			# if value < 0:
			# 	vect = (self.offset - point) / self.target_zoom_factor
			# else:
			# 	vect = -(self.offset - point) / self.target_zoom_factor
			# self.offset = self.offset + vect

	def update(self):
		# TODO: add zoom interpolation
		self.zoom_factor = self.target_zoom_factor

		self.zoom_rect.size = (self.size / self.zoom_factor).astype(int)

	def draw(self, surface):
		self.zoom_surf = surface.subsurface(self.zoom_rect)
		self.zoom_surf = pg.transform.scale(self.zoom_surf, self.size)
		surface.blit(self.zoom_surf, (0, 0))


class Player:

	def __init__(self, pos, mass):
		self.pos = np.array(pos)
		self.mass = mass
		self.r = int(self.mass ** 0.5)

	def update(self, cursor_pos, elapsed):
		vect = cursor_pos - self.pos
		mag = np.linalg.norm(vect)
		if mag != 0:
			heading = vect / mag
		else:
			heading = vect
		mag = min(mag, 25)
		speed = self.mass ** 0.5 / self.mass / 2
		self.pos = self.pos + heading * speed * mag * elapsed / 10
		self.r = int(self.mass ** 0.5)

	def draw(self, surface, offset):
		pg.draw.circle(surface, (25, 255, 42), (self.pos - offset).astype(int), self.r)


class Particle:

	def __init__(self, pos, value, color):
		self.pos = np.array(pos)
		self.value = value
		self.color = color

	def draw(self, surface, offset):
		pg.draw.circle(surface, self.color, (self.pos - offset).astype(int), 1)


if __name__ == "__main__":
	# Start the program
	World()

	# Exit gracefully
	pg.quit()
	sys.exit()
