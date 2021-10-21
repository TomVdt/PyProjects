import math
import os
import sys
try:
    import pygame
except ImportError:
    print("Pygame module not found, try installing it with 'pip install pygame'")
    print("Now, your punishment")
    import webbrowser
    webbrowser.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
    sys.exit()

width = 800
height = 600
background_color = (220, 220, 220)
walls = []
spikes = []
buttons = []

# Pygame global vars
sprites = pygame.sprite.LayeredUpdates(default_layer=1, layer0=0, layer2=2)

game_folder = os.path.dirname(__file__)
sprites_folder = os.path.join(game_folder, 'sprites')
music_folder = os.path.join(game_folder, 'music')

camera = pygame.Surface((width, height))
empty_tile = pygame.Surface((40, 40))

clock = pygame.time.Clock()
