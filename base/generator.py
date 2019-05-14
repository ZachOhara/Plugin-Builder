
# ---------------------------------------------------------
# generator.py
# Code for converting YAML configuration into images
# Copyright 2019 Zach Ohara
# ---------------------------------------------------------

from PIL import Image, ImageDraw, ImageFont
import yaml

import os

# Primary methods

def generate_image(config):
	image = build_base_image(config)
	draw = ImageDraw.ImageDraw(image)
	draw_signature_text(draw, config)
	return image

# Internal code

def build_base_image(config):
	return Image.new("RGB", (config.width, config.height), config.background_color)

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

# Helper methods

def resolve_font(configured_font):
	return os.path.sep.join((os.getcwd(), "res", configured_font + ".ttf"))
