from button import Button
from vars import *


class Menu:

    def __init__(self, *args):
        pos = HEIGHT // 2 - ((len(args) - 1) * 60) // 2
        for arg in args:
            buttons.append(Button(arg[0], (WIDTH // 2, pos), arg[1]))
            pos += 60
        self.run = True
        self.loop()

    def click(self):
        for button in buttons:
            if button.rect.collidepoint(pg.mouse.get_pos()):
                button.press()
                break

    def render(self):
        for button in buttons:
            button.draw()
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


Menu(("Button 1", "test"), ("Button 2", "reset"), ("Button 3", "leave"), ("Button 4", "test"))
