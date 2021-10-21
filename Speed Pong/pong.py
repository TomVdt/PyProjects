import pygame as pg
import random

vec = pg.math.Vector2

screen = pg.display.set_mode((750, 500))
clock = pg.time.Clock()
elapsed = 0

p1_pos = pg.Rect((10, 220), (10, 60))
p1_controls = {pg.K_w: -0.5, pg.K_s: 0.5}
p1_score = 0
p2_pos = pg.Rect((730, 220), (10, 60))
p2_controls = {pg.K_UP: -0.5, pg.K_DOWN: 0.5}
p2_score = 0

ball_pos = pg.Rect((375, 250), (5, 5), center=(375, 250))
ball_vel = vec(random.random() - 0.5, random.random() - 0.5).normalize() / 4

run = True
while run:
	for event in pg.event.get():
		if event.type == pg.QUIT:
			run = False
		if event.type == pg.KEYDOWN:
			if event.key == pg.K_ESCAPE:
				run = False

	pressed = pg.key.get_pressed()
	for p1 in p1_controls:
		if pressed[p1]:
			p1_pos[1] += (p1_controls[p1] * elapsed)
			if p1_pos[1] < 0:
				p1_pos[1] = 0
			if p1_pos[1] + 60 > 500:
				p1_pos[1] = 440
	for p2 in p2_controls:
		if pressed[p2]:
			p2_pos[1] += (p2_controls[p2] * elapsed)
			if p2_pos[1] < 0:
				p2_pos[1] = 0
			if p2_pos[1] + 60 > 500:
				p2_pos[1] = 440

	ball_pos.center += (ball_vel * elapsed)
	if ball_pos.y < 0:
		ball_pos.y = 0
		ball_vel[1] *= -1
	if ball_pos.y + 5 > 500:
		ball_pos.y = 495
		ball_vel[1] *= -1
	if ball_pos.x >= 745:
		p1_score += 1
		ball_pos.center = (375, 250)
		ball_vel = vec(random.random() - 0.5, random.random() - 0.5).normalize() / 4
	if ball_pos.x <= 0:
		p2_score += 1
		ball_pos.center = (375, 250)
		ball_vel = vec(random.random() - 0.5, random.random() - 0.5).normalize() / 4
	if p1_pos.colliderect(ball_pos) and ball_vel[0] < 0:
		ball_vel[0] *= -1.1
		ball_vel[1] = (random.random() - 0.5)
	if p2_pos.colliderect(ball_pos) and ball_vel[0] > 0:
		ball_vel[0] *= -1.1
		ball_vel[1] = (random.random() - 0.5)

	# p1_pos[1] = p2_pos[1] = ball_pos.center[1] - 30

	screen.fill((0, 0, 0))
	pg.draw.rect(screen, (69, 69, 69), p1_pos)
	pg.draw.rect(screen, (69, 69, 69), p2_pos)
	pg.draw.circle(screen, (255, 255, 255), ball_pos.center, 5)
	pg.display.flip()

	elapsed = clock.tick(60)
	pg.display.set_caption(f"Pong {p1_score} - {p2_score}")
