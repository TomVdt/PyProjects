import pygame as pg
import numpy as np
import math
import os
import sys


WIDTH = 500
HEIGHT = 500
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def matrix_rot_z(f_theta):
	return np.array((
		(math.cos(f_theta) , math.sin(f_theta), 0, 0),
		(-math.sin(f_theta), math.cos(f_theta), 0, 0),
		(0                      , 0                     , 1, 0),
		(0                      , 0                     , 0, 1))
	)


def matrix_rot_x(f_theta):
	return np.array((
		(1, 0                           , 0                            , 0),
		(0, math.cos(f_theta * 0.5), -math.sin(f_theta * 0.5), 0),
		(0, math.sin(f_theta * 0.5), math.cos(f_theta * 0.5) , 0),
		(0, 0                           , 0                            , 1))
	)


def matrix_rot_y(f_theta):
	return np.array((
		(math.cos(f_theta * 0.5), 0, -math.sin(f_theta * 0.5), 0),
		(0                           , 1, 0                            , 0),
		(math.sin(f_theta * 0.5), 0, math.cos(f_theta * 0.5) , 0),
		(0                           , 0, 0                            , 1))
	)


def matrix_identity():
	return np.array((
		(1, 0, 0, 0),
		(0, 1, 0, 0),
		(0, 0, 1, 0),
		(0, 0, 0, 1))
	)


def matrix_translate(x, y, z):
	return np.array((
		(1, 0, 0, 0),
		(0, 1, 0, 0),
		(0, 0, 1, 0),
		(x, y, z, 1))
	)


def matrix_projection(f_fov, f_aspect_ratio, f_near, f_far):
	f_fov_rad = 1 / math.tan(f_fov * 0.5 / 180 * math.pi)
	return np.array((
		(f_aspect_ratio * f_fov_rad, 0        , 0                                   , 0),
		(0                         , f_fov_rad, 0                                   , 0),
		(0                         , 0        , f_far / (f_far * f_near)            , 1),
		(0                         , 0        , (-f_far * f_near) / (f_far - f_near), 0))
	)


def matrix_mult_vect(mat, v):
	out = np.zeros(4)
	out[0] = v[0] * mat[0, 0] + v[1] * mat[1, 0] + v[2] * mat[2, 0] + v[3] * mat[3, 0]
	out[1] = v[0] * mat[0, 1] + v[1] * mat[1, 1] + v[2] * mat[2, 1] + v[3] * mat[3, 1]
	out[2] = v[0] * mat[0, 2] + v[1] * mat[1, 2] + v[2] * mat[2, 2] + v[3] * mat[3, 2]
	out[3] = v[0] * mat[0, 3] + v[1] * mat[1, 3] + v[2] * mat[2, 3] + v[3] * mat[3, 3]
	return out


# TODO: what have I fked up?
def matrix_point_at(pos, target, up):
	new_forward = target - pos
	new_forward[3] = 1
	new_forward /= np.linalg.norm(new_forward)

	new_up = new_forward[:3] * np.dot(up[:3], new_forward[:3])
	new_up = up[:3] - new_up
	new_up /= np.linalg.norm(new_up)

	new_right = np.cross(new_up, new_forward[:3])

	return np.array((
		(new_right[0]  , new_right[1]  , new_right[2]  , 0),
		(new_up[0]     , new_up[1]     , new_up[2]     , 0),
		(new_forward[0], new_forward[1], new_forward[2], 0),
		(pos[0]        , pos[1]        , pos[2]        , 1))
	)


# TODO: Check if this thing is working correctly
def matrix_quickinverse(m):
	minv = np.array((
		(m[0, 0], m[1, 0], m[2, 0], 0),
		(m[0, 1], m[1, 1], m[2, 1], 0),
		(m[0, 2], m[1, 2], m[2, 2], 0),
		(0      , 0      , 0      , 1))
	)
	minv[3, 0] = -(m[3][0] * minv[0][0] + m[3][1] * minv[1][0] + m[3][2] * minv[2][0])
	minv[3, 1] = -(m[3][0] * minv[0][1] + m[3][1] * minv[1][1] + m[3][2] * minv[2][1])
	minv[3, 2] = -(m[3][0] * minv[0][2] + m[3][1] * minv[1][2] + m[3][2] * minv[2][2])
	return minv


class Triangle:

	def __init__(self, p1, p2, p3):
		self.p = [
			np.array([p1[0], p1[1], p1[2], 1], dtype=np.float32),
			np.array([p2[0], p2[1], p2[2], 1], dtype=np.float32),
			np.array([p3[0], p3[1], p3[2], 1], dtype=np.float32)
		]
		self.col = np.array((255, 255, 0), dtype=np.float64)

	def __repr__(self):
		string = "Triangle: "
		for p in self.p:
			string += str(p[:3])
		return string


class Mesh:

	def __init__(self, tris):
		self.tris = []
		for tri in tris:
			self.tris.append(Triangle(tri[0], tri[1], tri[2]))


class Camera:

	def __init__(self, x, y, z):
		self.pos = np.array((x, y, z, 1), dtype=np.float64)
		self.look_dir = np.array((0, 0, 1, 1), dtype=np.float64)
		self.yaw = 0
		self.pitch = 0
		self.roll = 0

	@property
	def x(self):
		return self.pos[0]

	@x.setter
	def x(self, a):
		self.pos[0] = a

	@property
	def y(self):
		return self.pos[1]

	@y.setter
	def y(self, a):
		self.pos[1] = a

	@property
	def z(self):
		return self.pos[2]

	@z.setter
	def z(self, a):
		self.pos[2] = a


class Rasterizer:

	def __init__(self, file="cube.obj"):

		self.mesh = self.load_from_file(file)

		self.f_theta = 0

		f_fov = 90.0
		f_aspect_ratio = HEIGHT / WIDTH
		f_near = 0.1
		f_far = 1000.0

		self.mat_proj = matrix_projection(f_fov, f_aspect_ratio, f_near, f_far)
		self.camera = Camera(0, 0, 0)

		pg.init()
		self.screen = pg.display.set_mode((WIDTH, HEIGHT))
		self.clock = pg.time.Clock()

		os.environ['SDL_VIDEO_CENTERED'] = "1"
		pg.display.set_caption("Rasterizer")

		self.f_elapsed = 0
		self.fps = 60
		self.show_tris = False
		self.orthographic = False
		self.keypress = []
		self.mouse_control = False
		self.pause = False
		self.run = True

		self.main()

	def load_from_file(self, f_name):
		with open(f_name, "r") as f:
			verts = []
			mesh = Mesh([])
			for line in f.readlines():
				if line[0] == "v":
					words = line.split(" ")
					x = words[1]
					y = words[2]
					z = words[3]
					verts.append(np.array((x, y, z)))
				if line[0] == "f":
					words = line.split(" ")
					p1 = int(words[1])
					p2 = int(words[2])
					p3 = int(words[3])
					mesh.tris.append(Triangle(verts[p1 - 1], verts[p2 - 1], verts[p3 - 1]))
			f.close()
		return mesh

	def events(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				self.run = False
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					self.run = False
				if event.key == pg.K_LCTRL:
					self.pause = not self.pause
				if event.key == pg.K_o:
					self.orthographic = not self.orthographic
				if event.key == pg.K_z:
					self.show_tris = not self.show_tris
			# 	if event.key in [pg.K_w, pg.K_s, pg.K_a, pg.K_d, pg.K_LSHIFT, pg.K_SPACE]:
			# 		self.keypress.append(event.key)
			# elif event.type == pg.KEYUP:
			# 	if event.key in [pg.K_w, pg.K_s, pg.K_a, pg.K_d, pg.K_LSHIFT, pg.K_SPACE]:
			# 		self.keypress.pop(self.keypress.index(event.key))
			# elif event.type == pg.MOUSEBUTTONDOWN:
			# 	if event.button == pg.BUTTON_LEFT:
			# 		self.mouse_control = not self.mouse_control
			# elif event.type == pg.MOUSEMOTION:
			# 	if self.mouse_control:
			# 		self.camera.yaw += event.rel[0] * 0.1 * self.f_elapsed

		# if pg.K_a in self.keypress:
		# 	self.camera.x -= 0.001 * self.f_elapsed
		# if pg.K_d in self.keypress:
		# 	self.camera.x += 0.001 * self.f_elapsed
		# if pg.K_SPACE in self.keypress:
		# 	self.camera.y -= 0.001 * self.f_elapsed
		# if pg.K_LSHIFT in self.keypress:
		# 	self.camera.y += 0.001 * self.f_elapsed
		# v_forward = self.camera.look_dir * (0.001 * self.f_elapsed)
		# v_forward[3] = 0
		# if pg.K_w in self.keypress:
		# 	self.camera.pos += v_forward
		# if pg.K_s in self.keypress:
		# 	self.camera.pos -= v_forward

	def update(self):
		self.f_theta += 0.001 * self.f_elapsed

	def draw(self):

		self.screen.fill(BLACK)

		mat_rot_z = matrix_rot_z(self.f_theta)
		mat_rot_x = matrix_rot_x(self.f_theta)
		mat_trans = matrix_translate(0, 0, 3)

		mat_world = matrix_identity()
		mat_world = np.matmul(mat_rot_z, mat_rot_x)
		mat_world = np.matmul(mat_world, mat_trans)

		# TODO: REDO
		# v_up = np.array((0, 1, 0, 0), dtype=np.float64)
		# v_target = np.array((0, 1, 0, 1), dtype=np.float64)
		# mat_cam_rot = matrix_rot_y(self.camera.yaw)
		# self.camera.look_dir = matrix_mult_vect(mat_cam_rot, v_target)
		# v_target = self.camera.pos + self.camera.look_dir
		# mat_cam = matrix_point_at(self.camera.pos, v_target, v_up)
		# mat_view = matrix_quickinverse(mat_cam)

		tris_to_raster = []
		for tri in self.mesh.tris:

			# Apply transformations
			tri_transformed = Triangle(np.zeros(3), np.zeros(3), np.zeros(3))
			tri_transformed.p[0] = matrix_mult_vect(mat_world, tri.p[0])
			tri_transformed.p[1] = matrix_mult_vect(mat_world, tri.p[1])
			tri_transformed.p[2] = matrix_mult_vect(mat_world, tri.p[2])

			# Calculate normal
			line1 = tri_transformed.p[1] - tri_transformed.p[0]
			line2 = tri_transformed.p[2] - tri_transformed.p[0]
			normal = np.cross(line1[:3], line2[:3])
			normal /= np.linalg.norm(normal)

			if (normal[0] * (tri_transformed.p[0][0] - self.camera.x) +
				normal[1] * (tri_transformed.p[0][1] - self.camera.y) +
				normal[2] * (tri_transformed.p[0][2] - self.camera.z)) <= 0 or (normal[2] < 0 and self.orthographic):

				light_dir = np.array((0, 0, -1), dtype=np.float64)
				light_dir /= np.linalg.norm(light_dir)

				dp = max(0.1, np.dot(light_dir, normal))
				tri_transformed.col *= dp

				# tri_viewed = tri_transformed
				# tri_viewed.p[0] = matrix_mult_vect(mat_view, tri_transformed.p[0])
				# tri_viewed.p[1] = matrix_mult_vect(mat_view, tri_transformed.p[1])
				# tri_viewed.p[2] = matrix_mult_vect(mat_view, tri_transformed.p[2])

				tri_projected = tri_transformed
				tri_projected.p[0] = matrix_mult_vect(self.mat_proj, tri_transformed.p[0])
				tri_projected.p[1] = matrix_mult_vect(self.mat_proj, tri_transformed.p[1])
				tri_projected.p[2] = matrix_mult_vect(self.mat_proj, tri_transformed.p[2])

				# Apply depth effect
				if not self.orthographic:
					tri_projected.p[0] /= tri_projected.p[0][3]
					tri_projected.p[1] /= tri_projected.p[1][3]
					tri_projected.p[2] /= tri_projected.p[2][3]

				# Move to the middle of screen
				tri_projected.p[0] += (1, 1, 0, 0)
				tri_projected.p[1] += (1, 1, 0, 0)
				tri_projected.p[2] += (1, 1, 0, 0)

				tri_projected.p[0] *= (WIDTH * 0.5, HEIGHT * 0.5, 1, 1)
				tri_projected.p[1] *= (WIDTH * 0.5, HEIGHT * 0.5, 1, 1)
				tri_projected.p[2] *= (WIDTH * 0.5, HEIGHT * 0.5, 1, 1)

				tris_to_raster.append(tri_projected)

		tris_to_raster.sort(key=(lambda t: (t.p[0][2] + t.p[1][2] + t.p[2][2]) / 3), reverse=True)

		for tri in tris_to_raster:
			pg.draw.polygon(self.screen, tri.col, [
				(tri.p[0][0], tri.p[0][1]),
				(tri.p[1][0], tri.p[1][1]),
				(tri.p[2][0], tri.p[2][1])],
				0
			)
			if self.show_tris:
				pg.draw.polygon(self.screen, BLACK, [
					(tri.p[0][0], tri.p[0][1]),
					(tri.p[1][0], tri.p[1][1]),
					(tri.p[2][0], tri.p[2][1])],
					1
				)

		pg.display.flip()

	def main(self):
		while self.run:
			self.events()

			if not self.pause:
				self.update()

			self.draw()

			self.f_elapsed = self.clock.tick(self.fps)
			pg.display.set_caption(f"Rasterizer, fps: {self.clock.get_fps():.0f}, paused: {self.pause}, pos {self.camera.pos[:3]}")


if __name__ == "__main__":
	Rasterizer(file="house.obj")
	pg.quit()
	sys.exit()
