from vars import *

class Basket(pygame.sprite.Sprite):

    def __init__(self):
        self.x = int(width / 2)
        self.y = height - 100
        self.w = 150
        self.h = 100

        # # Init Sprite
        # pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((self.w, self.h))
        # self.image.fill((0,255,0))
        # self.rect = self.image.get_rect()
        # self.rect.x = self.x
        # self.rect.y = self.y

    def move(self):
        self.rect.x = pygame.math.Vector2(self.rect.x, 0).lerp(pygame.math.Vector2(pygame.mouse.get_pos()[0] - int(self.w / 2), 0), 0.1).x


    def show(self):
        pygame.draw.arc(screen, (255,255,255), ((self.x, self.y), (self.w, self.h)), math.pi, 0)
