
# ---------------------------------------------------------
# waveformer.py
# Code for drawing waveform icons
# Copyright 2019 Zach Ohara
# ---------------------------------------------------------

from PIL import Image, ImageDraw

import math

from base import graphics

# Primary methods

WAVE_TYPES = ("sine", "triangle", "square", "sawtooth")

def build_sprite_sheet(box_config, accent_color):
	sheet = graphics.blank_image((box_config.width, box_config.height * len(WAVE_TYPES)), prescaled=True)
	for i in range(len(WAVE_TYPES)):
		wave_image = draw_wave(box_config, accent_color, WAVE_TYPES[i])
		sheet.paste(wave_image, box=(0, i * box_config.height))
	return sheet

def draw_wave(box_config, accent_color, wavetype):
	image = graphics.blank_image((box_config.width, box_config.height))
	draw = ImageDraw.Draw(image)
	# Calcaulte dims
	line_width = box_config.width - (2 * box_config.h_inset)
	line_height = box_config.height - (2 * box_config.v_inset)
	line_thickness = graphics.scale(box_config.line_thickness)
	# Draw the line
	points = get_wave_points(wavetype, line_width)
	coords = []
	for p in points:
		x = box_config.h_inset + (p[0] * line_width)
		y = box_config.v_inset + (p[1] * line_height)
		coords.append((graphics.scale(x), graphics.scale(y)))
	draw.line(coords, fill=accent_color, width=line_thickness)
	# Draw circles at all the line intersections so they look better
	radius = line_thickness / 2
	for c in coords:
		x0 = c[0] - radius
		y0 = c[1] - radius
		x1 = c[0] + radius
		y1 = c[1] + radius
		draw.ellipse((x0, y0, x1, y1), fill=accent_color)
	# Downsize and return
	image = graphics.downsize_image(image)
	return image

def get_wave_points(wavetype, width):
	if wavetype == "sine":
		return [(x / width, 0.5 - (0.5 * math.sin(2 * math.pi * (x / width)))) for x in range(width + 1)]
	if wavetype == "triangle":
		return ((0, 0.5), (0.25, 0), (0.75, 1), (1, 0.5))
	if wavetype == "square":
		return ((0, 0.25), (0, 0), (0.5, 0), (0.5, 1), (1, 1), (1, 0.75))
	if wavetype == "sawtooth":
		return ((0, 0.5), (0.5, 0), (0.5, 1), (1, 0.5))
	raise ValueError("'" + wavetype + "' is not a wave type")
