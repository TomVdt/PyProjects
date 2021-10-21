import os
import sys

import pygame as pg


CAPTION = "Flashing Screen"
SCREEN_SIZE = (500, 500)
DELAY = 500


class App(object):
    def __init__(self):
        self.screen = pg.display.get_surface()
        self.clock = pg.time.Clock()
        self.fps = 60
        self.done = False
        self.timer = 0
        self.change = False
        self.color = pg.Color("black")

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True

    def update(self, dt):
        self.timer += dt
        while self.timer >= DELAY:
            self.timer -= DELAY
            self.change = not self.change
            if self.change:
                self.color = pg.Color("cyan")
            else:
                self.color = pg.Color("black")

    def main_loop(self):
        dt = 0
        self.clock.tick()
        while not self.done:
            self.event_loop()
            self.update(dt)
            self.screen.fill(self.color)
            pg.display.update()
            dt = self.clock.tick(self.fps)


def main():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    pg.display.set_caption(CAPTION)
    pg.display.set_mode(SCREEN_SIZE)
    App().main_loop()
    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
