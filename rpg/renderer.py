import pygame as pg

vec2 = pg.math.Vector2


class Renderer:

	def __init__(self):
		pass

	def _get_visible_tiles(self, tiles, rect):
		for tile in tiles:
			if rect.colliderect(tile.rect):
				yield tile

	def draw_world(self, surface, world, viewport):
		for tile in self._get_visible_tiles(world.tiles, viewport.rect):
			surface.blit(tile.texture, (viewport.offset + tile.pos))
		viewport.update()
		viewport.draw(surface)