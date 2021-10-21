import random, time
from vars import *
from vector import Vector

class Pipe:

    def __init__(self):
        self.space_size = random.randint(50,75)
        self.pipe_width = 40
        self.y = -self.pipe_width
        self.space_pos = random.randint(0, width - self.space_size)
        self.speed = 5
        self.color = (255,255,255)

    def update(self):
        self.y += self.speed

    def show(self):
        pygame.draw.rect(screen, self.color, ((0, self.y), (width, self.pipe_width)))
        pygame.draw.rect(screen, background, ((self.space_pos, self.y), (self.space_size, self.pipe_width)))

    def finished(self):
        if self.y - self.pipe_width > height:
            return True
        else:
            return False

    def hit(self, x, y, size):
        if self.y - size <= y <= self.y + size + self.pipe_width:
            if self.space_pos + size <= x <= self.space_pos + self.space_size - size:
                return False
            else:
                return True
        else:
            return False
