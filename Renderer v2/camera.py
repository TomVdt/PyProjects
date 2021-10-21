import pygame as pg
import numpy as np
from matrix_tools import *

class Camera:

	def __init__(self, POS, FOV, ASPECT_RATIO, NEAR, FAR):
		self.FOV = FOV
		self.NEAR = NEAR
		self.FAR = FAR

		self.projection = projection(FOV, ASPECT_RATIO, NEAR, FAR)

		self.pos = np.array((*POS, 1.))
		self.yaw = 0
		self.pitch = 0

		self.forward = np.array((0, 0, 1, 1))
		self.up = np.array((0, 1, 0, 1))
		self.right = np.array((1, 0, 0, 1))

		self.move_speed = 0.01
		self.rot_speed = 0.001

	def reset_projection(self, FOV, ASPECT_RATIO, NEAR, FAR):
		self.projection = projection(FOV, ASPECT_RATIO, NEAR, FAR)

	def controls(self, elapsed):
		pressed = pg.key.get_pressed()
		if pressed[pg.K_a]:
			self.pos -= self.right * self.move_speed * elapsed
		if pressed[pg.K_d]:
			self.pos += self.right * self.move_speed * elapsed
		if pressed[pg.K_w]:
			self.pos += self.forward * self.move_speed * elapsed
		if pressed[pg.K_s]:
			self.pos -= self.forward * self.move_speed * elapsed
		if pressed[pg.K_SPACE]:
			self.pos[1] -= self.move_speed * elapsed
		if pressed[pg.K_LSHIFT]:
			self.pos[1] += self.move_speed * elapsed

		# Rotate camera with keyboard
		if pressed[pg.K_LEFT]:
			self.camera_yaw(-self.rot_speed * elapsed)
		if pressed[pg.K_RIGHT]:
			self.camera_yaw(self.rot_speed * elapsed)
		if pressed[pg.K_UP]:
			self.camera_pitch(self.rot_speed * elapsed)
		if pressed[pg.K_DOWN]:
			self.camera_pitch(-self.rot_speed * elapsed)
		# Rotate camera with mouse
		rel = pg.mouse.get_rel()
		if rel[0] <= 0:
			self.yaw -= self.rot_speed * elapsed
		if rel[0] >= 0:
			self.yaw += self.rot_speed * elapsed
		if rel[1] <= 0:
			self.pitch -= self.rot_speed * elapsed
		if rel[1] >= 0:
			self.pitch += self.rot_speed * elapsed
		if rel != [0, 0]:
			self.camera_rotate()
		self.pos[3] = 1

	def camera_rotate_true(self):
		rotate = rotate_y(self.yaw) @ rotate_x(self.pitch)
		self.forward = np.array((0, 0, 1, 1)) @ rotate
		self.up = np.array((0, 1, 0, 1)) @ rotate
		self.right = np.array((1, 0, 0, 1)) @ rotate

	def camera_rotate(self):
		rotate = rotate_y(self.yaw) @ self.voodoo_magic(self.right, self.pitch)
		self.forward = np.array((0, 0, 1, 1)) @ rotate
		self.up = np.array((0, 1, 0, 1)) @ rotate
		self.right = np.array((1, 0, 0, 1)) @ rotate

	def voodoo_magic(self, axis, a):
		x, y, z = axis[:3]
		c = np.cos(a)
		s = np.sin(a)
		C = 1 - c
		return np.array((
			(x * x * C + c      , x * y * C - (z * s), x * z * C + (y * s), 0),
			(y * x * C + (z * s), y * y * C + c      , y * z * C - (x * s), 0),
			(z * x * C - (y * z), z * y * C + (x * s), z * z * C + c      , 0),
			(0                  , 0                  , 0                  , 1))
		)

	# def camera_yaw(self, angle):
	# 	rotate = rotate_y(angle)
	# 	self.forward = self.forward @ rotate
	# 	self.right = self.right @ rotate
	# 	self.up = self.up @ rotate

	# def camera_yaw(self, angle):
	# 	rotate = rotate_y(angle)
	# 	self.forward = np.array((1, 0, 0, 1)) @ rotate
	# 	self.right = np.array((0, 0, 1, 1)) @ rotate
	# 	self.up = np.array((0, 1, 0, 1)) @ rotate

	# def camera_pitch(self, angle):
	# 	rotate = rotate_x(angle)
	# 	self.forward = self.forward @ rotate
	# 	self.right = self.right @ rotate
	# 	self.up = self.up @ rotate

	# def camera_pitch(self, angle):
	# 	rotate = rotate_z(angle)
	# 	self.forward = np.array((1, 0, 0, 1)) @ rotate
	# 	self.right = np.array((0, 0, 1, 1)) @ rotate
	# 	self.up = np.array((0, 1, 0, 1)) @ rotate

	def translate_matrix(self):
		x, y, z, w = self.pos
		return np.array((
			(1 , 0 , 0 , 0),
			(0 , 1 , 0 , 1),
			(0 , 0 , 1 , 0),
			(-x, -y, -z, 1)
		))

	def rotate_matrix(self):
		fx, fy, fz, w = self.forward
		ux, uy, uz, w = self.up
		rx, ry, rz, w = self.right
		return np.array([
			[rx, ux, fx, 0],
			[ry, uy, fy, 0],
			[rz, uz, fz, 0],
			[0 , 0 , 0 , 1]
		])

	def camera_matrix(self):
		return self.translate_matrix() @ self.rotate_matrix()
