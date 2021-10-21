import random
from time import sleep
import pygame
from pydub import AudioSegment
from pydub.generators import Sine
from pydub.playback import play

length = 200
windowWidth = 1000
windowHeight = 500
spacing = 2
margin = 10

pygame.init()
window = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("Sorter")


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

def randomize(bars, l):
    barsRand = []
    for i in range(l):
        barsRand.append(bars.pop(bars.index(random.choice(bars))))
    if barsRand == bars:
        randomize(bars, l)
    else:
        return barsRand

def sort(bars):
    checkAmount = 1
    changes = 1
    while changes != 0:
        changes = 0
        for i in range(len(bars)-checkAmount):
            draw(bars, i)
            sleep(0.0001)
            if bars[i] > bars[i+1]:
                bars[i+1], bars[i] = bars[i], bars[i+1]
                changes += 1
        checkAmount += 1

def draw(bars, marker):
    width = ((windowWidth - (spacing*length) - margin*2) / length)
    chunckHeight = ((windowHeight - (margin*2)) / length)
    window.fill((69,69,69))
    pos = 0
    for i in bars:
        color = hsv_to_rgb((i+1)/length, 1, 1)
        x = margin + spacing/2 + pos*width + pos*spacing
        y = margin
        height = (i + 1) * chunckHeight
        pos += 1
        pygame.draw.rect(window, color, (x, y, width, height))
    pygame.draw.rect(window, (255,255,255), (margin + spacing/2 + marker*width + marker*spacing + int(width/2) - margin/4, int(margin/4), margin/2, margin/2))
    pygame.display.update()

def main(l):
    hue = 0
    bars = [i for i in range(l)]
    barsRand = randomize(bars, l)
    draw(barsRand, 0)
    sort(barsRand)

main(length)
pygame.quit()
