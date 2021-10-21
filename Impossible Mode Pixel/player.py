from vars import *


class Player(pygame.sprite.Sprite):

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(sprites_folder, 'player.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] + 3
        self.rect.y = pos[1] + 6
        self.dx = 0
        self.dy = 0
        self.in_air = False
        self.alive = True
        self.death_frame = 0
        self.death_duration = 30
        sprites.add(self)

    def move_lr(self, dir):
        self.dx += dir * 4.2

    def gravity(self, gravity):
        if self.is_in_air() or not self.alive:
            self.dy += gravity

    def jump(self, value):
        if not self.is_in_air() and self.alive:
            self.rect.y = int(self.rect.y)
            self.dy = 0
            self.dy -= value
            self.in_air = True

    def is_in_air(self):
        for wall in walls:
            if wall.rect.collidepoint(self.rect.bottomleft[0] + 1, self.rect.bottomleft[1]) or wall.rect.collidepoint(self.rect.bottomright[0] - 1, self.rect.bottomright[1]):
                return False
        return True

    def change_sprite(self):
        if self.dx > 0:
            self.image = pygame.image.load(os.path.join(sprites_folder, 'player_right.png')).convert_alpha()
        elif self.dx < 0:
            self.image = pygame.image.load(os.path.join(sprites_folder, 'player_left.png')).convert_alpha()
        else:
            self.image = pygame.image.load(os.path.join(sprites_folder, 'player.png')).convert_alpha()

    def update(self):
        if self.alive:
            self.change_sprite()

            self.move("x")
            self.dx = 0
            self.move("y")

        else:
            self.death_animation()

    def move(self, axis):
        if axis == "x":
            self.rect.x += self.dx
        elif axis == "y":
            self.rect.y += self.dy
        self.collide(axis)

    def collide(self, axis):
        if axis == "x":
            for wall in walls:
                if self.rect.colliderect(wall.rect):
                    if self.dx > 0:
                        self.rect.right = wall.rect.left
                    if self.dx < 0:
                        self.rect.left = wall.rect.right
                    return
        elif axis == "y":
            for wall in walls:
                if self.rect.colliderect(wall.rect):
                    if self.dy >= 0:
                        self.rect.bottom = wall.rect.top
                    if self.dy < 0:
                        self.rect.top = wall.rect.bottom
                    self.dy = 0
                    return

    def death_animation(self):
        if self.death_frame == 0:
            self.dy = 0
        self.rect.y += self.dy
        if self.death_frame % 10 == 0:
            self.image = pygame.image.load(os.path.join(sprites_folder, 'player_inverted.png')).convert_alpha()
        elif self.death_frame % 10 == 5:
            self.image = pygame.image.load(os.path.join(sprites_folder, 'player.png')).convert_alpha()
        self.death_frame += 1
        # print(self.death_frame)

    def show(self):
        pygame.draw.rect(camera, (255, 0, 0), self.rect)
        camera.blit(self.image, self.rect)


# class Player(pygame.sprite.Sprite):
#
#     def __init__(self, pos):
#         pygame.sprite.Sprite.__init__(self)
#         self.image = pygame.image.load(os.path.join(sprites_folder, 'player.png')).convert_alpha()
#         self.mask = pygame.mask.from_surface(self.image)
#         self.rect = self.image.get_rect()
#         self.rect.x = pos[0] + 3
#         self.rect.y = pos[1] + 6
#         self.dx = 0
#         self.dy = 0
#         self.in_air = False
#         self.alive = True
#         self.death_frame = 0
#         self.death_duration = 30
#         if not sprites.has(self):
#             sprites.add(self)
#
#     def move_lr(self, dir):
#         self.dx += dir * 4
#
#     def gravity(self, gravity):
#         self.dy += gravity
#
#     def jump(self, value):
#         if not self.in_air:
#             self.rect.y = int(self.rect.y)
#             self.dy = 0
#             self.dy -= value
#             self.in_air = True
#
#     def is_in_air(self):
#         pass
#
#     def update(self):
#         if self.alive:
#             if self.dx > 0:
#                 self.image = pygame.image.load(os.path.join(sprites_folder, 'player_right.png')).convert_alpha()
#             elif self.dx < 0:
#                 self.image = pygame.image.load(os.path.join(sprites_folder, 'player_left.png')).convert_alpha()
#             elif self.dx == 0:
#                 self.image = pygame.image.load(os.path.join(sprites_folder, 'player.png')).convert_alpha()
#             self.rect.x += self.dx
#             self.collide("x", walls)
#             self.dx = 0
#             self.rect.y += self.dy
#             self.collide("y", walls)
#
#         else:
#             if self.death_frame == 0:
#                 self.dy = 0
#             self.rect.y += self.dy
#             if self.death_frame % 10 == 0:
#                 self.image = pygame.image.load(os.path.join(sprites_folder, 'player_inverted.png')).convert_alpha()
#             elif self.death_frame % 10 == 5:
#                 self.image = pygame.image.load(os.path.join(sprites_folder, 'player.png')).convert_alpha()
#             self.death_frame += 1
#
#     def collide(self, axis, tiles):
#         if axis == "x":
#             for tile in tiles:
#                 if self.rect.colliderect(tile.rect):
#                     if self.dx > 0:
#                         self.rect.right = tile.rect.left
#                     if self.dx < 0:
#                         self.rect.left = tile.rect.right
#                     return
#         else:
#             for tile in tiles:
#                 if self.rect.colliderect(tile.rect):
#                     if self.dy >= 0:
#                         self.rect.bottom = tile.rect.top
#                         self.in_air = False
#                     if self.dy < 0:
#                         self.rect.top = tile.rect.bottom
#                     self.dy = 0
#                     return
#         # self.in_air = True
#
#     def show(self):
#         pygame.draw.rect(camera, (255, 0, 0), self.rect)
#         camera.blit(self.image, self.rect)


# Testing area
if __name__ == "__main__":
    p = Player((0, 0))
    p.show()

    screen.blit(camera, (0, 0))
    pygame.display.update()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
