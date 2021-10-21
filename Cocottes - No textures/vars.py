import pygame, random, math

width = 1000
height = 750
background = (0,0,0)

pygame.init
screen = pygame.display.set_mode((width, height))
screen.fill(background)
pygame.display.set_caption("Cocottes")

tick = pygame.time.Clock()
