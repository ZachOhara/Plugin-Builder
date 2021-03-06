
# ---------------------------------------------------------
# knobber.py
# Code for drawing knobs and generating sprite sheets
# Copyright 2019 Zach Ohara
# ---------------------------------------------------------

from PIL import Image, ImageDraw

from base import graphics

# Primary methods

def draw_knob(knob_config, accent_color):
	return create_sheet(knob_config, accent_color, [knob_config.default_value])

def build_sprite_sheet(knob_config, accent_color):
	return create_sheet(knob_config, accent_color, build_rotation_list(knob_config))

# Internal code

def create_sheet(config, accent_color, rotations):
	# Setup
	sheet = graphics.blank_image((config.size, config.size * len(rotations)), prescaled=True)
	ring_bounds = calculate_ring_mask_bounds(config)
	shade_color = (0, 0, 0, int(255 * config.ring_shade_opacity))
	# Draw some shapes
	body_mask = create_body_mask(config)
	body_image = graphics.apply_color(body_mask, config.body_color)
	tick_mask = create_tick_mask(config, body_mask)
	tick_image = graphics.apply_color(tick_mask, accent_color)
	ring_mask = create_ring_mask(config, ring_bounds)
	ring_image = graphics.apply_color(ring_mask, accent_color)
	# Now draw the individual sprites
	for i in range(len(rotations)):
		# Rotate the tick to this rotation (negative, since rotate() goes CCW)
		tick_rotated = tick_image.rotate(-rotations[i])
		# Start the sprite composite process
		sprite = Image.alpha_composite(body_image, tick_rotated)
		# Shade the ring and composite it in
		shade_mask = create_shade_mask(config, ring_bounds, rotations[i], ring_mask)
		shade_image = graphics.apply_color(shade_mask, shade_color)
		ring_shaded = Image.alpha_composite(ring_image, shade_image)
		sprite = Image.alpha_composite(sprite, ring_shaded)
		# Scale down to the output size
		sprite = graphics.downsize_image(sprite)
		# Paste onto the sheet
		sheet.paste(sprite, box=(0, i * config.size))
	return sheet

# Shape-drawing methods

def create_body_mask(config):
	mask = graphics.blank_mask(config.size)
	draw = ImageDraw.Draw(mask)
	cen = graphics.scale(center(config))
	radius = graphics.scale(body_radius(config))
	top = cen - radius
	bottom = cen + radius
	draw.ellipse((top, top, bottom, bottom), fill=(255))
	return mask

def create_tick_mask(config, body_mask):
	mask = graphics.blank_mask(config.size)
	draw = ImageDraw.Draw(mask)
	# Calculate rectangular bounds
	left_edge = graphics.scale(center(config) - (config.tick.width / 2))
	right_edge = graphics.scale(center(config) + (config.tick.width / 2))
	top_edge = graphics.scale(center(config) - body_radius(config))
	bottom_edge = top_edge + graphics.scale(config.tick.height)
	# Draw the tick rectangle
	draw.rectangle([left_edge, top_edge, right_edge, bottom_edge], fill=(255))
	# Now round off the top using the body mask
	for x in range(mask.width):
		for y in range(mask.height):
			if mask.getpixel((x, y)) == (255) and body_mask.getpixel((x, y)) == 0:
				mask.putpixel((x, y), (0))
	# Return
	return mask

def create_ring_mask(config, ring_bounds):
	mask = graphics.blank_mask(config.size)
	draw = ImageDraw.Draw(mask)
	# Extract the bounds we need
	inner_bounds, outer_bounds = ring_bounds[0:2]
	# Convert the angles from 12 o'clock to 3 o'clock
	start_angle = -(config.rotation_range / 2) - 90
	end_angle = (config.rotation_range / 2) - 90
	# Draw the outer shape of the ring, then carve out the inside
	draw.pieslice(outer_bounds, start_angle, end_angle, fill=(255))
	draw.ellipse(inner_bounds, fill=(0))
	# Return
	return mask

def create_shade_mask(config, ring_bounds, degrees, ring_mask):
	mask = graphics.blank_mask(config.size)
	draw = ImageDraw.Draw(mask)
	# Extract the bounds we need
	buffered_bounds = ring_bounds[2]
	# Convert the angles from 12 o'clock to 3 o'clock
	start_angle = degrees - 90
	end_angle = (config.rotation_range / 2) - 90
	# Draw the shaded portion
	draw.pieslice(buffered_bounds, start_angle, end_angle, fill=(255))
	# Carve out the middle by compositing with the ring mask, then return
	return Image.composite(mask, graphics.blank_mask(config.size), ring_mask)

def calculate_ring_mask_bounds(config):
	# Cache important values
	inner_radius = graphics.scale(body_radius(config) + config.ring.padding)
	outer_radius = inner_radius + graphics.scale(config.ring.thickness)
	cen = graphics.scale(center(config))
	shade_buffer = graphics.scale(1) # to prevent visual artifacts, 1 is enough
	# Run the math
	top_inn_bound = cen - inner_radius
	bot_inn_bound = cen + inner_radius
	top_out_bound = cen - outer_radius
	bot_out_bound = cen + outer_radius
	top_buf_bound = top_out_bound - shade_buffer
	bot_buf_bound = bot_out_bound + shade_buffer
	# Combine into 4-tubles and return
	inner_bounds = (top_inn_bound, top_inn_bound, bot_inn_bound, bot_inn_bound)
	outer_bounds = (top_out_bound, top_out_bound, bot_out_bound, bot_out_bound)
	buffered_bounds = (top_buf_bound, top_buf_bound, bot_buf_bound, bot_buf_bound)
	return inner_bounds, outer_bounds, buffered_bounds

# Math helper methods

def center(config):
	return config.size / 2

def body_radius(config):
	return (config.size / 2) - config.ring.padding - config.ring.thickness

def build_rotation_list(config):
	step = config.rotation_range / (config.num_sprites - 1)
	limit = config.rotation_range /2
	current_rotation = -limit
	rotations = []
	for i in range(config.num_sprites):
		rotations.append(current_rotation)
		current_rotation += step
	return rotations
