
# ---------------------------------------------------------
# generator.py
# Code for converting YAML configuration into images
# Copyright 2019 Zach Ohara
# ---------------------------------------------------------

from PIL import Image, ImageDraw, ImageFont
import yaml

import os

from base import knobber

# Primary methods

PREVIEW_MODE = "preview_mode"
RENDER_MODE = "render_mode"

def generate_image(config, mode=PREVIEW_MODE):
	image = build_base_image(config)
	draw = ImageDraw.Draw(image)
	draw_signature_text(draw, config)
	for control_name in dir(config.controls):
		control_config = config.controls.lookup(control_name)
		default_config = control_config.defaults.lookup(
			control_config.type).lookup(control_config.variant)
		darw_control_text(draw, control_config, default_config.label)
	del draw
	for control_name in dir(config.controls):
		control_config = config.controls.lookup(control_name)
		default_config = control_config.defaults.lookup(
			control_config.type).lookup(control_config.variant)
		if mode == PREVIEW_MODE:
			if control_config.type == "knob":
				knob_image = knobber.draw_knob(default_config, config.accent_color)
				comp_image = Image.new(mode="RGBA", size=image.size, color=(0, 0, 0, 0))
				comp_image.paste(knob_image, box=(control_config.x_pos, control_config.y_pos))
				image = Image.alpha_composite(image, comp_image)
	return image

# Internal code

def build_base_image(config):
	return Image.new("RGBA", (config.width, config.height), config.background_color)

def draw_signature_text(draw, config):
	font = ImageFont.truetype(font=resolve_font(config.font), size=config.signature.font_size)
	left_text = config.signature.left_text.replace("@version", str(config.version))
	right_text = config.signature.right_text
	left_textsize = font.getsize(left_text)
	right_textsize = font.getsize(right_text)
	left_textpos = (config.signature.h_offset,
		config.height - config.signature.v_offset - left_textsize[1])
	right_textpos = (config.width - config.signature.h_offset - right_textsize[0],
		config.height - config.signature.v_offset - right_textsize[1])
	draw.text(left_textpos, left_text, fill=config.font_color, font=font)
	draw.text(right_textpos, right_text, fill=config.font_color, font=font)

def darw_control_text(draw, control_config, label_config):
	font = ImageFont.truetype(font=resolve_font(label_config.font), size=label_config.font_size)
	label_text = control_config.label
	label_size = font.getsize(label_text)
	h_center = control_config.x_pos + (label_config.size / 2)
	x_pos = h_center - (label_size[0] / 2)
	y_pos = control_config.y_pos - label_config.v_offset - label_size[1]
	draw.text((x_pos, y_pos), label_text, fill=label_config.font_color, font=font)
	if "value" in dir(control_config):
		value_config = label_config.value
		value_font = ImageFont.truetype(font=resolve_font(value_config.font), size=value_config.font_size)
		value_text = control_config.value
		value_size = value_font.getsize(value_text)
		value_xpos = h_center - (value_size[0] / 2)
		value_ypos = control_config.y_pos + value_config.size + value_config.v_offset	
		draw.text((value_xpos, value_ypos), value_text, fill=value_config.font_color, font=value_font)

# Helper methods

def resolve_font(configured_font):
	return os.path.sep.join((os.getcwd(), "res", configured_font + ".ttf"))
