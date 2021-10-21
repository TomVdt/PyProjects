import random, math
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.apply_force(-12)
                    bird.vel = 0

        screen.fill((0,0,0))

        # bird.y = pygame.math.Vector2(0, bird.y).lerp(pygame.math.Vector2(0, pygame.mouse.get_pos()[1]), 0.1).y
        # bird.x = abs(math.sin(val)) * 300
        # val += 0.02
        #bird.x = pygame.math.Vector2(bird.x, 0).lerp(pygame.math.Vector2(pygame.mouse.get_pos()[0], 0), 0.1).x

        for i in range(len(pipes)-1, 0, -1):
            pipes[i].update()
            pipes[i].show()
            if pipes[i].finished():
                pipes.pop(i)
            if pipes[i].hit(bird.x, bird.y, bird.size):
                pipes[i].color = (255,0,0)
            else:
                pipes[i].color = (255,255,255)

        bird.apply_force(0.7)
        bird.update()
        bird.show()

        pygame.display.update()

        tick.tick(60)


draw()
