import pyglet as pg
from pyglet.window import key
from pyglet import shapes
from random import random
import numpy as np


WIDTH = 500
HEIGHT = 500
PADDLE_SPEED = 300
P1_CONTROLS = {
	"up": key.W,
	"down": key.S,
}
P2_CONTROLS = {
	"up": key.UP,
	"down": key.DOWN,
}

window = pg.window.Window(WIDTH, HEIGHT)
keys = key.KeyStateHandler()
window.push_handlers(keys)
batch = pg.graphics.Batch()


class Paddle(shapes.Rectangle):

	def __init__(self, x, y, width, height, color, controls):
		super().__init__(x, y, width, height, color=color, batch=batch)
		self.controls = controls

	def get_middle():
		return (self.x + self.width/2, self.y + self.height/2)

	def move(self, dy):
		self.y += dy


class Ball(shapes.Circle):
	def __init__(self, x, y, radius, color):
		super().__init__(x, y, radius, color=color, batch=batch)
		self.dx = 0
		self.dy = 0

	def bounce(self):
		self.dx *= -1.05
		self.dy *= (1 + random()*0.05)

	def collide_borders(self):
		if self.y + self.radius < 0:
			self.y = self.radius
			self.dy *= -1
		elif self.y - self.radius > HEIGHT:
			self.y = HEIGHT - self.radius
			self.dy *= -1

	def collide_paddles(self):
		...

	def update(self, dt, paddles):
		self.collide_borders()
		self.collide_paddles(paddles)
		self.x += self.dx * dt
		self.y += self.dy * dt

	def set_vel(self, dx, dy):
		self.dx = dx
		self.dy = dy


def update(dt):
	# Controls
	if keys[player1.controls["up"]]:
		player1.move(PADDLE_SPEED * dt)
	if keys[player1.controls["down"]]:
		player1.move(-PADDLE_SPEED * dt)
	if keys[player2.controls["up"]]:
		player2.move(PADDLE_SPEED * dt)
	if keys[player2.controls["down"]]:
		player2.move(-PADDLE_SPEED * dt)

	ball.update(dt, [player1, player2])

pg.clock.schedule_interval(update, 1/60.0)

@window.event
def on_draw():
	window.clear()
	batch.draw()

player1 = Paddle(10, 60, 10, 50, (255, 255, 255), P1_CONTROLS)
player2 = Paddle(WIDTH - 20, 60, 10, 50, (255, 255, 0), P2_CONTROLS)
ball = Ball(WIDTH // 2, HEIGHT // 2, 5, (255, 255, 255))
ball.set_vel(-100, 300)

pg.app.run()