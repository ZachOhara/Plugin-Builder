
# ---------------------------------------------------------
# configuration.py
# Code for managing YAML configurations and relationships
# Copyright 2019 Zach Ohara
# ---------------------------------------------------------

import yaml

# Primary methods

def load_configuration(global_config_stream, image_config_stream):
	global_config = Configuration(None, parse_yaml(global_config_stream))
	image_config = Configuration(global_config, parse_yaml(image_config_stream))
	return image_config

# Internal code

class Configuration:

	def __init__(self, parent, data):
		self.parent = parent
		self.raw_data = data
		for key in self.raw_data.keys():
			if type(self.raw_data[key]) is dict:
				self.raw_data[key] = Configuration(self, self.raw_data[key])

	def lookup(self, name):
		return self.__getattr__(name)

	def __getattr__(self, name):
		try:
			return self.raw_data[name]
		except:
			try:
				return self.parent.__getattr__(name)
			except:
				raise AttributeError("Configuration has no attribute '" + name + "'")

	def __dir__(self):
		return self.raw_data.keys()

def parse_yaml(config_stream):
	return yaml.load(config_stream, Loader=yaml.Loader)
