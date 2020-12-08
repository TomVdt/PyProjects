import kandinsky as k
import random, math
from time import sleep
import pygame, sys

background = (0,0,0)

def rotate(a, n):
	"""Rotates grid n quarter turns in the trigonometric direction"""
	b = [x[:] for x in a]
	cx, cy = (len(a)-1)/2, (len(a[0])-1)/2
	w = -math.pi/2 * n
	for y in range(len(a)):
		for x in range(len(a[0])):
			x_ = round(math.cos(w)*(x-cx) - math.sin(w)*(y-cy) + cx)
			y_ = round(math.sin(w)*(x-cx) + math.cos(w)*(y-cy) + cy)
			b[y_][x_] = a[y][x]
	return b
if __name__ == '__main__':
	print(rotate([[1,0,0],[2,3,0],[0,0,0]], -1))
	print(rotate([[1,0,0],[2,3,0],[0,0,0]], 1))
	print(rotate([[1,0,0,0],[2,3,0,0],[0,0,0,0],[0,0,0,0]], 1))
	print(rotate([[1,0,0,0],[2,3,0,0],[0,0,0,0],[0,0,0,0]], -1))
	print(rotate([[1,0,0,0],[2,3,0,0],[0,0,0,0],[0,0,0,0]], 4))

class Grid:
	"""Grid manager for the game"""
	def __init__(self, size=4, new=[2, 2, 2, 4], empty=0):
		self.grid = [[0] * size for _ in range(size)]
		self.new = new
		self.empty = empty
		self.score = 0
		self.size = size
	def __repr__(self) -> str:
		res = ''
		for line in self.grid:
			for cell in line:
				res += str(cell)
			res += '\n'
		return res
	"""Place a random number (new=2) somewhere on the grid"""
	def rand(self):
		avail = [(x, y) for y, line in enumerate(self.grid) for x, cell in enumerate(line) if cell == self.empty]
		x, y = random.choice(avail)
		self.grid[y][x] = random.choice(self.new)
	"""Slide cubes to the side"""
	def slide(self, direction):
		dir2rot = {'down': 0, 'left': 1, 'up': 2, 'right': -1}
		# Rotate to make given direction face down
		self.grid = rotate(self.grid, dir2rot[direction])
		# Apply "gravity"
		def fall():
			for x in range(self.size):
				for y in range(self.size-1, -1, -1):
					# Skip empty cells
					if self.grid[y][x] == self.empty:
						continue
					y_ = y
					# Fuse down empty cells
					while y_ < self.size-1 and self.grid[y_+1][x] == self.empty:
						y_ += 1
					# Swap values (if same cell, value is kept)
					cell = self.grid[y][x]
					self.grid[y][x] = self.empty
					self.grid[y_][x] = cell
		# Combine cells down once
		def combine():
			for x in range(self.size):
				for y in range(self.size-1, 0, -1):
					# Fuse down if possible
					if self.grid[y-1][x] == self.grid[y][x]:
						self.grid[y-1][x] += self.grid[y][x]
						self.grid[y][x] = self.empty
						self.score += self.grid[y-1][x]
		fall()
		combine()
		fall()
		# Rotate back
		self.grid = rotate(self.grid, -dir2rot[direction])

	"""Detect if stuck (grid complete + no move possible)"""
	def stuck(self) -> bool:
		# Try to find an empty spot
		for line in self.grid:
			for cell in line:
				if cell == self.empty:
					return False
		# Otherwise, check if another move is possible
		for y, line in enumerate(self.grid):
			for x, cell in enumerate(line):
				neigh_x, neigh_y = [], []
				if x-1 > -1: neigh_x.append(x-1)
				if x+1 < self.size: neigh_x.append(x+1)
				if y-1 > -1: neigh_y.append(y-1)
				if y+1 < self.size: neigh_y.append(y+1)
				# Check all neighbors
				for x_ in neigh_x:
					for y_ in neigh_y:
						if self.grid[y][x] == self.grid[y_][x_]:
							return False
		# Player is stuck
		return True

def render(grid):
    size = int(222/4 - 3)
    x = 320/4 -3
    y = 0
    for i in grid:
        k.fill_rect(x,y,size,size,(100,25,39))
        k.draw_string(i,x,y,(0,0,0),(100,25,39))
        x += size
        if x == 320/4 - 3 + size*4:
            x = 320/4 -3
            y += size


def game():
    grid = Grid()
    grid.rand()
    grid.rand()
    k.fill_rect(0,0,320,222,background)
    game = True
    while game:
        render(grid.__repr__())
        
        mv = str(input())
        grid.slide(mv)
        grid.rand()
