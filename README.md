# Plugin Builder

This app provides an easy way to design and render interfaces and graphic elements for audio plugins. Every plugin has a layout configuration that is defined in a .yaml file, and the app is able to render that into an image.

## Sample configuration

This is a sample configuration that can be read and digested by the app. Each section of this configuration is broken down below.

```
name: NewConfiguration
version: 1.0
width: 400
height: 300
accent_color: "#F44336" # Material red 500
objects:
  example_control:
    class: knob.px80
    label: Example
    value: "50.0%"
    x_pos: 160
    y_pos: 110
parameters:
  example_control:
    hostname: Example
    template: percentage
processors:
  example_processor:
    class: audio.VolumeProcessor
    parameters:
      loudness: example_control
```

## Heading

The heading of a configuration file contains the following elements

* `name`: The name of the plugin. When rendered, the background image will be called `name`.png and all elements will be output to a folder called `name`.
* `version`: The version of the plugin. This version number will be displayed in the bottom-left corner of the interface as "OZ-DSP v`version`"
* `width` and `height`: The size of the plugin's window, in px
* `accent_color`: The accent color for the plugin. Various elements use this accent color in different ways, but this is a way to define consistency for the entire interface.

## Objects

An object corresponds to some visual element of the interface. Every object must be under its own node. That node can be named whatever is appropriate for the object.

Every object must have a class, which defines what kind of element it is. Different classes have their own properties that must be defined. A full list of object types and thier properties is provided at the bottom of this file.

## Parameters

Every node under the parameters section represents a parameter of the audio plugin. Every parameter must have the same name as a visual element defined in the objects section, since that's how a parameter gets linked to the interface.

Every parameter can have two properties defined: hostname and template. Only the hostname is required; template can be omitted. The hostname is an arbitrary string that is sent to the plugin's host as the parameter's name. The template property relates to a common parameter type and must be a pre-defined value.

## Processors

Every node under the processors section represents a modular processor that is used by the plugin. Processors can have two properties defined: class and parameters. Only the class property is required. The class property relates to a C++ class defined in the core library.

The parameters property is a list of parameters for the processor which can be controlled by elements in the interface. If there are no parameters, then the property can be omitted. Every parameter must have the format `parameter_type: parameter_name` where parameter type corresponds to a type of parameter implemented by the processor, and parameter name is the name of the parameter (as defined under the objects and parameters nodes).

# Index of Objects

### Display boxes

`class: displaybox` - Defines a black box that can be used for any kind of drawing.
* `width`, `height` - The width and height of the box.
* `x_pos`, `y_pos` - The x and y positions of the center of the box.

### Display text

`class: displaytext` - Defines text that can be rendered anywhere in the interface and is not linked to any specific visual element.
* `text` - The text that is displayed
* `font_size` - The size of the text
* `h_align`, `v_align` - The horizontal and vertical alignment. h_align can be left, right, or center, and v_align can be top, bottom, or center. This changes how x_pos and y_pos are used.
* `x_pos`, `y_pos` - The x and y positions of the text, depending on how the alignment is set. For example, if the alignment is set to top left, then these coordinates define the top left corner of the text.

### Knobs

`class: knob.px<size>` - Defines a knob. Every knob must have a defined size, in pixels. For any given size, there must be a corresponding node in the global configuration that defines the proportions of the knob.
* `label` - The text that appears above the knob, describing its function. The font size and vertical spacing of this text are specific to the size of the knob, and are defined in the global configuration.
* `value` - The sample text that appears as a placeholder for the value label. This is only displayed in preview mode, and is not rendered in the final output.
* `x_pos`, `y_pos` - The x and y positions of the center of the knob.

### Waveform boxes

* `class: waveform_box.px<size>` - Defines a selection box that is used to cycle through waveforms. Every box must have a defined size, in pixels. The defined size is the same as the desired width. For any given size, there must be a corresponding node in the global configuration that defines the proportions of the box.
* `x_pos`, `y_pos` - The x and y positions of the center of the box.
