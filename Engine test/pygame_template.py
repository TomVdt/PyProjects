import pygame as pg
import os
import sys
from vec2 import Vec2
from math import pi


# Constants
NAME = 'Name'
WIDTH = 500
HEIGHT = 500
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class World:

	def __init__(self):

		# Init pygame, set screen surface, create a clock
		pg.init()
		self.screen = pg.display.set_mode((WIDTH, HEIGHT))
		self.clock = pg.time.Clock()
		os.environ['SDL_VIDEO_CENTERED'] = '1'
		pg.display.set_caption(f'{NAME}')

		# Programm vars
		# Vars
		self.v = Vec2(-100, 100)
		self.v_rot = self.v.rotate(pi)
		self.v_rot *= self.v.mag()

		# Pygame vars
		self.fps = 200
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

	def update(self):
		# Everything to update out of pause
		return

	def draw(self):
		# Draw everything

		self.screen.fill(BLACK)

		pg.draw.line(self.screen, (255, 255, 255), (self.v.x + 250, self.v.y + 250), (250, 250))
		pg.draw.line(self.screen, (255, 255, 255), (self.v_rot.x + 250, self.v_rot.y + 250), (250, 250))

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
			pg.display.set_caption(f'{NAME}, fps: {self.clock.get_fps():.0f}, paused: {self.pause}')


if __name__ == '__main__':
	# Start the program
	World()

	# Exit gracefully
	pg.quit()
	sys.exit()
