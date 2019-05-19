
# ---------------------------------------------------------
# render.py
# Render the saved configurations and output usable images
# Copyright 2019 Zach Ohara
# ---------------------------------------------------------

import os, shutil, sys

from base import configuration, generator, textwriter

'''
Usage: py render.py [file1, file2, ...]

Including files is optional. If no files are given, all files in the
configs/ folder will be rendered. ALL config files (besides the global
configuration) must be inside the configs/ folder for the renderer to
accept them.
'''

OUTPUT_FOLDER = "output"

def main():
	print()
	filelist = sys.argv[1:]
	if len(filelist) == 0:
		filelist = os.listdir(configuration.CONFIG_FOLDER_NAME)
	global_config = None
	try:
		global_config = open(configuration.GLOBAL_CONFIG_PATH).read()
	except FileNotFoundError:
		print("The global configuration file could not be opened")
		print("It was expected to be found at " + configuration.GLOBAL_CONFIG_PATH)
		print("Stopping...")
		return
	print("Loading configurations")
	configlist = []
	for file in filelist:
		path = os.path.join(configuration.CONFIG_FOLDER_NAME, file)
		try:
			img_config = open(path).read()
			configlist.append(configuration.load_configuration(global_config, img_config))
			print("\tSuccessfully loaded " + path)
		except FileNotFoundError:
			print("\tError, file could not be found: '" + path + "'")
			print("\tSkipping...")
	print()
	for config in configlist:
		print("Rendering " + config.name)
		output_image, supporting_images = generator.generate_image(config, render_mode=True)
		output_path = os.path.join(OUTPUT_FOLDER, config.name)
		try:
			if config.name in os.listdir(OUTPUT_FOLDER):
				print("\t" + output_path + " already exists, overwriting...")
				shutil.rmtree(output_path)
			os.mkdir(output_path)
			output_image.save(os.path.join(output_path, config.name + ".png"))
			print("\tSuccessfully saved " + config.name + ".png")
			for name, image in supporting_images:
				image.save(os.path.join(output_path, name + ".png"))
				print("\tSuccessfully saved " + os.path.join(config.name, name) + ".png")
		except PermissionError:
			print("\tError: could not access " + output_path)
			print("\tIs it currently open in another program?")
			print("\tSkipping...")
		text = textwriter.generate_text(config, [si[0] for si in supporting_images])
		#print(text)
		file = open(os.path.join(output_path, "copyable.h"), "w")
		file.write(text)
		file.close()
		print("\tSuccessfully wrote copyable.h")
	
if __name__ == "__main__":
	main()
