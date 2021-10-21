from vars import *
from vector import Vector
from cocotte import Cocotte
from drop import Drop
from basket import Basket

def draw():
    poulets = [Cocotte(100+i*200, 35+(math.sin(i*0.5+0.73866)*115)) for i in range(5)]
    basket = Basket()
    sprites.add(basket, poulets)
    egg = 0
    poop = 0
    gold_egg = 0
    luck = 0
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('Eggs caught: \t\t{} \nPoop caught: \t\t{} \nGolden eggs caught: \t{} \nTotal score: \t\t{}'.format(egg, poop, gold_egg, egg + 5*gold_egg - 3*poop))
                run = False

        screen.blit(background, (0,0))

        drop_nb = int(random.choice([i for i in range(len(poulets))]))
        luck += 0.0001
        pas_pondu = True

        for i in range(len(poulets)):
            if drop_nb == i and len(poulets[i].pondu) == 0 and random.random() <= 0.0001 + luck:
                luck = 0
                if abs(poulets[i].rect.x - basket.rect.x) >= width * 0.75:
                    poulets[i].pondre([70,5,25])
                else:
                    poulets[i].pondre()

            is_caught = poulets[i].get_caught(basket.rect)
            if is_caught == 'egg':
                egg += 1
            elif is_caught == 'poop':
                poop += 1
            elif is_caught == 'gold_egg':
                gold_egg += 1

            poulets[i].update_pos(0.4)

        basket.move()

        drop_sprites.update()
        sprites.update()
        drop_sprites.draw(screen)
        sprites.draw(screen)

        pygame.display.update()

        clock.tick(60)


draw()
