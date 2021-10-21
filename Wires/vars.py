import math
import os
import random

import pygame as pg

# COLORS
BLACK = (0, 0, 0)
GREY = (127, 127, 127)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
ORANGE = (250, 170, 10)

WIDTH = 800
HEIGHT = 600
background_color = BLACK

# Init pygame
pg.init()
os.environ['SDL_VIDEO_CENTERED'] = "1"
screen = pg.display.set_mode((WIDTH, HEIGHT))
screen.fill(background_color)
pg.display.set_caption("Wires")
# pg.display.set_icon(pg.image.load(os.path.join(sprites_folder, 'icon.png')).convert_alpha())
clock = pg.time.Clock()

game_folder = os.path.dirname(__file__)
sprites_folder = os.path.join(game_folder, 'sprites')

sprites = pg.sprite.Group()

buttons = []
