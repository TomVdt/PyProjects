# import pygame as pg
import numpy as np


class Object3D:

	def __init__(self, file):
		self.mesh = self.load_from_file(file)

	def load_from_file(self, file):
		with open(file, 'r') as f:
			verts = []
			tris = []
			for line in f.readlines():
				components = line[:-1].split(' ')
				if components[0] == 'v':
					verts.append(np.array(components[1:]).astype(float))
				elif components[0] == 'f':
					p1 = int(components[1]) - 1
					p2 = int(components[2]) - 1
					p3 = int(components[3]) - 1
					tris.append(Tri(verts[p1], verts[p2], verts[p3]))
			f.close()
		return tris


class Tri:

	def __init__(self, p1=(0, 0, 0), p2=(0, 0, 0), p3=(0, 0, 0)):
		self.points = [
			np.array((*p1, 1)),
			np.array((*p2, 1)),
			np.array((*p3, 1))
		]
		self.color = np.array((255, 255, 255))

	def get_normal(self):
		line1 = self.points[1][:3] - self.points[0][:3]
		line2 = self.points[2][:3] - self.points[0][:3]
		normal = np.cross(line1, line2)
		mag = np.linalg.norm(normal)
		if mag != 0:
			normal /= mag
		return normal

	def __matmul__(self, a):
		p1 = self.points[0] @ a
		p2 = self.points[1] @ a
		p3 = self.points[2] @ a
		return Tri(p1[:3], p2[:3], p3[:3])

	def __truediv__(self, a):
		p1 = self.points[0] / a[0]
		p2 = self.points[1] / a[1]
		p3 = self.points[2] / a[2]
		return Tri(p1[:3], p2[:3], p3[:3])

	def __mul__(self, a):
		p1 = self.points[0] * a
		p2 = self.points[1] * a
		p3 = self.points[2] * a
		return Tri(p1[:3], p2[:3], p3[:3])

	def __add__(self, a):
		p1 = self.points[0] + a
		p2 = self.points[1] + a
		p3 = self.points[2] + a
		return Tri(p1[:3], p2[:3], p3[:3])

	def __iter__(self):
		return iter(self.points)

	def __getitem__(self, i):
		return self.points[i]

	def __setitem__(self, i, a):
		self.points[i] = a


if __name__ == '__main__':
	test1 = Tri(np.zeros(3), np.zeros(3), np.zeros(3))
	test2 = Tri(np.zeros(3), np.zeros(3), np.zeros(3))
	test3 = Tri(np.zeros(3), np.zeros(3), np.zeros(3))
	arr = np.array((test1, test2, test3))
	print(arr)
