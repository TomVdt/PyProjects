import pygame as pg
import noise
import os
import sys
import random


NAME = "Waves"
WIDTH = 500
HEIGHT = 500
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class World:

	def __init__(self, lines=100, steps=250):

		pg.init()
		self.screen = pg.display.set_mode((WIDTH, HEIGHT))
		self.clock = pg.time.Clock()

		os.environ['SDL_VIDEO_CENTERED'] = '1'
		pg.display.set_caption(f"{NAME}")

		self.x_off = 0
		self.lines = lines
		self.steps = steps
		self.step = 0
		self.line = 0
		self.old_pos = [0, 0]
		self.new_pos = [0, 0]

		self.line_spacing = int(1 / self.lines * HEIGHT)
		self.step_spacing = int(1 / self.steps * WIDTH)
		self.line_height = 0

		self.fps = 200
		self.elapsed = 0
		self.pause = False
		self.run = True

		self.main()

	def mask(self):
		return (-abs((self.steps / 2) - self.step) + (self.steps / 2)) / (self.steps / 2)

	def events(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				self.run = False
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					self.run = False
				if event.key == pg.K_LCTRL:
					self.pause = not self.pause

	def update(self):
		self.x_off += 0.01

		self.step += 1
		if self.step > self.steps:
			self.x_off = 0
			self.step = 0
			self.line += 1
			self.old_pos = [self.step * self.step_spacing, self.line * self.line_spacing]
			self.line_height = 100 * random.random()
			if self.line > self.lines:
				self.pause = True

		y = self.line * self.line_spacing - ((noise.pnoise2(self.x_off, self.line, octaves=2, persistence=0.25, lacunarity=2) + 1) ** 2) * self.line_height * self.mask()
		self.new_pos = [self.step * self.step_spacing, y]

	def draw(self):

		# self.screen.fill(BLACK)

		pg.draw.rect(self.screen, BLACK, ((int(self.old_pos[0]), int(min(self.old_pos[1], self.new_pos[1]))), (self.step_spacing, 100)))
		pg.draw.aaline(self.screen, WHITE, [int(i) for i in self.old_pos], [int(i) for i in self.new_pos])

		self.old_pos = list(self.new_pos)

		pg.display.flip()

	def main(self):
		while self.run:
			self.events()

			if not self.pause:
				self.update()

			self.draw()

			self.elapsed = self.clock.tick(self.fps)
			pg.display.set_caption(f"{NAME}, fps: {self.clock.get_fps():.0f}, paused: {self.pause}")


if __name__ == "__main__":
	World()
	pg.quit()
	sys.exit()
