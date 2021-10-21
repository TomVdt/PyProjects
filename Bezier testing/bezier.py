import pygame as pg
import os
import sys
from point import *
from numpy import sqrt

# Constants
NAME = 'Bezier'
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
		self.pressed = False
		origin = Circle(20, 20, 5)
		endpoint = Circle(480, 480, 5)
		control1 = Circle(480, 20, 5)
		control2 = Circle(20, 480, 5)
		self.points = [origin, control1, control2, endpoint]

		# Pygame vars
		self.fps = 200
		self.elapsed = 0
		self.pause = False
		self.run = True

		self.main()

	def lerp(self, p1, p2, t):
		return Point(p1.x + (p2.x - p1.x) * t, p1.y + (p2.y - p1.y) * t)

	def recursive_bezier(self, t, points):
		if len(points) == 1:
			# pg.draw.circle(self.screen, (255, 0, 0), (points[0].x, points[0].y), 1)
			return points[0]

		subpoints = []
		nb_points = len(points)
		for i in range(nb_points - 1):
			subpoints.append(self.lerp(points[i], points[i + 1], t))
		return self.recursive_bezier(t, subpoints)

	def bezier(self, points):
		t = 0
		resolution = 50
		prev_point = points[0]
		for _ in range(resolution):
			new_point = self.recursive_bezier(t, points)
			pg.draw.line(self.screen, WHITE, (prev_point.x, prev_point.y), (new_point.x, new_point.y))
			prev_point = new_point
			t += (1 / resolution)
		pg.draw.line(self.screen, WHITE, (prev_point.x, prev_point.y), (points[-1].x, points[-1].y))

	def collide_points(self, points, x, y):
		colliding = []
		for point in points:
			if point.collide(x, y):
				colliding.append(point)
		return colliding

	def hover_points(self, points, x, y):
		for point in points:
			if point.collide(x, y):
				point.hover()
			else:
				point.dehover()

	def events(self):
		# All event checks go here
		for event in pg.event.get():
			if event.type == pg.QUIT:
				self.run = False
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					self.run = False
				if event.key == pg.K_SPACE:
					self.pause = not self.pause

	def update(self):
		# Everything to update out of pause
		mx, my = pg.mouse.get_pos()
		self.hover_points(self.points, mx, my)

		if pg.mouse.get_pressed()[0]:
			if not self.pressed and pg.key.get_pressed()[pg.K_LSHIFT]:
				colliding = False
				self.pressed = True
				for i in range(len(self.points) - 1, -1, -1):
					if self.points[i].hovering:
						colliding = True
						self.points.pop(i)
				if not colliding:
					temp = self.points.pop(-1)
					self.points.append(Circle(mx, my, 5))
					self.points.append(temp)
			for point in self.points:
				if point.hovering:
					point.select()
				if point.selected:
					point.set(mx, my)
		else:
			self.pressed = False
			for point in self.points:
				point.deselect()

		return

	def draw(self):
		# Draw everything

		self.screen.fill(BLACK)

		for point in self.points:
			point.draw(self.screen)

		self.bezier(self.points)

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
