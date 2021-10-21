import pygame as pg
import os
import sys


# Constants
NAME = 'Chess'
WIDTH = 400
HEIGHT = 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

img_folder = os.path.join(os.path.dirname(__file__), 'img')


class World:

	def __init__(self):

		# Init pygame, set screen surface, create a clock
		pg.init()
		self.screen = pg.display.set_mode((WIDTH, HEIGHT))
		self.clock = pg.time.Clock()
		os.environ['SDL_VIDEO_CENTERED'] = '1'
		pg.display.set_caption(f'{NAME}')

		# Programm vars
		self.textures = [
			pg.image.load(os.path.join(img_folder, 'pawn.png')).convert_alpha(),
			pg.image.load(os.path.join(img_folder, 'rook.png')).convert_alpha(),
			pg.image.load(os.path.join(img_folder, 'knight.png')).convert_alpha(),
			pg.image.load(os.path.join(img_folder, 'bishop.png')).convert_alpha(),
			pg.image.load(os.path.join(img_folder, 'queen.png')).convert_alpha(),
			pg.image.load(os.path.join(img_folder, 'king.png')).convert_alpha()
		]
		self.board = [
			2, 3, 4, 6, 5, 4, 3, 2,
			1, 1, 1, 1, 1, 1, 1, 1,
			0, 0, 0, 0, 0, 0, 0, 0,
			0, 0, 0, 0, 0, 0, 0, 0,
			0, 0, 0, 0, 0, 0, 0, 0,
			0, 0, 0, 0, 0, 0, 0, 0,
			7, 7, 7, 7, 7, 7, 7, 7,
			8, 9, 10, 12, 11, 10, 9, 8,
		]
		self.tile_size = WIDTH // 8

		# Pygame vars
		self.fps = 200
		self.elapsed = 0
		self.pause = False
		self.run = True

		self.main()

	def draw_board(self):
		for y in range(8):
			for x in range(8):
				pg.draw.rect(self.screen, BLACK if (y + x) % 2 == 0 else WHITE, ((x * self.tile_size, y * self.tile_size), (self.tile_size, self.tile_size)))

	def fill_board(self, board):
		for y in range(8):
			for x in range(8):
				if board[y * 8 + x] != 0:
					self.screen.blit(self.textures[board[y * 8 + x] % 6 - 1], (x * self.tile_size, y * self.tile_size))

	def get_selection(self):
		x, y = pg.mouse.get_pos()
		return x // self.tile_size, y // self.tile_size

	def draw_selection(self, bx, by):
		pg.draw.rect(self.screen, (255, 255, 0), ((bx * self.tile_size, by * self.tile_size), (self.tile_size, self.tile_size)))

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
		return

	def draw(self):
		# Draw everything

		self.screen.fill(BLACK)

		self.draw_board()
		self.draw_selection(*self.get_selection())
		self.fill_board(self.board)

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
