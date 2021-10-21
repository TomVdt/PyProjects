from vars import *

class Bird:

    def __init__(self):
        self.x = 75
        self.y = int(height / 2)
        self.color = (255,255,255)
        self.size = 10
        self.vel = 0
        self.acc = 0

    def apply_force(self, force):
        self.acc += force

    def update(self):
        self.vel += self.acc
        self.y += self.vel
        self.acc = 0
        if self.y < 0:
            self.y = 0
            self.vel = 0
        elif self.y > height:
            self.y = height
            self.vel = 0

    def show(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
