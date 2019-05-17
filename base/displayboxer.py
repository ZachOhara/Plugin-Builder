
# ---------------------------------------------------------
# displayboxer.py
# Code for drawing pretty-looking rectangles
# Copyright 2019 Zach Ohara
# ---------------------------------------------------------

from PIL import Image, ImageDraw

import math

from base import graphics

# Primary methods

def draw_display_box(default_config, size):
	image = graphics.blank_image(size)
	draw = ImageDraw.Draw(image)
	draw.rectangle((0, 0, graphics.scale(size[0]), graphics.scale(size[1])),
		fill=default_config.body_color)
	round_corners(image, graphics.scale(default_config.corner_radius))
	image = graphics.downsize_image(image)
	return image

# Internal code

def round_corners(image, radius):
	for x in range(radius):
		y = radius - round(radius * math.cos(math.asin(1 - (x / radius))))
		for i in range(y + 1):
			image.putpixel((x, i), (0, 0, 0, 0))
			image.putpixel((x, image.height - i - 1), (0, 0, 0, 0))
			image.putpixel((image.width - x - 1, i), (0, 0, 0, 0))
			image.putpixel((image.width - x - 1, image.height - i - 1), (0, 0, 0, 0))
