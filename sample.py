
# ---------------------------------------------------------
# sample.py
# Test runs and other misc. garbage
# Copyright 2019 Zach Ohara
# ---------------------------------------------------------

GLOBAL_CONFIG = "global_config.yaml"
SAMPLE_IMAGE = "sample_image.yaml"

from base import configuration
from base import generator

def main():
	image_config = load_sample_configuration()
	generator.generate_image(image_config).show()

def load_sample_configuration():
	return configuration.load_configuration(open(GLOBAL_CONFIG), open(SAMPLE_IMAGE))

if __name__ == "__main__":
	main()
