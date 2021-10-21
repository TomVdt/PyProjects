import pygame, random, math, os

width = 1000
height = 750
background_color = (255,255,255)

pygame.init
screen = pygame.display.set_mode((width, height))
screen.fill(background_color)
pygame.display.set_caption("Cocottes")

sprites = pygame.sprite.Group()
drop_sprites = pygame.sprite.Group()

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')

background = pygame.image.load(os.path.join(img_folder, 'background.png')).convert()

clock = pygame.time.Clock()
