from vars import *
from vector import Vector
from cocotte import Cocotte
from drop import Drop
from basket import Basket

def draw():
    poulets = [Cocotte(100+i*200, 75) for i in range(5)]
    basket = Basket()
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

        screen.fill(background)

        drop_nb = int(random.choice([i for i in range(len(poulets))]))
        luck += 0.001

        for i in range(len(poulets)):
            if drop_nb == i and len(poulets[i].pondu) == 0 and random.random() <= 0.005 + luck:
                luck = 0
                if abs(poulets[i].x - basket.x) >= width * 0.75:
                    poulets[i].pondre([70,5,25])
                else:
                    poulets[i].pondre()

            is_caught = poulets[i].get_caught(basket.x, basket.y, basket.w, basket.h)
            if is_caught == 'egg':
                egg += 1
            elif is_caught == 'poop':
                poop += 1
            elif is_caught == 'gold_egg':
                gold_egg += 1

            poulets[i].update(0.4)
            poulets[i].show()

        basket.move()
        basket.show()

        pygame.display.update()

        tick.tick(60)


draw()
