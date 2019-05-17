
# ---------------------------------------------------------
# displayboxer.py
# Code for drawing pretty-looking rectangles
# Copyright 2019 Zach Ohara
# ---------------------------------------------------------

from PIL import Image, ImageDraw

import math

SCALE_FACTOR = 4 # must be >= 1 ; higher for more antialiasing, lower for faster

# Primary methods

def draw_display_box(default_config, box_config):
	image = blank_image(box_config)
	draw = ImageDraw.Draw(image)
	draw.rectangle((0, 0, scaled(box_config.width), scaled(box_config.height)),
		fill=default_config.body_color)
	round_corners(image, scaled(default_config.corner_radius))
	image = image.resize((box_config.width, box_config.height), resample=Image.BICUBIC)
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

# Helper methods

def blank_image(box_config):
	return Image.new("RGBA", (scaled(box_config.width), scaled(box_config.height)), color=(0, 0, 0, 0))

def scaled(n):
	return SCALE_FACTOR * n
