
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
	image_config = configuration.load_configuration(open(GLOBAL_CONFIG), open(SAMPLE_IMAGE))
	generator.generate_image(image_config).show()

if __name__ == "__main__":
	main()
