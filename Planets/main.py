from vars import *
from vector import Vector
from planet import Planet


def draw():
    # planets = [planet(random.randrange(0, width), random.randrange(
    #    0, height), random.randrange(50, 150)) for i in range(2)]
    # for planet in planets:
    #    planet.vel = Vector.random2D() * 5
    planets = []
    planets.append(Planet(500, 150, 1))
    planets.append(Planet(500, 600, 1))
    planets.append(Planet(500, 375, 1000))
    planets[0].vel.set(2, 0)
    planets[1].vel.set(-2, 0)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.mouse:
                pass

        camera.fill((background_color))

        mouse = pygame.mouse.get_pos()
        camera_x = int(mouse[0] / 10)
        camera_y = int(mouse[1] / 10)

        for i in range(len(planets)):
            for j in range(len(planets)):
                if i != j:
                    planets[i].attract(planets[j].pos, planets[j].mass)

        for planet in planets:
            planets[2].acc *= 0
            planet.update()
            # planet.border()
            planet.show()

        # screen.blit(camera, (0 - camera_x, 0 - camera_y))
        # camera.scroll(int(width / 2 - planets[2].pos[0]), int(height / 2 - planets[1].pos[1]))
        screen.blit(camera, (0, 0))
        pygame.display.update()

        clock.tick(60)


draw()
