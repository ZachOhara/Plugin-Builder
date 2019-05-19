
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
		obj_class = obj_config.lookup("class") # 'class' is a Python reserved work
		obj_defaults = config.object_defaults.lookup(obj_class)
		obj_position = (obj_config.x_pos, obj_config.y_pos)
		# Displaybox
		if obj_class.startswith("displaybox"):
			box_image = displayboxer.draw_display_box(obj_defaults,
				(obj_config.width, obj_config.height))
			image = composite_at_position(image, box_image, obj_position)
		# Knob
		if obj_class.startswith("knob"):
			draw_knob_text(image, obj_config, obj_defaults.label,
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
				config.object_defaults.lookup(obj_defaults.graphic_class),
				(obj_defaults.width, obj_defaults.height))
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
	draw = ImageDraw.Draw(image)
	font = ImageFont.truetype(
		font=resolve_font(config.font), size=config.signature.font_size)
	text_1 = config.signature.text_1.replace("@version", str(config.version))
	text_2 = config.signature.text_2
	textsize_1 = font.getsize(text_1)
	textsize_2 = font.getsize(text_2)
	textpos_1 = None
	textpos_2 = None
	if config.width >= config.signature.width_threshold:
		arr_config = config.signature.one_line # shorthand
		textpos_1 = (arr_config.h_offset,
			config.height - arr_config.v_offset - textsize_1[1])
		textpos_2 = (config.width - arr_config.h_offset - textsize_2[0],
			config.height - arr_config.v_offset - textsize_2[1])
	else:
		arr_config = config.signature.two_lines # shorthand
		textpos_1 = ((config.width / 2) - (textsize_1[0] / 2),
			config.height - arr_config.v_offset_1 - textsize_1[1])
		textpos_2 = ((config.width / 2) - (textsize_2[0] / 2),
			config.height - arr_config.v_offset_2 - textsize_2[1])
	draw.text(textpos_1, text_1, fill=config.font_color, font=font)
	draw.text(textpos_2, text_2, fill=config.font_color, font=font)
	return image # this is optional, because it's the same object

def draw_knob_text(image, control_config, label_config, draw_value=True):
	draw = ImageDraw.Draw(image)
	font = ImageFont.truetype(font=resolve_font(label_config.font), size=label_config.font_size)
	label_text = control_config.label
	label_size = font.getsize(label_text)
	h_center = control_config.x_pos + (label_config.size / 2)
	x_pos = h_center - (label_size[0] / 2)
	y_pos = control_config.y_pos - label_config.v_offset
	draw.text((x_pos, y_pos), label_text, fill=label_config.font_color, font=font)
	if draw_value and "value" in dir(control_config):
		value_config = label_config.value
		value_font = ImageFont.truetype(
			font=resolve_font(value_config.font), size=value_config.font_size)
		value_text = control_config.value
		value_size = value_font.getsize(value_text)
		value_xpos = h_center - (value_size[0] / 2)
		value_ypos = control_config.y_pos + value_config.size + value_config.v_offset	
		draw.text((value_xpos, value_ypos), value_text, fill=value_config.font_color, font=value_font)

# Helper methods

def composite_at_position(image1, image2, position):
	temp_image = Image.new(mode="RGBA", size=image1.size, color=(0, 0, 0, 0))
	temp_image.paste(image2, box=position)
	return Image.alpha_composite(image1, temp_image)

def resolve_font(configured_font):
	return os.path.sep.join((os.getcwd(), "res", configured_font + ".ttf"))
