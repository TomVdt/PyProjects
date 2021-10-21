import pygame as pg
import numpy as np
from itertools import product
import particle
import os
import sys

# Constants
NAME = 'Sand'
WIDTH = 500
HEIGHT = 500
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PARTICLE_TYPES = {
	0: particle.Air,
	1: particle.Sand,
	2: particle.Water
}


class World:

	def __init__(self):

		# Init pygame, set screen surface, create a clock
		pg.init()
		self.screen = pg.display.set_mode((WIDTH, HEIGHT))
		self.clock = pg.time.Clock()
		os.environ['SDL_VIDEO_CENTERED'] = '1'
		pg.display.set_caption(f'{NAME}')

		# Programm vars
		self.pixels = np.array([particle.Air(x, y) for x, y in product(range(100), range(100))], dtype=particle.Particle)
		self.delay = 1000
		self.particle_type = 1

		# Pygame vars
		self.fps = 60
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
				if event.key == pg.K_SPACE:
					self.particle_type = (self.particle_type + 1) % len(PARTICLE_TYPES)
	
		if pg.mouse.get_pressed()[0] and self.delay <= 0:
			self.delay = 10
			x, y = pg.mouse.get_pos()
			x, y = x // 5, y // 5
			self.pixels[x + y*100] = PARTICLE_TYPES[self.particle_type](x, y)

	def update(self):
		# Everything to update out of pause
		old_pixels = self.pixels.copy()
		for pixel in old_pixels:
			self.pixels = pixel.update(old_pixels)

	def draw(self):
		# Draw everything

		self.screen.fill(BLACK)

		for y in range(100):
			for x in range(100):
				pg.draw.rect(self.screen, self.pixels[x + y*100].color, ((x * 5, y * 5), (5, 5)))
		pg.display.flip()

	def main(self):
		while self.run:
			# Get all events
			self.events()

			# Update if running
			if not self.pause:
				self.update()

			# Always draw
			self.draw()

			# Tick the clock and get the elapsed time, update fps display
			self.elapsed = self.clock.tick(self.fps)
			self.delay -= self.elapsed
			pg.display.set_caption(f'{NAME}, fps: {self.clock.get_fps():.0f}, paused: {self.pause}')


if __name__ == '__main__':
	# Start the program
	World()

	# Exit gracefully
	pg.quit()
	sys.exit()
