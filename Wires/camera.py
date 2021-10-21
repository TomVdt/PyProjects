from button import Button
from vars import *


class Chunk:

    def __init__(self, pos, tile_size=10, size=16):
        self.pos = pos
        self.size = size
        self.tile_size = tile_size

    def draw(self):
        for x in range(0, self.pos[0] * self.tile_size * self.size, self.tile_size):
            for y in range(0, self.pos[1] * self.tile_size * self.size, self.tile_size):
                pg.draw.rect(screen, GREY, (x, y, self.tile_size, self.tile_size), 2)


class World:

    def __init__(self, *args):
        self.chunks = [Chunk((i % 4, i // 4)) for i in range(16)]
        self.run = True
        self.loop()

    def click(self):
        for button in buttons:
            if button.rect.collidepoint(pg.mouse.get_pos()):
                button.press()
                break

    def render(self):
        for chunk in self.chunks:
            chunk.draw()
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.run = False
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                self.click()

    def loop(self):
        while self.run:
            self.events()

            self.render()

            clock.tick(60)


World()
