from vars import *

class Basket(pygame.sprite.Sprite):

    def __init__(self):
        # Init Sprite
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, 'basket.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (int(width/2), height - 50)
        self.acc = 0
        self.vel = 0

    def move(self):
        #self.rect.center = pygame.mouse.get_pos()
        self.rect.x = pygame.math.Vector2(self.rect.x, 0).lerp(pygame.math.Vector2(pygame.mouse.get_pos()[0] - int(self.rect.w / 2), 0), 0.1).x
        pygame.event.pump()
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.acc -= 5
        elif key[pygame.K_RIGHT]:
            self.acc += 5

        self.vel = self.acc
        if not -25 <= self.vel <= 25:
            self.vel = self.vel/abs(self.vel)*25
        self.rect = self.rect.move(self.vel, 0)
        self.acc *= 0.75
