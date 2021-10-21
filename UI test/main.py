import pygame as pg
import numpy as np
import os
import sys

from ui import Button, Title
from viewport import Viewport

# Constants
NAME = "UI test"
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
		pg.display.set_caption(f"{NAME}")

		# Program vars
		self.viewport = Viewport(self.screen)
		self.background = pg.Surface((WIDTH, HEIGHT))
		# self.button = Button((0, 0), (500, 30), "Test", lambda: print("Testing"), hover=(250, 127, 69), background=(128, 125, 130))
		self.objects = []
		self.elements = []
		self.buttons = []

		self.mouse_pos = np.array((0, 0))
		self.mouse_world_pos = self.viewport.get_mouse_pos(self.mouse_pos)

		# Game Vars
		self.event_context = self._load_main_menu
		self.draw_context = self._menu_draw

		# Pygame vars
		self.fps = 120
		self.elapsed = 0
		self.pause = False
		self.run = True

		self.main()

	def _load_main_menu(self):
		self.background = pg.transform.scale(pg.image.load("back.jpg"), (WIDTH, HEIGHT))
		title = Title((250, 80), NAME, text_size=50, text_color=(0, 0, 0))
		start = Button((WIDTH // 2 - WIDTH // 4, 205), (WIDTH // 2, 30), "Start", self._start_game, hover=(250, 127, 69), background=(128, 125, 130))
		options = Button((WIDTH // 2 - WIDTH // 4, 235), (WIDTH // 2, 30), "Options", self._load_options_menu, hover=(250, 127, 69), background=(128, 125, 130))
		quit = Button((WIDTH // 2 - WIDTH // 4, 265), (WIDTH // 2, 30), "Quit", self._menu_quit, hover=(250, 127, 69), background=(128, 125, 130))
		self.elements.append(title)
		self.buttons.append(start)
		self.buttons.append(options)
		self.buttons.append(quit)
		self.event_context = self._menu_controls
		self.draw_context = self._menu_draw

	def _start_game(self):
		print("start")

	def _load_options_menu(self):
		print("options")

	def _menu_controls(self):
		for button in self.buttons:
			button.update(self.mouse_pos)

	def _menu_quit(self):
		self.run = False

	def _menu_draw(self):
		self.screen.blit(self.background, (0, 0))
		for button in self.buttons:
			button.draw(np.array((0, 0)), self.screen)
		for element in self.elements:
			element.draw(np.array((0, 0)), self.screen)

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
				if event.button == 1:
					for button in self.buttons:
						if button.hovering:
							button.press()

		self.mouse_pos = np.array(pg.mouse.get_pos())
		self.mouse_world_pos = self.viewport.get_mouse_pos(self.mouse_pos)

		pressed = pg.key.get_pressed()
		for key in self.viewport.controls:
			if pressed[key]:
				self.viewport.scroll(self.viewport.controls[key] * self.elapsed)

		self.event_context()

	def update(self):
		# Everything to update out of pause
		return

	def draw(self):
		# Draw everything

		self.screen.fill(BLACK)

		self.viewport.draw(self.objects, self.screen)

		self.draw_context()

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
			pg.display.set_caption(f"{NAME}, fps: {self.clock.get_fps():.0f}, paused: {self.pause}")


if __name__ == "__main__":
	# Start the program
	World()

	# Exit gracefully
	pg.quit()
	sys.exit()
