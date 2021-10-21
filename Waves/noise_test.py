import pygame as pg
import numpy as np
import noise
import os
import sys


NAME = "Noise"
WIDTH = 500
HEIGHT = 500
WHITE = np.array((255, 255, 255), dtype=np.float16)
BLACK = (0, 0, 0)


class World:

	def __init__(self, lines=100, steps=250):

		pg.init()
		self.screen = pg.display.set_mode((WIDTH, HEIGHT))
		self.clock = pg.time.Clock()

		os.environ['SDL_VIDEO_CENTERED'] = '1'
		pg.display.set_caption(f"{NAME}")

		self.x_off = 0
		self.y_off = 0
		self.x = 0
		self.y = 0

		self.pixels = pg.PixelArray(self.screen)
		self.overlay = pg.Surface((WIDTH, HEIGHT))
		self.p_overlay = pg.PixelArray(self.overlay)
		self.enable_overlay = False

		self.fps = 200
		self.elapsed = 0
		self.pause = False
		self.run = True

		self.main()

	def events(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				self.run = False
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					self.run = False
				if event.key == pg.K_LCTRL:
					self.enable_overlay = not self.enable_overlay
					self.pause = not self.pause

	def update(self):
		# self.x_off = 0
		self.y_off = 0
		for x in range(WIDTH):
			for y in range(HEIGHT):
				val = max(min(noise.pnoise2(self.x_off, self.y_off, octaves=3, lacunarity=0.25), 0.5), -0.5) + 0.5
				if val <= 0.2:
					color = 0x0d4bbf
				elif val <= 0.3:
					color = 0xe0b341
				elif val <= 0.55:
					color = 0x60af28
				elif val <= 0.9:
					color = 0x828282
				else:
					color = 0xffffff
				self.pixels[x, y] = color
				self.p_overlay[x, y] = tuple(WHITE * ((val + 1) / 2))
				self.y_off += 0.007
			self.x_off += 0.007
			self.y_off = 0
		self.x_off -= WIDTH * 0.007 + 0.1

		# self.pause = True

	def draw(self):

		# self.screen.fill(BLACK)

		pg.surfarray.blit_array(self.screen, self.p_overlay if self.enable_overlay else self.pixels)

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
