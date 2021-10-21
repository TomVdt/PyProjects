import pygame as pg
import os
import sys

from viewport import Viewport
from world import World
from renderer import Renderer


# Constants
NAME = 'Pygame rpg'
WIDTH = 800
HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
vec2 = pg.math.Vector2


class Game:

	def __init__(self):

		# Init pygame, set screen surface, create a clock
		pg.init()
		self.screen = pg.display.set_mode((WIDTH, HEIGHT))
		self.clock = pg.time.Clock()
		os.environ['SDL_VIDEO_CENTERED'] = '1'
		pg.display.set_caption(f'{NAME}')

		# Programm vars
		self.zoom_surf = pg.Surface((WIDTH, HEIGHT))
		self.viewport = Viewport(0, 0, self.zoom_surf)
		self.world = World()
		self.world.load(None)
		self.renderer = Renderer()

		# Pygame vars
		self.fps = 60
		self.elapsed = 0
		self.pause = False
		self.run = True

		self.main()

	def events(self):
		# All event checks go here
		keys = pg.key.get_pressed()
		direction = vec2()
		if keys[pg.K_LEFT]:
			direction += (-1, 0)
		if keys[pg.K_RIGHT]:
			direction += (1, 0)
		if keys[pg.K_UP]:
			direction += (0, -1)
		if keys[pg.K_DOWN]:
			direction += (0, 1)

		if direction != vec2():
			self.viewport.move(*direction)

		for event in pg.event.get():
			if event.type == pg.QUIT:
				self.run = False
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					self.run = False
			elif event.type == pg.MOUSEBUTTONDOWN:
				if event.button == 4:
					self.viewport.zoom(1)
				elif event.button == 5:
					self.viewport.zoom(-1)
		

	def update(self):
		# Everything to update out of pause
		return

	def draw(self):
		# Draw everything

		self.screen.fill(BLACK)

		self.renderer.draw_world(self.screen, self.world, self.viewport)

		pg.display.flip()

	def main(self):
		while self.run:
			# Get all events
			self.events()

			# Update if running
			self.update()

			# Always draw
			self.draw()

			# Tick the clock and get the elapsed time, update fps display
			self.elapsed = self.clock.tick(self.fps)
			pg.display.set_caption(f'{NAME}, fps: {self.clock.get_fps():.0f}')


if __name__ == '__main__':
	# Start the program
	Game()

	# Exit gracefully
	pg.quit()
	sys.exit()
