import numpy as np
import math


def projection(FOV, ASPECT_RATIO, NEAR, FAR):
	FOV = 1 / math.tan(FOV * 0.5 / 180 * math.pi)
	return np.array((
		(ASPECT_RATIO * FOV, 0  , 0                           , 0),
		(0                 , FOV, 0                           , 0),
		(0                 , 0  , FAR / (FAR * NEAR)          , 1),
		(0                 , 0  , (-FAR * NEAR) / (FAR - NEAR), 0))
	)


def translate(pos):
	return np.array((
		(1     , 0     , 0     , 0),
		(0     , 1     , 0     , 0),
		(0     , 0     , 1     , 0),
		(pos[0], pos[1], pos[2], 1),
	))


def rotate_x(a):
	return np.array((
		(1, 0           , 0          , 0),
		(0, math.cos(a) , math.sin(a), 0),
		(0, -math.sin(a), math.cos(a), 0),
		(0, 0           , 0          , 1)
	))


def rotate_y(a):
	return np.array((
		(math.cos(a), 0, -math.sin(a), 0),
		(0          , 1, 0           , 0),
		(math.sin(a), 0, math.cos(a) , 0),
		(0          , 0, 0           , 1)
	))


def rotate_z(a):
	return np.array((
		(math.cos(a) , math.sin(a), 0, 0),
		(-math.sin(a), math.cos(a), 0, 0),
		(0           , 0          , 1, 0),
		(0           , 0          , 0, 1)
	))


def scale(n):
	return np.array((
		(n, 0, 0, 0),
		(0, n, 0, 0),
		(0, 0, n, 0),
		(0, 0, 0, 1),
	))
