import random, time
from vars import *
from vector import Vector

class Pipe:

    def __init__(self):
        self.space_size = random.randint(int(height/5), int(height/4))
        self.x = width
        self.space_pos = random.randint(0, height - self.space_size)
        self.pipe_width = 40
        self.speed = 5
        self.color = (255,255,255)

    def update(self):
        self.x -= self.speed

    def show(self):
        pygame.draw.rect(screen, self.color, ((self.x, 0), (self.pipe_width, height)))
        pygame.draw.rect(screen, background, ((self.x, self.space_pos), (self.pipe_width, self.space_size)))

    def finished(self):
        if self.x + self.pipe_width < 0:
            return True
        else:
            return False

    def hit(self, x, y, size):
        if self.x-size <= x <= self.x+size+self.pipe_width:
            if self.space_pos + size <= y <= self.space_pos + self.space_size - size:
                return False
            else:
                return True
        else:
            return False
