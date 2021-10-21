from vars import *


class Button(pygame.sprite.Sprite):

    def __init__(self, pos, type):
        pygame.sprite.Sprite.__init__(self)
        if type == "play":
            self.image = pygame.image.load(os.path.join(sprites_folder, 'play.png')).convert_alpha()
        elif type == "info":
            self.image = pygame.image.load(os.path.join(sprites_folder, 'info.png')).convert_alpha()
            self.text = pygame.image.load(os.path.join(sprites_folder, 'info_text.png')).convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.type = type
        self.start_level = False
        self.show_text = False
        sprites.add(self)

    def dist_sq(self, a, b):
        return (b[0] - a[0])**2 + (b[1] - a[1])**2

    def update(self):
        if self.start_level:
            self.start_level = False
        if pygame.mouse.get_pressed()[0]:
            if self.show_text:
                self.show_text = False
                pygame.time.wait(100)
            elif self.dist_sq(self.rect.center, pygame.mouse.get_pos()) <= 8000:
                if self.type == "play":
                    self.start_level = True
                elif self.type == "info":
                    self.show_text = True
                    pygame.time.wait(100)
