import pygame
import os
import sys
import time

width = 800
height = 600
background_color = (220, 220, 220)

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (20, 40)
pygame.init
screen = pygame.display.set_mode((width, height))
screen.fill(background_color)
pygame.display.set_caption("Impossible Mode Pixel editor")

grid = pygame.Surface((width, height), flags=pygame.SRCALPHA)
for x in range(20):
    pygame.draw.line(grid, (0, 0, 0, 50), (x * 40, 0), (x * 40, height))
for y in range(15):
    pygame.draw.line(grid, (0, 0, 0, 50), (0, y * 40), (width, y * 40))

sprites = pygame.sprite.Group()

game_folder = os.path.dirname(__file__)
sprites_folder = os.path.join(game_folder, 'sprites')

clock = pygame.time.Clock()


class Tile(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, 40))
        self.image.fill((220, 220, 220))
        self.rect = self.image.get_rect()
        sprites.add(self)
        self.rect.x = x
        self.rect.y = y
        self.type = "none"
        self.do_offset = False
        self.offset = 0
        self.rot = 0

    def change_rot(self):
        center = self.rect.center
        self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect(center=center)

    def change_type(self, type):
        self.type = type
        if type == "wall":
            self.image = pygame.image.load(os.path.join(sprites_folder, type + '.png')).convert_alpha()
        if type == "vertical_beam":
            self.image = pygame.image.load(os.path.join(sprites_folder, type + '.png')).convert_alpha()
        if type == "spike":
            self.image = pygame.image.load(os.path.join(sprites_folder, type + '.png')).convert_alpha()
        if type == "horizontal_beam":
            self.image = pygame.image.load(os.path.join(sprites_folder, type + '.png')).convert_alpha()
        if type == "chains":
            self.image = pygame.image.load(os.path.join(sprites_folder, type + '.png')).convert_alpha()
        if type == "center_beam":
            self.image = pygame.image.load(os.path.join(sprites_folder, type + '.png')).convert_alpha()
        if type == "player":
            self.image = pygame.image.load(os.path.join(sprites_folder, type + '.png')).convert_alpha()
        if type == "ending":
            self.image = pygame.image.load(os.path.join(sprites_folder, type + '.png')).convert_alpha()
        if type == "none":
            self.image = pygame.Surface((40, 40))
            self.image.fill((220, 220, 220))

    def show(self):
        pygame.draw.rect(screen, (220, 220, 220), self.rect)
        if self.do_offset:
            pygame.draw.circle(screen, (255, 0, 0), self.rect.center, 5)
        else:
            pygame.draw.circle(screen, (220, 220, 220), self.rect.center, 5)
        screen.blit(self.image, self.rect)

    def highlight(self):
        pygame.draw.rect(screen, (252, 246, 179), self.rect)


def generate_level(tiles, level_nb):
    tile_dict = {
        "wall": "W",
        "vertical_beam": "v",
        "spike": {0: "S",
                  2: "s",
                  3: "z",
                  1: "Z"
                  },
        "horizontal_beam": "h",
        "chains": {True: "c",
                   False: "C"
                   },
        "center_beam": "b",
        "none": " ",
        "player": "P",
        "ending": "E"
    }
    output = ["" for i in range(15)]
    for y in range(15):
        for x in range(20):
            if tiles[x + y * 20].type == "spike":
                output[y] += str(tile_dict[tiles[x + y * 20].type][tiles[x + y * 20].rot])
            elif tiles[x + y * 20].type == "chains":
                output[y] += str(tile_dict[tiles[x + y * 20].type][tiles[x + y * 20].do_offset])
            else:
                output[y] += str(tile_dict[tiles[x + y * 20].type])

    with open('levels.txt', 'a') as out:
        out.write("'level" + str(level_nb) + "': [")
        for i in output:
            out.write("'" + i + "',\n")
            print(i)
        out.seek(out.tell() - 3, os.SEEK_SET)
        out.truncate()
        out.write("],")
        out.write("\n")
        out.close()


def draw():
    tiles = []
    sprite_list = {2: "wall",
                   4: "vertical_beam",
                   3: "spike",
                   5: "horizontal_beam",
                   7: "chains",
                   6: "center_beam",
                   1: "none",
                   0: "player",
                   9: "ending"
                   }

    for y in range(15):
        for x in range(20):
            tiles.append(Tile(x * 40, y * 40))

    cursor = pygame.Rect((1, 1), (1, 1))
    click = False
    clicked = False
    index = 1
    level_nb = 0

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
            if event.type == pygame.MOUSEBUTTONUP:
                click = False
                clicked = False

        screen.fill((220, 220, 220))

        cursor.center = pygame.mouse.get_pos()

        key = pygame.key.get_pressed()
        if key[pygame.K_0]:
            index = 0
        if key[pygame.K_1]:
            index = 1
        if key[pygame.K_2]:
            index = 2
        if key[pygame.K_3]:
            index = 3
        if key[pygame.K_4]:
            index = 4
        if key[pygame.K_5]:
            index = 5
        if key[pygame.K_6]:
            index = 6
        if key[pygame.K_7]:
            index = 7
        if key[pygame.K_9]:
            index = 9
        if key[pygame.K_r]:
            index = 33
        if key[pygame.K_f]:
            index = 44
        if key[pygame.K_SPACE]:
            generate_level(tiles, level_nb)
            level_nb += 1
            time.sleep(1)

        for tile in tiles:
            if cursor.colliderect(tile):
                tile.highlight()
                if click:
                    if index == 33 and not clicked:
                        tile.rot += 1
                        tile.rot %= 4
                        tile.change_rot()
                    elif index == 44 and not clicked:
                        tile.do_offset = not tile.do_offset
                    elif 0 <= index <= 9:
                        tile.change_type(sprite_list[index])
                        tile.rot = 0
                    clicked = True
            tile.show()

        screen.blit(grid, (0, 0))
        pygame.display.update()

        clock.tick(60)


draw()
