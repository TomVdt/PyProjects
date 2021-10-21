import pygame as pg
import os
import sys


# Constants
NAME = 'Color Picker'
WIDTH = 160
HEIGHT = 150
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
		self.select_color = (0, 0, 0)
		self.luminence = 1
		self.draw_chromatic_rect()

		# Pygame vars
		self.fps = 60
		self.elapsed = 0
		self.pause = False
		self.run = True

		self.main()

	def hsv_to_rgb(self, h, s, v):
		if s == 0.0: v*=255; return (v, v, v)
		i = int(h*6.) # XXX assume int() truncates!
		f = (h*6.)-i; p,q,t = int(255*(v*(1.-s))), int(255*(v*(1.-s*f))), int(255*(v*(1.-s*(1.-f)))); v*=255; i%=6
		if i == 0: return (v, t, p)
		if i == 1: return (q, v, p)
		if i == 2: return (p, v, t)
		if i == 3: return (p, q, v)
		if i == 4: return (t, p, v)
		if i == 5: return (v, p, q)

	def draw_chromatic_rect(self):
		for y in range(HEIGHT-50):
			for x in range(WIDTH):
				pg.draw.rect(self.screen, self.hsv_to_rgb(x/WIDTH, y/(HEIGHT-50), self.luminence), ((x, y), (1, 1)))

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
			elif event.type == pg.MOUSEBUTTONDOWN:
				if event.button == 4:
					self.luminence += 0.05
				if event.button == 5:
					self.luminence -= 0.05
				self.luminence = min(max(self.luminence, 0), 1)
				# self.draw_chromatic_rect()

	def update(self):
		# Everything to update out of pause
		x,y = pg.mouse.get_pos()
		if y < HEIGHT-50:
			self.select_color = self.hsv_to_rgb(x/WIDTH, y/(HEIGHT-50), self.luminence)

	def draw(self):
		# Draw everything

		# self.screen.fill(BLACK)
		pg.draw.rect(self.screen, self.select_color, ((0, 100), (WIDTH, 50)))

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
