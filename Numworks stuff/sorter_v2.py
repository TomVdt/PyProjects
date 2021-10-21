import random
from time import sleep
import kandinsky as k

background = (0,0,0)
windowWidth = 320
windowHeight = 222
spacing = 2
margin = 10

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
    return

def bubble(bars):
    checkAmount = 1
    changes = 1
    while changes != 0:
        changes = 0
        for i in range(len(bars)-checkAmount):
            if bars[i] > bars[i+1]:
                bars[i+1], bars[i] = bars[i], bars[i+1]
                changes = 1
            draw(bars,[i,i+1])
            sleep(1/len(bars))
        checkAmount += 1

def draw(bars, marker):
    for i in marker:
        color = hsv_to_rgb((bars[i]+1)/length, 1, 1)
        x = margin + spacing/2 + i*width + i*spacing
        y = margin
        height = (bars[i]+1) * chunckHeight
        k.fill_rect(int(x), int(y), int(width), 222-2*margin, background)
        k.fill_rect(int(x), int(y), int(width), int(height), color)
    k.draw_string("Length: "+str(length),margin,208-margin,(255,255,255),background)
    k.fill_rect(0,0,windowWidth,margin,background)
    k.fill_rect(int(margin+spacing/2+marker[0]*width+marker[0]*spacing+width-margin/4), int(margin/4), int(margin/2), int(margin/2), (255,255,255))

def main(l=25):
    global length,width,chunckHeight
    length = l
    width = ((windowWidth-(spacing*l)-margin*2)/l)
    chunckHeight = ((windowHeight-(margin*2))/l)
    if int(width)==0:
        print("Unable to display with current list size")
        return
    bars = randomize([i for i in range(l)], l)
    k.fill_rect(0,0,windowWidth,windowHeight,background)
    for i in range(l-1):
        draw(bars, [i, i+1])
    bubble(bars)

main()
