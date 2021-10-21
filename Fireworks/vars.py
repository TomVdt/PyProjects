import pygame

width = 1000
height = 500

pygame.init
screen = pygame.display.set_mode((width, height))
screen.fill((0, 0, 0))
pygame.display.set_caption("Fireworks")

fade = pygame.Surface((width, height))
fade.set_alpha(16)
fade.fill((0, 0, 0))
screen.blit(fade, (0, 0))

tick = pygame.time.Clock()
