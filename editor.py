# ---------------------------------------------------------
# editor.py
# A live WYSIWYG editor for audio plugin interfaces
# Copyright 2019 Zach Ohara
# ---------------------------------------------------------

from PIL import ImageTk
import tkinter as tk

from base import configuration
from base import generator

DUMMYTEXT = "Blank\ntext\nconfiguration\nline\nline\nline\nline\nline\nline\nline\nline\nline\nline\nline\nline\nline\nline\nline\nline\nline\nline\nhelper\nline\nline\nline\nline\nline\nline\nline\nline\nline\nline\nline\nline\nline\nline\nline\nline\nline\nline\nline\nline\nline\nline\nline"

CONFIG_TEMPLATE = "config_template.yaml"

def main():
	root = tk.Tk()
	app = DisplayWindow(root)
	root.mainloop()

def generate_image(image_config_stream):
	global_config_stream = open(configuration.GLOBAL_CONFIG_PATH)
	config = configuration.load_configuration(global_config_stream, image_config_stream)
	image = generator.generate_image(config, mode=generator.PREVIEW_MODE)
	return image

class DisplayWindow:
	def __init__(self, master):
		master.bind("<Button-1>", self.update_image)
		self.config_win = ConfigurationWindow(master)
		self.config_win.set_text(open(CONFIG_TEMPLATE).read())
		#self.img_canvas = tk.Canvas(master, width=600, height=400)
		#self.img_canvas.pack()
		self.img_label = tk.Label(master)
		self.update_image(None)
		self.img_label.pack()

	def update_image(self, event):
		image = generate_image(self.config_win.get_text())
		tk_image = ImageTk.PhotoImage(image)
		#self.img_canvas.create_image(10, 10, image=tk_image)
		self.img_label.configure(image=tk_image)
		self.img_label.image = tk_image

class ConfigurationWindow:
	def __init__(self, master):
		self.window = tk.Toplevel(master)
		self.window.protocol("WM_DELETE_WINDOW", master.destroy)
		self.window.resizable(False, True)
		self.scrollbar = tk.Scrollbar(self.window)
		self.textbox = tk.Text(self.window, height=30, width=70)
		# Init scrollbar
		self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
		self.scrollbar.config(command=self.textbox.yview)
		# Init textbox
		self.textbox.pack(side=tk.LEFT, fill=tk.Y)
		self.textbox.config(yscrollcommand=self.scrollbar.set)
		
	def set_text(self, text):
		self.textbox.delete("1.0", "end")
		self.textbox.insert("1.0", text)

	def get_text(self):
		return self.textbox.get("1.0", "end")

if __name__ == "__main__":
	main()
