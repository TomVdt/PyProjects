from time import sleep
import pygame

background = (0,0,0)
windowWidth = 1000
windowHeight = 500
spacing = 2
margin = 10

pygame.init()
window = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("Game of Life")

def toggle(x,y):
  if field[y][x]==0:
    return 1
  else:
    return 0

def simu():
  newfield = [[0 for i in range(xlen+2)] for i in range(ylen+2)]
  for x in range(1,xlen+1):
    for y in range(1,ylen+1):
      fren = field[y-1][x-1]+field[y-1][x]+field[y-1][x+1]+field[y][x-1]+field[y][x+1]+field[y+1][x-1]+field[y+1][x]+field[y+1][x+1]
      if 2==fren and field[y][x]==1:
        newfield[y][x]=1
      elif fren==3:
        newfield[y][x]=1
      else:
        newfield[y][x]=0
  return newfield

def draw():
  global lastgamestate
  mv = int(size)+spacing
  x, y = margin+int(spacing/2), margin+int(spacing/2)
  for ypos in range(1,ylen+1):
    for xpos in range(1,xlen+1):
      if lastgamestate[ypos][xpos] != field[ypos][xpos]:
        if field[ypos][xpos]==1:
          pygame.draw.rect(window, (255,255,255), (x,y,int(size),int(size)))
        else:
          pygame.draw.rect(window, (25,25,25), (x,y,int(size),int(size)))
      lastgamestate[ypos][xpos] = field[ypos][xpos]
      x += mv
    y += mv
    x = margin+int(spacing/2)
  pygame.display.update()

def cur(xpos,ypos):
  x = margin+int((spacing/2)+(size/2))
  pygame.draw.rect(window, (150,150,150), (x+xpos*round(size)+spacing,x+ypos*round(size)+spacing,2,2))
  pygame.display.update()

def init(l):
  global size, xlen, ylen, field, lastgamestate
  xspace = windowWidth-(spacing*int(windowWidth/windowHeight*l))-margin*2
  yspace = windowHeight-(spacing*l)-margin*2
  size = min(xspace,yspace)/l
  xlen = int(xspace/size)
  ylen = int(yspace/size)
  if int(size)==0:
    print("Unable to display with current size")
    return
  field = [[0 for i in range(xlen+2)] for i in range(ylen+2)]
  lastgamestate = [[1 for i in range(xlen+2)] for i in range(ylen+2)]
  window.fill(background)
  draw()
  simu()

def main(l=50):
  global field
  init(l)
  run = True
  xcur, ycur = 1,1
  while run:
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]==1 and xcur>1:
      xcur-=1
      cur(xcur-1,ycur-1)
    elif key[pygame.K_RIGHT]==1 and xcur<len(field[0])-2:
      xcur+=1
      cur(xcur-1,ycur-1)
    elif key[pygame.K_UP]==1 and ycur>1:
      ycur-=1
      cur(xcur-1,ycur-1)
    elif key[pygame.K_DOWN]==1 and ycur<len(field)-2:
      ycur+=1
      cur(xcur-1,ycur-1)
    elif key[pygame.K_SPACE]==1:
      field[ycur][xcur] = toggle(xcur,ycur)
      draw()
    elif key[pygame.K_RETURN]==1:
      field = simu()
      draw()
    elif key[pygame.K_ESCAPE]==1:
      pygame.quit()
      return
    elif key[pygame.K_BACKSPACE]==1:
      if autosimu == 0:
        autosimu = 1
      else:
        autosimu = 0
    pygame.event.wait()

main()
