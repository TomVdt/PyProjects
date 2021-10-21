from vars import *
import math

class Bird:

    def __init__(self):
        self.y = 75
        self.x = int(width / 2)
        self.color = (255,255,255)
        self.size = 10

    def update(self, val):
        self.x = pygame.math.Vector2(self.x, 0).lerp(pygame.math.Vector2(pygame.mouse.get_pos()[0], 0), 0.1).x
        self.y = height-abs(math.sin(val)) * 200

    def show(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
