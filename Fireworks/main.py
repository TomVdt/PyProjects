import pygame, random, math, vars
from vector import Vector
from firework import Firework
from particle import Particle

gravity = Vector(0,0.1)
fireworks = []

def draw():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        vars.fade.fill((0,0,0))
        vars.screen.blit(vars.fade, (0,0))

        if random.random() < 0.05:
            fireworks.append(Firework([random.randint(0,255),random.randint(0,255),random.randint(0,255)], vars.width, vars.height, gravity))

        for i in range(len(fireworks)-1, 0, -1):
            fireworks[i].update()
            fireworks[i].show()

            if fireworks[i].done():
                fireworks.pop(i)

        vars.pygame.display.update()

        vars.tick.tick(60)

draw()
