import pygame
from pygame.locals import *

width = 250
height = 500
background = (0,0,0)

pygame.init
screen = pygame.display.set_mode((width, height))
screen.fill(background)
pygame.display.set_caption("Frog")

tick = pygame.time.Clock()
