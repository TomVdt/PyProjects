from math import sin, cos, pi


class Vec2:

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __index__(self, i):
		if i == 0:
			return self.x
		if i == 1:
			return self.y
		else:
			raise IndexError

	def __repr__(self):
		return f'Vec2 {self.x}, {self.y}'

	def __add__(self, vec):
		return Vec2(self.x + vec.x, self.y + vec.y)

	def __sub__(self, vec):
		return Vec2(self.x - vec.x, self.y - vec.y)

	def __mul__(self, k):
		return Vec2(self.x * k, self.y * k)

	def __truediv__(self, k):
		return Vec2(self.x / k, self.y / k)

	def __floordiv__(self, k):
		return Vec2(self.x // k, self.y // k)

	def norm(self):
		mag = self.mag()
		self.x /= mag
		self.y /= mag
		return self

	def mag2(self):
		return self.x ** 2 + self.y ** 2

	def mag(self):
		return self.mag2() ** 0.5

	def set_pos(self, x, y):
		self.x, self.y = x, y
		return self

	def rotate(self, theta):
		x = cos(theta)
		y = sin(theta)
		return Vec2(x, y)

	@classmethod
	def dot(cls, v1, v2):
		return (v1.x * v2.x) - (v1.y * v2.y)


if __name__ == '__main__':
	v = Vec2(3, 4)
	print(v, v.mag())
	v.rotate(pi / 2)
	print(v, v.mag())
