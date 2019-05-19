
# ---------------------------------------------------------
# textwriter.py
# Generates a C++ boilerplate based on a configuration
# Copyright 2019 Zach Ohara
# ---------------------------------------------------------

# Primary methods

def generate_text(config, images):
	parameters = []
	for param_name in dir(config.parameters):
		parameters.append(ParameterInfo(config, param_name))
	processors = []
	for proc_name in dir(config.processors):
		processors.append(ProcessorInfo(config, proc_name))
	bitmaps = []
	bitmaps.append(BitmapInfo(config, config.name, 101))
	i = 201
	for img_name in images:
		bitmaps.append(BitmapInfo(config, img_name, i, multiframe=True))
		i += 1
	output = ""
	# .rc app configuration
	output += "\n// Paste the following in the .rc app configuration file:\n"
	output += "// ======================================================================\n"
	output += "// Image resource definitions\n"
	output += "".join([b.get_rc_entry() for b in bitmaps])
	# resource.h
	output += "\n\n// Paste the following in resource.h:\n"
	output += "// ======================================================================\n"
	output += "// GUI dimensions\n"
	output += "#define GUI_WIDTH " + str(config.width) + "\n"
	output += "#define GUI_HEIGHT " + str(config.height) + "\n"
	output += "// Unique IDs for each image resource\n"
	output += "".join([b.get_id_definition() for b in bitmaps])
	output += "// Image resource locations for this plug\n"
	output += "".join([b.get_fn_definition() for b in bitmaps])
	output += "// Number of frames in the bitmaps\n"
	output += "".join([b.get_frames_definition() for b in bitmaps])
	# main class header
	output += "\n\n// Paste the following in the main class .h:\n"
	output += "// ======================================================================\n"
	output += "// Processor class includes\n"
	output += "".join([p.include for p in processors])
	output += "\n// Object definitions:\nprivate:\n"
	output += "".join([p.get_obj_definition() for p in processors])
	# main class definition
	output += "\n\n// Paste the following in the main class .cpp:\n"
	output += "// ======================================================================\n"
	output += "const int kNumPrograms = 0;\n\n"
	output += "enum EParams\n{\n"
	output += "".join(["\t" + p.param_id + ",\n" for p in parameters])
	output += "\tkNumParams\n"
	output += "};\n\n"
	output += "std::vector<ParameterInfo> kParameterList =\n{\n"
	output += "".join([p.get_parameter_definition() for p in parameters])
	output += "};\n"
	# constructor
	output += "\n\n// Paste the following in the main class constructor:\n"
	output += "// ======================================================================\n"
	output += "{\n"
	output += "\tSetBackground(" + bitmaps[0].id_handle + ", " + bitmaps[0].fn_handle + ");\n"
	output += "\t\n"
	output += "".join(["\tRegisterBitmap(" + b.id_handle + ", " + b.fn_handle + ", " + b.frame_handle + ");\n" for b in bitmaps[1:]])
	output += "\t\n"
	output += "\tAddParameterList(kParameterList);\n"
	output += "\t\n"
	output += "".join([p.get_registration() + "\t\n" for p in processors])
	output += "\tFinishConstruction();\n"
	output += "}\n"
	# end
	return output


# Internal code

class ParameterInfo:

	def __init__(self, config, param_name):
		param_config = config.parameters.lookup(param_name)
		control_config = config.objects.lookup(param_name)
		self.param_id = get_param_id_str(param_name)
		self.hostname = param_config.hostname
		self.bitmap_id = get_bitmap_id_str(param_name)
		self.x_pos = control_config.x_pos
		self.y_pos = control_config.y_pos
		self.label_config = None
		if "value" in dir(control_config):
			self.label_config = config.object_defaults.lookup(control_config.lookup("class")).label	
		self.template = None
		if "template" in dir(param_config):
			self.template = self.resolve_param_template(param_config.template)

	def resolve_param_template(self, template):
		return "Make" + camelcase(template) + "Param"

	def get_parameter_definition(self):
		s = "\tParameterInfo()\n"
		s += "\t\t.InitParam(\"" + self.hostname + "\", " + self.param_id +	", " + self.bitmap_id + ", " + str(self.x_pos) + ", " + str(self.y_pos) + ")\n"
		if self.label_config != None:
			s += "\t\t.InitLabel()\n"
		if self.template != None:
			s += "\t\t." + self.template + "()\n"
		s = s[:-1] # remove the last newline
		s += ",\n"
		return s

class ProcessorInfo:

	def __init__(self, config, proc_name):
		proc_config = config.processors.lookup(proc_name)
		self.name = "m" + camelcase(proc_name)
		self.type = proc_config.lookup("class").split(".")[-1]
		self.include = self.resolve_include_path(proc_config.lookup("class"), self.type)
		self.params = []
		if "parameters" in dir(proc_config):
			for param_name in dir(proc_config.parameters):
				param_id = get_param_id_str(proc_config.parameters.lookup(param_name))
				type_index = "k" + camelcase(param_name) + "Param"
				self.params.append((param_id, type_index))

	def resolve_include_path(self, classpath, type):
		folder = "/".join(classpath.split(".")[:-1])
		return "#include \"../OZDSP_Core/" + folder + "/" + type + ".h\"\n"

	def get_obj_definition(self):
		return "\t" + self.type + " " + self.name + ";\n"

	def get_registration(self):
		s = "\tRegisterProcessor(&" + self.name + ");\n"
		for p in self.params:
			s += "\t" + self.name + ".RegisterParameter(" + p[0] + ", " + self.type + "::" + p[1] + ");\n"
		return s

class BitmapInfo:

	def __init__(self, config, name, id, multiframe=False):
		self.bitmap_id = id
		self.id_handle = get_bitmap_id_str(name)
		self.filename = "resources/img/" + name + ".png"
		self.fn_handle = name.upper() + "_CONTROL_FN"
		if name == config.name:
			# this is the background image
			self.id_handle = "BACKGROUND_ID"
			self.fn_handle = "BACKGROUND_FN"
		self.is_multiframe = multiframe
		if self.is_multiframe:
			self.num_frames = config.object_defaults.lookup(
				config.objects.lookup(name).lookup("class")).num_sprites
			self.frame_handle = name.upper() + "_CONTROL_FRAMES"

	def get_id_definition(self):
		return "#define " + self.id_handle + " " + str(self.bitmap_id) + "\n"

	def get_fn_definition(self):
		return "#define " + self.fn_handle + " \"" + self.filename + "\"\n"

	def get_frames_definition(self):
		if self.is_multiframe:
			return "#define " + self.frame_handle + " " + str(self.num_frames) + "\n"
		else:
			return ""

	def get_rc_entry(self):
		return self.id_handle + " PNG " + self.fn_handle + "\n"

# Helper methods

def get_bitmap_id_str(bitmap_name):
	return bitmap_name.upper() + "_CONTROL_ID"

def get_param_id_str(param_name):
	return "k" + camelcase(param_name) + "Pid"

def camelcase(s):
	s = "_" + s
	while "_" in s:
		i = s.find("_")
		s = s[:i] + s[i + 1].upper() + s[i + 2:]
	return s
