import pygame
import random
import math
import os
import sys

width = 1000
height = 750
camera_x = 0
camera_y = 0
background_color = (0, 0, 0)

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (20, 40)
pygame.init
screen = pygame.display.set_mode((width, height))
screen.fill(background_color)
pygame.display.set_caption("Planets")

# fade = pygame.Surface((width, height))
# fade.set_alpha(16)
# fade.fill((0, 0, 0))
# screen.blit(fade, (0, 0))

camera = pygame.Surface((width, height))

clock = pygame.time.Clock()
