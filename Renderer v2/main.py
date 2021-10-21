import pygame as pg
import os
import sys

from camera import Camera
from object3d import Object3D, Tri
from matrix_tools import *


# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class World:

	def __init__(self):

		# Pygame settings
		self.NAME = 'Rasterizer v2'
		self.WIDTH = 500
		self.HEIGHT = 500

		# Init pygame, set screen surface
		pg.init()
		self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT), pg.RESIZABLE)
		os.environ['SDL_VIDEO_CENTERED'] = '1'
		pg.display.set_caption(f'{self.NAME}')

		# Program vars
		self.camera = Camera((0, 0, -4), 90, self.HEIGHT / self.HEIGHT, 0.1, 10.0)
		self.object = Object3D('models/axis.obj')
		self.theta = 0
		self.orthographic = False

		# Pygame vars
		self.clock = pg.time.Clock()
		self.fps = 200
		self.avg_fps = np.zeros(100)
		self.elapsed = 0
		self.pause = False
		self.run = True

		self.main()

	def project(self):
		world_mat = self.camera.camera_matrix()  # rotate_z(self.theta) @ rotate_x(self.theta) @ translate((0, 0, 4))

		tris_to_raster = []
		for tri in self.object.mesh:
			transformed = tri @ world_mat
			# Same as;
			# transformed = Tri()
			# for i in range(3):
			# 	# Apply transformations
			# 	transformed[i] = tri[i] @ world_mat

			# Calculate normal
			normal = transformed.get_normal()
			camera_ray = transformed[0][:3] - self.camera.pos[:3]

			# if ((normal[0] * (transformed[0][0] - self.camera.forward[0])) +
			# 	(normal[1] * (transformed[0][1] - self.camera.forward[1])) +
			# 	(normal[2] * (transformed[0][2] - self.camera.forward[2]))) <= 0:  # or (normal[2] < 0 and self.orthographic):
			if np.dot(normal, camera_ray) <= 0:

				light_dir = np.array((0., -1., -1.))
				light_dir /= np.linalg.norm(light_dir)
				dp = max(0.1, np.dot(light_dir, normal))
				transformed.color = transformed.color * dp

				# projected = transformed @ self.camera.projection
				# if not self.orthographic:
				# 	for i in range(3):
				# 		projected[i] /= projected[i][3]
				# projected += np.array((1, 1, 0, 0))
				# projected *= np.array((WIDTH * 0.5, HEIGHT * 0.5, 1, 1))
				projected = transformed
				for i in range(3):
					projected[i] = transformed[i] @ self.camera.projection

					# Apply depth effect
					if not self.orthographic:
						projected[i] /= projected[i][3]

					# Scale to view
					projected[i] += np.array((1, 1, 0, 0))
					projected[i] *= np.array((self.WIDTH * 0.5, self.HEIGHT * 0.5, 1, 1))

				tris_to_raster.append(projected)

		tris_to_raster.sort(key=(lambda t: (t[0][2] + t[1][2] + t[2][2]) / 3), reverse=True)
		return tris_to_raster

	def events(self):
		# All event checks go here
		for event in pg.event.get():
			if event.type == pg.QUIT:
				self.run = False
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					self.run = False
				if event.key == pg.K_LCTRL:
					self.pause = not self.pause
				if event.key == pg.K_0:
					self.camera = Camera((0, 0, -4), 90, self.HEIGHT / self.HEIGHT, 0.1, 10.0)
			elif event.type == pg.VIDEORESIZE:
				self.WIDTH, self.HEIGHT = event.size
				# self.camera.reset_projection(90, 1, 0.1, 10.0)

	def update(self):
		# Everything to update out of pause
		self.theta += 0.001 * self.elapsed
		self.camera.controls(self.elapsed)

	def draw(self):
		# Draw everything

		self.screen.fill(BLACK)

		for tri in self.project():
			pg.draw.polygon(self.screen, tri.color, (
				(tri[0][0], tri[0][1]),
				(tri[1][0], tri[1][1]),
				(tri[2][0], tri[2][1])),
				0
			)

		pg.display.flip()

	def main(self):
		while self.run:
			# Get all events
			self.events()

			# Update if running
			if not self.pause:
				self.update()

			pg.mouse.set_visible(self.pause)
			pg.event.set_grab(not self.pause)

			# Always draw
			self.draw()

			# Tick the clock and get the elapsed time, update fps display
			self.elapsed = self.clock.tick(self.fps)
			self.avg_fps = np.append(self.avg_fps, self.clock.get_fps())[1:]
			pg.display.set_caption(f'{self.NAME}, fps: {np.average(self.avg_fps):.0f}, camera: {self.camera.pos.astype(int)}')


if __name__ == '__main__':
	# Start the program
	World()

	# Exit gracefully
	pg.quit()
	sys.exit()
