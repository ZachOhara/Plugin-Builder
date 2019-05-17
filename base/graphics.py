
# ---------------------------------------------------------
# graphics.py
# Graphics common code and helper methods
# Copyright 2019 Zach Ohara
# ---------------------------------------------------------

from PIL import Image

# Mask tools

def blank_mask(size):
	return blank_image(size, mode="L", color=(0))

def apply_color(mask, color):
	base = blank_image(mask.size, prescaled=True)
	color = blank_image(mask.size, color=color, prescaled=True)
	return Image.composite(color, base, mask)

# Image creation

def blank_image(size, mode="RGBA", color=(0, 0, 0, 0), prescaled=False):
	'''Size can be a 2-tuple (w, h) or an int (for square images)'''
	if type(size) == int:
		size = (size, size)
	if not prescaled:
		size = [scale(i) for i in size]
	return Image.new(mode=mode, size=size, color=color)

# Scaling methods

SCALE_FACTOR = 4 # must be >= 1 ; higher for more antialiasing, lower for faster

def scale(n):
	return SCALE_FACTOR * n

def unscale(n):
	return int(n / SCALE_FACTOR)

def downsize_image(image):
	return image.resize((unscale(image.width), unscale(image.height)), resample=Image.BICUBIC)
