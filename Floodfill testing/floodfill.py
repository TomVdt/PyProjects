import pygame as pg
import numpy as np
import os
import sys


# Constants
NAME = 'Floodfill'
WIDTH = 500
HEIGHT = 500
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
Color = pg.Color


class World:

	def __init__(self):

		# Init pygame, set screen surface, create a clock
		pg.init()
		self.screen = pg.display.set_mode((WIDTH, HEIGHT))
		self.clock = pg.time.Clock()
		os.environ['SDL_VIDEO_CENTERED'] = '1'
		pg.display.set_caption(f'{NAME}')

		# Programm vars
		self.filling = []
		self.grid = np.empty((50, 50), dtype=Color)
		for x in range(50):
			for y in range(50):
				self.grid[y][x] = Color(255, 255, 255)

		# Pygame vars
		self.fps = 200
		self.elapsed = 0
		self.pause = False
		self.run = True

		self.main()

	def color_distance(self, color1, color2):
		rmean = (color1.r + color2.r ) / 2
		r = color1.r - color2.r
		g = color1.g - color2.g
		b = color1.b - color2.b
		return np.sqrt((((512+rmean)*r*r)/256) + 4*g*g + (((767-rmean)*b*b)/256))


	def is_similar(self, color1, color2, variance):
		dist = self.color_distance(color1, color2)
		if dist < variance:
			return True
		else:
			return False

	def floodfill(self, x, y, replace_color, fill_color, variance):
		q = []
		q.append((x, y))
		while len(q) > 0:
			x, y = q[0]
			q.pop(0)
			if self.is_similar(self.grid[y][x], replace_color, variance):
				self.grid[y][x] = fill_color(x, y)
				if 0 < x:
					q.append((x - 1, y))
				if x < 49:
					q.append((x + 1, y))
				if 0 < y:
					q.append((x, y - 1))
				if y < 49:
					q.append((x, y + 1))

	def floodfill_visual(self, color, q):
		while len(q) > 0:
			x, y = q[0]
			q.pop(0)
			if self.grid[y][x] == color:
				self.grid[y][x].hsva = (int((x + y) / 100 * 360), 100, 100)
				if 0 < x:
					q.append((x - 1, y))
				if x < 49:
					q.append((x + 1, y))
				if 0 < y:
					q.append((x, y - 1))
				if y < 49:
					q.append((x, y + 1))
			return q

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
			elif event.type == pg.MOUSEBUTTONDOWN:
				x = event.pos[0] // 10
				y = event.pos[1] // 10
				replace_color = Color(self.grid[y][x])
				if event.button == 2:
					self.floodfill(x, y, replace_color, lambda x,y: Color(0,int(x/50*255),0), 0.1)
				if event.button == 3:
					self.floodfill(x, y, replace_color, lambda x,y: Color(255, 0, 0), 100)

	def update(self):
		# Everything to update out of pause
		mx, my = pg.mouse.get_pos()
		left, middle, right = pg.mouse.get_pressed()
		if left:
			x, y = mx // 10, my // 10
			for x_ in range(max(0, x - 1), min(50, x + 2)):
				for y_ in range(max(0, y - 1), min(50, y + 2)): 
					self.grid[y_][x_] = Color(0, 0, 0)
		# if len(self.filling) > 0:
		# 	self.filling = self.floodfill(self.fill_color, self.filling)


	def draw(self):
		# Draw everything

		self.screen.fill(BLACK)

		for x in range(50):
			for y in range(50):
				pg.draw.rect(self.screen, self.grid[y][x], ((x * 10, y * 10), (10, 10)))

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
