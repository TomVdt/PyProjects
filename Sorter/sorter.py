import pygame as pg
import random
import os
import sys


# Constants
NAME = "Sorting visualisations!"
WIDTH = 500
HEIGHT = 500
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def hsv_to_rgb(h, s, v):
	if s == 0.0:
		v *= 255
		return (v, v, v)
	i = int(h * 6.)  # XXX assume int() truncates!
	f = (h * 6.) - i
	p, q, t = int(255 * (v * (1. - s))), int(255 * (v * (1. - s * f))), int(255 * (v * (1. - s * (1. - f))))
	v *= 255
	i %= 6
	if i == 0:
		return (v, t, p)
	if i == 1:
		return (q, v, p)
	if i == 2:
		return (p, v, t)
	if i == 3:
		return (p, q, v)
	if i == 4:
		return (t, p, v)
	if i == 5:
		return (v, p, q)


class World:

	def __init__(self):

		# Init pygame, set screen surface, create a clock
		pg.init()
		self.screen = pg.display.set_mode((WIDTH, HEIGHT))
		self.clock = pg.time.Clock()
		os.environ['SDL_VIDEO_CENTERED'] = '1'
		pg.display.set_caption(f'{NAME}')

		# Program vars
		self.options = {
			'n': 64,
			'delay': 25
		}
		self.bars = list(range(self.options['n']))

		# Pygame vars
		self.fps = 60
		self.elapsed = 0
		self.pause = False
		self.run = True

		self.main()

	def update_options(self, kwargs):
		for key in kwargs:
			if key in self.options.keys():
				self.options[key] = kwargs[key]
			else:
				raise('Option does not exist')

	def randomize(self):
		temp = list(range(self.options['n']))
		for i in range(self.options['n']):
			self.bars[i] = temp.pop(temp.index(random.choice(temp)))

	def merge_sort(self, arr, offset):
		if len(arr) > 1:
			mid = len(arr) // 2
			L = arr[:mid]
			R = arr[mid:]
			self.merge_sort(L, offset)
			self.merge_sort(R, offset + mid)

			i = j = k = 0
			while i < len(L) and j < len(R):
				if L[i] > R[j]:
					arr[k] = R[j]
					self.draw_bar(arr[j - 1] + 1, offset + mid + j - 1)
					self.select_bar(R[j] + 1, offset + mid + j)
					j += 1
				else:
					arr[k] = L[i]
					self.draw_bar(arr[i - 1] + 1, offset + i - 1)
					self.select_bar(L[i] + 1, offset + i)
					i += 1
				k += 1
				pg.time.wait(self.options['delay'])

			while i < len(L):
				arr[k] = L[i]
				self.draw_bar(arr[i - 1] + 1, offset + i - 1)
				self.select_bar(L[i] + 1, offset + i)
				pg.time.wait(self.options['delay'])
				i += 1
				k += 1
			while j < len(R):
				arr[k] = R[j]
				self.draw_bar(arr[j - 1] + 1, offset + mid + j - 1)
				self.select_bar(R[j] + 1, offset + mid + j)
				pg.time.wait(self.options['delay'])
				j += 1
				k += 1
			for k in range(len(arr)):
				self.draw_bar(arr[k] + 1, offset + k)
				pg.time.wait(self.options['delay'])
			return arr

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
				if event.key == pg.K_LCTRL:
					self.randomize()
				if event.key == pg.K_RCTRL:
					self.bars = self.merge_sort(self.bars, 0)

	def update(self):
		# Everything to update out of pause
		self.arrs = []
		self.mids = []
		self.offsets = []
		self.Ls = []
		self.Liters = []
		self.Rs = []
		self.Riters = []
		# ????


	def select_bar(self, l, i):
		h = HEIGHT / self.options['n']
		w = WIDTH / self.options['n']

		pg.draw.rect(self.screen, WHITE, ((i * w, HEIGHT - (h * l)), (w, h * l)))
		pg.display.update(pg.Rect((i * w, HEIGHT - (h * l)), (w, h * l)))

	def draw_bar(self, l, i):
		h = HEIGHT / self.options['n']
		w = WIDTH / self.options['n']
		color = hsv_to_rgb(l / self.options['n'], 1., 1.)

		pg.draw.rect(self.screen, BLACK, ((i * w, 0), (w, HEIGHT)))
		pg.draw.rect(self.screen, color, ((i * w, HEIGHT - (h * l)), (w, h * l)))
		pg.display.update(pg.Rect((i * w, 0), (w, HEIGHT)))

	def draw(self):
		# Draw everything

		self.screen.fill(BLACK)

		n = self.options['n']
		for i in range(n):
			l = self.bars[i] + 1
			h = HEIGHT / n
			w = WIDTH / n
			color = hsv_to_rgb(l / n, 1., 1.)

			pg.draw.rect(self.screen, color, ((i * w, HEIGHT - (h * l)), (w, h * l)))

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
