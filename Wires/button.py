from vars import *


class Button:

    def __init__(self, text, pos, action, bg=WHITE, fg=BLACK, highlight=GREY, size=(300, 50), centered=True, font="Comic Sans MS", font_size=16):
        self.color = bg

        self.bg = bg
        self.fg = fg  # text color
        self.hover = highlight
        self.size = size

        self.font = pg.font.SysFont(font, font_size)
        self.text = self.font.render(text, 1, self.fg)
        self.text_rect = self.text.get_rect()

        self.surface = pg.surface.Surface(self.size)
        self.rect = self.surface.get_rect(center=pos)

        if centered:
            self.text_rect.center = [i // 2 for i in self.size]
        else:
            self.text_rect.topleft = (0, (self.size[1] - self.text_rect.height) // 2)

        self.action = action

    def on_hover(self):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            self.color = self.hover
        else:
            self.color = self.bg

    def actions(self):
        print({"test": 1, "reset": 2, "leave": 3}[self.action])

    def press(self):
        self.actions()

    def draw(self):
        self.on_hover()

        self.surface.fill(self.color)
        self.surface.blit(self.text, self.text_rect)
        screen.blit(self.surface, self.rect)
