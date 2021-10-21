from vars import *

class Drop(pygame.sprite.Sprite):

    def __init__(self, center, type):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        if type == 'egg':
            self.image = pygame.image.load(os.path.join(img_folder, 'egg.png')).convert_alpha()
        if type == 'poop':
            self.image = pygame.image.load(os.path.join(img_folder, 'poop.png')).convert_alpha()
        if type == 'gold_egg':
            self.image = pygame.image.load(os.path.join(img_folder, 'gold_egg.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.caught = False
        self.splat = False
        self.lifespan = 30
        self.vel = 0
        self.acc = 0

    def apply_force(self, gravity):
        self.acc += gravity

    def hit_ground(self):
        if self.rect.y >= height:
            if self.type == 'egg' or self.type == 'gold_egg':
                self.image = pygame.image.load(os.path.join(img_folder, 'exploded_egg.png')).convert_alpha()
                self.rect.center = (self.rect.center[0]+random.choice([i for i in range(-10, 10, 1)]), height)
            self.splat = True
            return True

    def is_caught(self, rect):
        if rect.colliderect(self.rect):
            self.caught = True
            return True
        else:
            return False

    def update(self):
        if not self.splat:
            self.vel += self.acc
            self.rect.y += self.vel
            self.acc = 0
            self.hit_ground()
        elif self.lifespan == 0:
            self.lifespan -= 1
            print(self.lifespan)
