from vars import *
from drop import Drop

class Cocotte(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, 'chicken.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.pondu = []

    def pondre(self, weights = [70,20,5]):
        roll = random.choices([0,1,2], weights)[0]
        if roll == 0:
            self.pondu.append(Drop(self.rect.center, 'egg'))
        elif roll == 1:
            self.pondu.append(Drop(self.rect.center, 'poop'))
        elif roll == 2:
            self.pondu.append(Drop(self.rect.center, 'gold_egg'))
        drop_sprites.add(self.pondu)

    def get_caught(self, rect):
        for i in range(len(self.pondu)):
            if self.pondu[i].is_caught(rect):
                return self.pondu[i].type

    def update_pos(self, gravity):
        counter = len(self.pondu)-1
        for i in reversed(self.pondu):
            i.apply_force(gravity)
            i.update()
            if i.splat or i.caught:
                if i.caught:
                    drop_sprites.remove(i)
                self.pondu.pop(counter)
            counter -= 1
