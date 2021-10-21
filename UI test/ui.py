import pygame as pg
# import numpy as np


# class Element:

# 	def __init__(self, pos, size):
# 		self.rect = pg.Rect(pos, size)

# 	def update(self, mouse_pos=(0, 0)):
# 		return


class Button:

	def __init__(self, pos, size, text, action, text_size=12, text_font="arial", text_color=(255, 255, 255), background=(0, 0, 0, 0), hover=(0, 0, 0, 0)):
		# Button data
		self.action = action
		self.rect = pg.Rect((pos, size))

		# Button text
		self.text = text
		self.text_color = text_color
		self.text_font = pg.font.SysFont(text_font, text_size)
		self.text_surf = self.text_font.render(text, True, text_color, background)
		self.text_hover_surf = self.text_font.render(text, True, text_color, hover)
		self.text_rect = self.text_surf.get_rect()
		self.text_rect.center = self.rect.center

		# Colors
		self.background_color = background
		self.hover_color = hover

		# Flags
		self.hovering = False

	def update(self, pos):
		if self.rect.collidepoint(pos):
			self.hovering = True
			return True
		else:
			self.hovering = False
			return False

	def press(self):
		self.action()

	def draw(self, offset, surf):
		if self.hovering:
			pg.draw.rect(surf, self.hover_color, (self.rect.topleft - offset, self.rect.size))
			surf.blit(self.text_hover_surf, self.text_rect.topleft - offset)
		else:
			pg.draw.rect(surf, self.background_color, (self.rect.topleft - offset, self.rect.size))
			surf.blit(self.text_surf, self.text_rect.topleft - offset)


class Title:

	def __init__(self, pos, text, text_size=20, text_font="arial", text_color=(255, 255, 255), centered=True):
		self.text = text
		self.text_color = text_color
		self.text_font = pg.font.SysFont(text_font, text_size)
		self.text_surf = self.text_font.render(text, True, text_color, None)
		self.rect = self.text_surf.get_rect()

		if centered:
			self.rect.center = pos

	def update(self, pos):
		return

	def draw(self, offset, surf):
		surf.blit(self.text_surf, self.rect.topleft - offset)


if __name__ == "__main__":
	pg.font.init()
	# but = Button(0, 0, "test")
