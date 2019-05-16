
# ---------------------------------------------------------
# waveformer.py
# Code for drawing waveform selection boxes
# Copyright 2019 Zach Ohara
# ---------------------------------------------------------

from PIL import Image, ImageDraw

import math

SCALE_FACTOR = 4 # must be >= 1 ; higher for more antialiasing, lower for faster

# Primary methods

def draw_waveform_box(box_config):
	image = blank_image(box_config)
	draw = ImageDraw.Draw(image)
	draw.rectangle((0, 0, scaled(box_config.width), scaled(box_config.height)),
		fill=box_config.body_color)
	round_corners(image, scaled(box_config.corner_radius))
	image = image.resize((box_config.width, box_config.height), resample=Image.BICUBIC)
	return image

def build_sprite_sheet(box_config, accent_color):
	pass

def draw_wave(box_config, accent_color, wavetype):
	image = blank_image(box_config)
	draw = ImageDraw.Draw(image)
	line_width = box_config.width - (2 * box_config.h_inset)
	line_height = box_config.height - (2 * box_config.v_inset)
	line_thickness = scaled(box_config.line_thickness)
	points = get_wave_points(wavetype, line_width)
	coords = []
	for p in points:
		x = box_config.h_inset + (p[0] * line_width)
		y = box_config.v_inset + (p[1] * line_height)
		coords.append((scaled(x), scaled(y)))
	draw.line(coords, fill=accent_color, width=line_thickness)
	radius = line_thickness / 2
	for c in coords:
		x0 = c[0] - radius
		y0 = c[1] - radius
		x1 = c[0] + radius
		y1 = c[1] + radius
		draw.ellipse((x0, y0, x1, y1), fill=accent_color)
	image = image.resize((box_config.width, box_config.height), resample=Image.BICUBIC)
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

# Internal code

def round_corners(image, radius):
	for x in range(radius):
		y = radius - round(radius * math.cos(math.asin(1 - (x / radius))))
		for i in range(y + 1):
			image.putpixel((x, i), (0, 0, 0, 0))
			image.putpixel((x, image.height - i - 1), (0, 0, 0, 0))
			image.putpixel((image.width - x - 1, i), (0, 0, 0, 0))
			image.putpixel((image.width - x - 1, image.height - i - 1), (0, 0, 0, 0))

# Helper methods

def blank_image(box_config):
	return Image.new("RGBA", (scaled(box_config.width), scaled(box_config.height)), color=(0, 0, 0, 0))

def scaled(n):
	return SCALE_FACTOR * n
