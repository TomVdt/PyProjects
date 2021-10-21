import pygame as pg
import numpy as np
import os
import sys
from node import Node
from link import Link


# Constants
NAME = 'Springs'
WIDTH = 1000
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
		self.gravity = np.array((0, 5))
		self.nodes = [Node(WIDTH // 2, 0) for i in range(20)]
		self.nodes[0].anchored = True
		# self.nodes[-1].anchored = True
		# self.nodes[-1].pos = np.array((WIDTH // 2, HEIGHT), dtype=np.float)
		self.links = []
		for i in range(20):
			if i == 0:
				continue
			self.links.append(Link(self.nodes[i], self.nodes[i - 1], 10, 0.05))
		self.objects = []

		# Flags
		self.clicking = False
		self.right_clicking = False

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
			if event.type == pg.MOUSEBUTTONDOWN:
				if event.button == pg.BUTTON_LEFT:
					self.clicking = True
				if event.button == pg.BUTTON_RIGHT:
					self.right_clicking = True
			if event.type == pg.MOUSEBUTTONUP:
				if event.button == pg.BUTTON_LEFT:
					self.clicking = False
				if event.button == pg.BUTTON_RIGHT:
					self.right_clicking = False

	def update(self):
		for link in self.links:
			link.update()
		for node in self.nodes:
			node.apply_force(self.gravity * self.elapsed)
			node.update()
		for object in self.objects:
			object.apply_force(self.gravity * self.elapsed)
			object.update()
		if self.clicking:
			self.nodes[-1].pos = np.array(pg.mouse.get_pos(), dtype=np.float)
			self.nodes[-1].vel *= 0

	def draw(self):
		# Draw everything

		self.screen.fill(BLACK)

		for link in self.links:
			link.show(self.screen)
		for object in self.objects:
			object.show(self.screen)
		self.nodes[-1].show(self.screen)

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
			self.elapsed = self.clock.tick(self.fps) / 1000
			pg.display.set_caption(f'{NAME}, fps: {self.clock.get_fps():.0f}, paused: {self.pause}')


if __name__ == '__main__':
	# Start the program
	World()

	# Exit gracefully
	pg.quit()
	sys.exit()
