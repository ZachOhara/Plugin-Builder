
# ---------------------------------------------------------
# generator.py
# Code for converting YAML configuration into images
# Copyright 2019 Zach Ohara
# ---------------------------------------------------------

from PIL import Image, ImageDraw, ImageFont

import os

from base import displayboxer, knobber, waveformer

# Primary methods

def generate_image(config, render_mode=False):
	image = build_base_image(config)
	supporting_images = []
	draw_signature_text(image, config)
	for obj_name in dir(config.objects):
		obj_config = config.objects.lookup(obj_name)
		obj_class = obj_config.lookup("class") # 'class' is a Python reserved word
		obj_defaults = config.object_defaults.lookup(obj_class)
		obj_position = (obj_config.x_pos, obj_config.y_pos)
		obj_size = None
		if "width" in dir(obj_config) and "height" in dir(obj_config):
			obj_size = (obj_config.width, obj_config.height)
		elif "width" in dir(obj_defaults) and "height" in dir(obj_defaults):
			obj_size = (obj_defaults.width, obj_defaults.height)
		elif "size" in dir(obj_defaults):
			obj_size = (obj_defaults.size, obj_defaults.size)
		else:
			obj_size = (0, 0)

		# Displaybox
		if obj_class.startswith("displaybox"):
			box_image = displayboxer.draw_display_box(obj_defaults, obj_size)
			image = composite_at_position(image, box_image, obj_position)
		if obj_class.startswith("displaytext"):
			pass
			# TODO
		# Knob
		if obj_class.startswith("knob"):
			draw_knob_text(image, obj_config, obj_defaults,
				draw_value=(not render_mode))
			if render_mode:
				sprite_sheet = knobber.build_sprite_sheet(obj_defaults, obj_config.accent_color)
				supporting_images.append((obj_name, sprite_sheet))
			if not render_mode:
				knob_image = knobber.draw_knob(obj_defaults, obj_config.accent_color)
				image = composite_at_position(image, knob_image, obj_position)
		# Waveform_box
		if obj_class.startswith("waveform_box"):
			box_image = displayboxer.draw_display_box(
				config.object_defaults.lookup(obj_defaults.graphic_class), obj_size)
			image = composite_at_position(image, box_image, obj_position)
			if render_mode:
				sprite_sheet = waveformer.build_sprite_sheet(obj_defaults, obj_config.accent_color)
				supporting_images.append((obj_name, sprite_sheet))
			if not render_mode:
				wave_image = waveformer.draw_wave(
					obj_defaults, obj_config.accent_color, obj_defaults.default_value)
				image = composite_at_position(image, wave_image, obj_position)
	if render_mode:
		return image, supporting_images
	else:
		return image

# Internal code

def build_base_image(config):
	return Image.new("RGBA", (config.width, config.height), config.background_color)

def draw_signature_text(image, config):
	text_1 = config.signature.text_1.replace("@version", str(config.version))
	text_2 = config.signature.text_2
	font_size = config.signature.font_size
	if (config.width > config.signature.width_threshold):
		# Put the signature on one line
		v_offset = config.height - config.signature.one_line.v_offset
		h_offset_1 = config.signature.one_line.h_offset
		h_offset_2 = config.width - h_offset_1
		draw_text(image, text_1, font_size, ("left", "bottom"), (h_offset_1, v_offset))
		draw_text(image, text_2, font_size, ("right", "bottom"), (h_offset_2, v_offset))
	else:
		# Put the signature on two lines
		center = config.width / 2
		v_offset_1 = config.height - config.signature.two_lines.v_offset_1
		v_offset_2 = config.height - config.signature.two_lines.v_offset_2
		draw_text(image, text_1, font_size, ("center", "bottom"), (center, v_offset_1))
		draw_text(image, text_2, font_size, ("center", "bottom"), (center, v_offset_2))

def draw_knob_text(image, control_config, default_config, draw_value=True):
	# Draw the label
	label_ypos = control_config.y_pos - (default_config.size / 2) - default_config.label.v_offset
	draw_text(image, control_config.label, default_config.label.font_size,
		("center", "top"), (control_config.x_pos, label_ypos))
	if draw_value and "value" in dir(control_config):
		value_ypos = control_config.y_pos + (default_config.size / 2) + default_config.value.v_offset
		draw_text(image, control_config.value, default_config.value.font_size,
		("center", "top"), (control_config.x_pos, value_ypos))

# Helper methods

def draw_text(image, text, font_size, alignment, position, font_name="Roboto-Regular", font_color="#FFFFFF"):
	draw = ImageDraw.Draw(image)
	font = ImageFont.truetype(font=resolve_font(font_name), size=font_size)
	text_size = font.getsize(text)
	# calculate positions
	x_pos = position[0] # assume left align, then correct if necessary
	if alignment[0] == "right":
		x_pos -= text_size[0]
	elif alignment[0] == "center":
		x_pos -= text_size[0] / 2
	y_pos = position[1] # assume top align, then correct if necessary
	if alignment[1] == "bottom":
		y_pos -= text_size[1]
	elif alignment[1] == "center":
		y_pos -= text_size[1] / 2
	# draw the text
	draw.text((x_pos, y_pos), text, fill=font_color, font=font)

def composite_at_position(image1, image2, center_pos):
	temp_image = Image.new(mode="RGBA", size=image1.size, color=(0, 0, 0, 0))
	position = get_corner_position(center_pos, image2.size)
	temp_image.paste(image2, box=position)
	return Image.alpha_composite(image1, temp_image)

def get_corner_position(centerpos, size):
	return (int(centerpos[0] - (size[0] / 2)), int(centerpos[1] - (size[1] / 2)))

def resolve_font(configured_font):
	return os.path.sep.join((os.getcwd(), "res", configured_font + ".ttf"))
