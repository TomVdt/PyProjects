import kandinsky as k
from time import sleep
import pygame
#import ez_console

width = 320
height = 222
colors = {
             "1red": (255,0,0),
             "2green": (0,255,0),
             "3blue": (0,0,255),
             "4yellow": (255,255,0),
             "5pink": (255,0,255),
             "6cyan": (0,255,255),
             "7black": (0,0,0),
             "8grey":(128,128,128),
             "9white": (255,255,255)
             }
c = []
for x in colors:
  c.append(x)
c.sort()

def pen(x,y,size,color):
  k.fill_rect(x-int(size/2),y-int(size/2),size,size,color)

def fill(x,y,color):
  old_col = k.get_pixel(x,y)
  left,up,right,down = 0,-1,0,0
  while k.get_pixel(x-left,y)==old_col and x!=0:
    k.set_pixel(x-left,y,color)
    pygame.event.wait()
    left += 1
    up = -1
    while k.get_pixel(x-up,y)==old_col and x!=0:
      k.set_pixel(x-up,y,color)
      up += 1
  while k.get_pixel(x-right,y)==old_col and x!=0:
    k.set_pixel(x-right,y,color)
    right += 1
  while k.get_pixel(x-down,y)==old_col and x!=0:
    k.set_pixel(x-down,y,color)
    down += 1

def cursor(x,y):
  old_col = k.get_pixel(x,y)
  k.set_pixel(x,y,(128,128,128))
  return old_col

def main():
  size = 2
  x = int(width/2)
  y = int(height/2)
  k.set_pixel(x,y,(248,252,248))
  mv = 0
  r,g,b = 0,0,0
  color = (r,g,b)
  old_col = cursor(x,y)
  run = True
  while run:
#    for i in k.get_keys():
#      if i=="left" and x>0:
#        k.set_pixel(x,y,old_col)
#        x-=1
#        mv = 1
#      elif i=="right" and x<width-1:
#        k.set_pixel(x,y,old_col)
#        x+=1
#        mv = 1
#      elif i=="up" and y>0:
#        k.set_pixel(x,y,old_col)
#        y-=1
#        mv = 1
#      elif i=="down" and y<height-1:
#        k.set_pixel(x,y,old_col)
#        y+=1
#        mv = 1
#      elif i=="OK":
#        pen(x,y,size,color)
#        mv = 1
#      elif i=="+":
#        size += 1
#        sleep(0.1)
#      elif i=="-":
#        size -= 1
#        sleep(0.1)
#      elif i in [str(n) for n in range(1,10)]:
#        color = colors[c[int(i)-1]]
#      elif i=="0":
#        k.fill_rect(0,0,width,height,(248,252,248))
#        sleep(0.1)
#        main()
    x = 60
    for ys in range(222):
      pen(x,ys,size,(0,0,255))
      pygame.event.wait()
    x = 160
    fill(x,y,(255,0,0))
    y+=1

    if mv==1:
      old_col = cursor(x,y)
      mv = 0
    sleep(0.02)
