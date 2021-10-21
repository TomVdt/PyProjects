import random
from vars import *
from vector import Vector
from bird import Bird
from pipe import Pipe

def draw():
    run = True
    pygame.time.set_timer(USEREVENT+1, 1000)
    val = 0
    pipes = [Pipe()]
    bird = Bird()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == USEREVENT+1:
                pipes.append(Pipe())

        screen.fill((0,0,0))

        for i in range(len(pipes)-1, 0, -1):
            pipes[i].update()
            pipes[i].show()
            if pipes[i].finished():
                pipes.pop(i)
            if pipes[i].hit(bird.x, bird.y, bird.size):
                pipes[i].color = (255,0,0)
            else:
                pipes[i].color = (255,255,255)

        bird.update(val)
        bird.show()
        val += 0.04

        pygame.display.update()

        tick.tick(60)


draw()
