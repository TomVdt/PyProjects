import pygame
import os

width = 700
height = 600
background_color = (220, 220, 220)
run = True
click = False

os.environ['SDL_VIDEO_CENTERED'] = "1"
pygame.init
screen = pygame.display.set_mode((width, height))
screen.fill(background_color)
pygame.display.set_caption("Connect 4 MiniMax")

grid = pygame.Surface((width, height), flags=pygame.SRCALPHA)
for x in range(7):
    pygame.draw.line(grid, (0, 0, 0, 50), (x * 100, 0), (x * 100, height))
for y in range(6):
    pygame.draw.line(grid, (0, 0, 0, 50), (0, y * 100), (width, y * 100))

clock = pygame.time.Clock()
