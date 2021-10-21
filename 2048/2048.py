import random
from time import sleep
import pygame

length = 200
windowWidth = 500
windowHeight = 500
spacing = 2
margin = 10
field = [[0,512,0,0] for i in range(4)]

pygame.init()
window = pygame.display.set_mode((windowWidth, windowHeight))
font = pygame.font.SysFont('Comic Sans MS', 10)
pygame.display.set_caption("2048")


def hsv_to_rgb(h, s, v):
    if s == 0.0: v*=255; return (v, v, v)
    i = int(h*6.)
    f = (h*6.)-i; p,q,t = int(255*(v*(1.-s))), int(255*(v*(1.-s*f))), int(255*(v*(1.-s*(1.-f)))); v*=255; i%=6
    if i == 0: return (v, t, p)
    if i == 1: return (q, v, p)
    if i == 2: return (p, v, t)
    if i == 3: return (p, q, v)
    if i == 4: return (t, p, v)
    if i == 5: return (v, p, q)

def randomTile(field):
    emptyTiles = 0
    for row in field:
        for pos in row:
            if pos == 0:
                emptyTiles += 1
    newTilePos = int(random.randrange(1,emptyTiles+1))
    for row in range(4):
        for pos in range(4):
            if field[row][pos] == 0:
                newTilePos -= 1
            if newTilePos == 0:
                field[row][pos] = random.choice([2,2,2,4])
                return field
                

def move(field, sens):
    return                

def draw(field):
    tileSize = int(min(windowHeight, windowWidth)/4-spacing*2-margin/2)
    window.fill((69,69,69))
    for row in range(4):
        textX = int(tileSize / 2 + margin + spacing + spacing*2*row + tileSize*row)
        tileX = int(margin + spacing + spacing*2*row + tileSize*row)
        for col in range(4):
            textY =int(tileSize / 2 + margin + spacing + spacing*2*col + tileSize*col)
            tileY = int(margin + spacing + spacing*2*col + tileSize*col)
            color = hsv_to_rgb(field[row][col]/2048*360,1,1)
            if field[row][col] != 0:
                pygame.draw.rect(window, color, (tileX, tileY, tileSize, tileSize))
                window.blit(font.render(str(field[row][col]), False, (255, 255, 255)),(textX,textY))
    pygame.display.update()
    sleep(5)
        

def game(field):
    events = pygame.event.get()
    field = randomTile(field)
    game = True
    while game:
        draw(field)
        game = False

game(field)
pygame.quit()
