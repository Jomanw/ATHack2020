from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QSlider, QHBoxLayout, QGridLayout, QVBoxLayout

def create_slider(slider_name, min_value, max_value, release_fn):
	grid_layout = QGridLayout()

	slider = QSlider(Qt.Horizontal)
	slider.setMinimum(min_value)
	slider.setMaximum(max_value)

	slider.setTickPosition(QSlider.TicksBelow)
	slider.sliderReleased.connect(release_fn)
	
	low_label = QLabel()
	low_label.setText('LOW {}'.format(slider_name.upper()))
	low_label.setAlignment(Qt.AlignLeft)

	high_label = QLabel('HIGH {}'.format(slider_name.upper()))
	high_label.setAlignment(Qt.AlignRight)

	midpoint = (max_value - min_value) / 2

	# low_label.setStyleSheet('background-color: green;')
	# high_label.setStyleSheet('background-color: cyan;')
	
	grid_layout.addWidget(slider, 0, 0, 1, max_value)
	grid_layout.addWidget(low_label, 1, 0, 1, midpoint)
	grid_layout.addWidget(high_label, 1, min_value + midpoint, 1, midpoint)

	return slider, grid_layout

def create_toggle(sharpen_fn, enhance_fn, trace_fn, video_fn):
	options = ['sharpen', 'enhance', 'trace', 'video']
	toggle_buttons = [QPushButton(option) for option in options]

	box_layout = QHBoxLayout()
	for toggle_button in toggle_buttons:
		box_layout.addWidget(toggle_button)

	toggle_buttons[0].clicked.connect(sharpen_fn)
	toggle_buttons[1].clicked.connect(enhance_fn)
	toggle_buttons[2].clicked.connect(trace_fn)
	toggle_buttons[3].clicked.connect(video_fn)

	return toggle_buttons[0], toggle_buttons[1], toggle_buttons[2], toggle_buttons[3], box_layout

def create_save(save_img_fn, save_video_fn):
	pass

class HoverButton(QPushButton):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.setStyleSheet('color: white;'
						   'background-color: blue;'
						   'border-radius: 200px;')

class CircleButton(QPushButton):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		self.setStyleSheet('color: white;'
						   'background-color: red;'
						   'border-radius: 200px;')










