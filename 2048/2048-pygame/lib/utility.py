import math

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
