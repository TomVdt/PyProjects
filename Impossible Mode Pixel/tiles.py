from vars import *


class Wall(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(sprites_folder, 'wall.png')).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        sprites.add(self)
        sprites.change_layer(self, 0)
        walls.append(self)

    def show(self):
        pygame.draw.rect(camera, background_color, self.rect)
        camera.blit(self.image, self.rect)


class Spike(pygame.sprite.Sprite):

    def __init__(self, x, y, rotation):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(sprites_folder, 'spike.png')).convert_alpha()
        self.image = pygame.transform.rotate(self.image, rotation)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rot = rotation
        self.bottoml = pygame.math.Vector2(self.rect.bottomleft[0] - self.rect.center[0], self.rect.bottomleft[1] - 1 - self.rect.center[1]).rotate(-self.rot) + pygame.math.Vector2(self.rect.center)
        self.bottomr = pygame.math.Vector2(self.rect.bottomright[0] - self.rect.center[0], self.rect.bottomright[1] - 1 - self.rect.center[1]).rotate(-self.rot) + pygame.math.Vector2(self.rect.center)
        self.midtop = pygame.math.Vector2(self.rect.midtop[0] - self.rect.center[0], self.rect.midtop[1] - self.rect.center[1]).rotate(-self.rot) + pygame.math.Vector2(self.rect.center)
        self.midl = pygame.math.Vector2(self.rect.midleft[0] + 10 - self.rect.center[0], self.rect.midleft[1] - self.rect.center[1]).rotate(-self.rot) + pygame.math.Vector2(self.rect.center)
        self.midr = pygame.math.Vector2(self.rect.midright[0] - 10 - self.rect.center[0], self.rect.midright[1] - self.rect.center[1]).rotate(-self.rot) + pygame.math.Vector2(self.rect.center)
        sprites.add(self)
        sprites.change_layer(self, 0)
        spikes.append(self)

    def show(self):
        pygame.draw.rect(camera, background_color, self.rect)
        camera.blit(self.image, self.rect)


class Ending(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(sprites_folder, 'ending.png')).convert_alpha()
        self.original_image = pygame.image.load(os.path.join(sprites_folder, 'ending.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.angle = 0
        sprites.add(self)
        sprites.change_layer(self, 2)

    def update(self):
        self.rotate()

    def rotate(self):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.angle += 5 % 360
        x, y = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def show(self):
        pygame.draw.rect(camera, background_color, self.rect)
        camera.blit(self.image, self.rect)


class Background_tile(pygame.sprite.Sprite):

    def __init__(self, x, y, type, do_offset=False):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(sprites_folder, type + '.png')).convert_alpha()
        self.rect = self.image.get_rect()
        if (y // 40) % 2 == 0 and type == "chains" and do_offset:
            if x < width / 2:
                offset = 20
            else:
                offset = -20
        else:
            offset = 0
        self.rect.x = x + offset
        self.rect.y = y
        sprites.add(self)
        sprites.change_layer(self, 2)

    def show(self):
        pygame.draw.rect(camera, background_color, self.rect)
        camera.blit(self.image, self.rect)


# Testing area
if __name__ == "__main__":
    spike = Spike(50, 50, 0)
    test = pygame.Surface((50, 50), masks=spike.mask)
    test.fill((0, 0, 0))
    screen.blit(test, (0, 0))

    pygame.display.update()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
