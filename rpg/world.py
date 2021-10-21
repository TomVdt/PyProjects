import pygame as pg
import os


game_folder = os.path.dirname(__file__)
sprites = os.path.join(game_folder, 'assets/sprites/tiles')
sounds = os.path.join(game_folder, 'assets/sounds/tiles')


class World:

	def __init__(self):
		self.tiles = []
		self.tile_size = 10

	def load(self, file):
		for y in range(20):
			for x in range(20):
				self.tiles.append(FloorTile(x * self.tile_size, y * self.tile_size, self.tile_size))


class Tile:

	def __init__(self, wx, wy, size, texture, lighting):
		super().__init__()
		self._texture = pg.image.load(os.path.join(sprites, texture)).convert_alpha()
		self._rect = pg.Rect((wx, wy), (size, size))
		self.lighting = 10

	@property
	def pos(self):
		return self._rect.topleft

	@property
	def size(self):
		return self._rect.w

	@property
	def rect(self):
		return self._rect
	
	@property
	def texture(self):
		return self._texture
	

	def set_lighting(self, level):
		self.lighting = level

	def get_lighting(self):
		return self.lighting


class FloorTile(Tile):

	def __init__(self, wx, wy, size, lighting=15):
		super().__init__(wx, wy, size, 'no_texture.png', lighting)