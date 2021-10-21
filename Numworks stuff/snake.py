from time import *
from random import randint, choice
import pygame
import kandinsky as k

background = (0,0,0)
windowWidth = 320
windowHeight = 222
spacing = 0
margin = 0
rainbow = 1 #False
peace = 0  #True

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

def grid():
  mv = size+spacing
  x, y = margin, margin
  for ypos in range(ylen):
    for xpos in range(xlen):
      k.fill_rect(round(x),round(y),int(size),int(size),(25,25,25))
      x += mv
    y += mv
    x = margin

def draw(c=(255,0,0)):
  global headpos, tailpos, xf, yf
  mv = size+spacing
  x, y = margin, margin
  k.fill_rect(round(x+mv*tailpos[0]),round(y+mv*tailpos[1]),int(size),int(size),(25,25,25))
  k.fill_rect(round(x+mv*headpos[0]),round(y+mv*headpos[1]),int(size),int(size),c)
  k.fill_rect(round(x+mv*xf),round(y+mv*yf),int(size),int(size),(255,0,0))

def init(l,showMargin=False):
  global size, xlen, ylen, headpos, snakepos
  xspace = windowWidth-margin*2-spacing*(l-1)
  yspace = windowHeight-margin*2-spacing*(l-1)
  size = min(xspace,yspace)/l
  if windowWidth>=windowHeight:
    ylen = l
    xlen = int((l*windowWidth)/windowHeight)
  else:
    xlen = l
    ylen = int((l*windowHeight)/windowWidth)
  if int(size)==0:
    print("Unable to display with current size")
    return True

  headpos = [int(xlen/2),int(ylen/2)]
  snakepos = [[int(xlen/2)-2,int(ylen/2)],[int(xlen/2)-1,int(ylen/2)],[int(xlen/2),int(ylen/2)]]

  k.fill_rect(0,0,windowWidth,windowHeight,background)
  if showMargin:
    k.fill_rect(0,0,margin,windowHeight,(55,55,55))
    k.fill_rect(0,windowHeight-margin,windowWidth,margin,(55,55,55))
    k.fill_rect(0,0,windowWidth,margin,(55,55,55))
    k.fill_rect(windowWidth-margin,0,margin,windowHeight,(55,55,55))

  grid()
  fruit()

def fruit():
  global xf,yf
  xf = randint(0,xlen-1)
  yf = randint(0,ylen-1)
  for i in snakepos:
    if i[0]==xf and i[1]==yf:
      fruit()

def snake(dir):
  global snakepos, headpos, tailpos, xf, yf, xlen, ylen
  if dir==1:
    headpos[0] -= 1
    if peace:
      if headpos[0]==-1:
        headpos[0] = xlen-1
  elif dir==2:
    headpos[1] -= 1
    if peace:
      if headpos[1]==-1:
        headpos[1] = ylen-1
  elif dir==3:
    headpos[0] += 1
    if peace:
      if headpos[0]==xlen:
        headpos[0] = 0
  elif dir==4:
    headpos[1] += 1
    if peace:
      if headpos[1]==ylen:
        headpos[1] = 0
  snakepos.append(list(headpos))
  tailpos = snakepos.pop(0)
  if headpos[0]==xf and headpos[1]==yf:
    snakepos.insert(0,tailpos)
    fruit()

def hit():
  global snakepos, headpos, xlen, ylen
  if headpos[0]>xlen-1 or headpos[0]<0 or headpos[1]>ylen-1 or headpos[1]<0:
    return True
  for i in range(len(snakepos)):
    if snakepos.count(snakepos[i])!=1:
      return True
  return False

def ai():
  global snakepos, headpos, xf, yf, xlen, ylen
  snek = list(snakepos)
  snek.pop(0)
  if headpos[0]<xf:
    if not [headpos[0]+1,headpos[1]] in snek:
      return 3
    else:
      if not [headpos[0],headpos[1]-1] in snek and headpos[1]!=0:
        return 2
      if not [headpos[0],headpos[1]+1] in snek and headpos[1]!=ylen-1:
        return 4
      return 1
  if headpos[0]>xf:
    if not [headpos[0]-1,headpos[1]] in snek:
      return 1
    else:
      if not [headpos[0],headpos[1]-1] in snek and headpos[1]!=0:
        return 2
      if not [headpos[0],headpos[1]+1] in snek and headpos[1]!=ylen-1:
        return 4
      return 3
  if headpos[1]<yf:
    if not [headpos[0],headpos[1]+1] in snek:
      return 4
    else:
      if not [headpos[0]-1,headpos[1]] in snek and headpos[0]!=0:
        return 1
      if not [headpos[0]+1,headpos[1]] in snek and headpos[0]!=xlen-1:
        return 3
      return 2
  if headpos[1]>yf:
    if not [headpos[0],headpos[1]-1] in snek:
      return 2
    else:
      if not [headpos[0]-1,headpos[1]] in snek and headpos[0]!=0:
        return 1
      if not [headpos[0]+1,headpos[1]] in snek and headpos[0]!=xlen-1:
        return 3
      return 4

def main(l=12,speed=0.2,auto=False):
  global run
  if init(l):
    return
  run = True
  d = 3
  ite = randint(0,360)
  while run:
    snake(d)
    if not peace:
      if hit():
        msg = str("{} Your score is {}".format(choice(["Oof.","Ouch!","Oh no!","Nope."]),len(snakepos)-3))
        print(msg)
        sleep(0.5)
        main(l,speed,auto)
    draw(hsv_to_rgb((ite%360)/360,int(rainbow),1))

    pygame.time.wait(speed)
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]==1:
        d = 1
    elif key[pygame.K_RIGHT]==1:
        d = 3
    elif key[pygame.K_UP]==1:
        d = 2
    elif key[pygame.K_DOWN]==1:
        d = 4
    elif key[pygame.K_SPACE]==1:
        sleep(0.5)
        main(l,speed,auto)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    if auto:
      d = ai()
    ite+=.5

main(25,5,1)
