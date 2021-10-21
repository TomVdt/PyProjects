import pygame
import math
from metaball import Metaball
from vector import Vector

# Initialize pygame
width = 200
height = 200

pygame.init
screen = pygame.display.set_mode((width, height))
screen.fill((0, 0, 0))
pygame.display.set_caption("Metaballs")

tick = pygame.time.Clock()

# Gloabal variables

pxarray = pygame.PixelArray(screen)
metaballs = [Metaball(width, height) for i in range(3)]


def hsv_to_rgb(h, s, v):
    if s == 0.0:
        v *= 255
        return (v, v, v)
    i = int(h * 6.)  # XXX assume int() truncates!
    f = (h * 6.) - i
    p, q, t = int(255 * (v * (1. - s))), int(255 *
                                             (v * (1. - s * f))), int(255 * (v * (1. - s * (1. - f))))
    v *= 255
    i %= 6
    if i == 0:
        return (v, t, p)
    if i == 1:
        return (q, v, p)
    if i == 2:
        return (p, v, t)
    if i == 3:
        return (p, q, v)
    if i == 4:
        return (t, p, v)
    if i == 5:
        return (v, p, q)


def dist(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def draw():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for x in range(width):
            for y in range(height):
                sum = 0
                for i in metaballs:
                    d = dist(x, y, i.pos.x, i.pos.y)
                    if d != 0:
                        sum += int(100 * i.radius / d)
                if sum > 220:
                    sum = 220
                pxarray[x, y] = tuple(hsv_to_rgb(sum / 255, 1, 1))

        # pygame.draw.circle(screen, (255,0,0), (int(metaballs[0].pos.x),int(metaballs[0].pos.y)), metaballs[0].radius)
        for i in metaballs:
            i.update()

        pygame.display.update()

        tick.tick(30)


draw()
