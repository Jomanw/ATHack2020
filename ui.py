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
	# low_label.setStyleSheet('background-color: green;')
	low_label.setAlignment(Qt.AlignLeft)

	high_label = QLabel('HIGH {}'.format(slider_name.upper()))
	# high_label.setStyleSheet('background-color: cyan;')
	high_label.setAlignment(Qt.AlignRight)

	midpoint = (max_value - min_value) / 2
	
	grid_layout.addWidget(slider, 0, 0, 1, max_value)
	grid_layout.addWidget(low_label, 1, 0, 1, midpoint)
	grid_layout.addWidget(high_label, 1, min_value + midpoint, 1, midpoint)

	return slider, grid_layout

def create_toggle():
	options = ['sharpen', 'enhance']
	toggle_buttons = [QPushButton(option) for option in options]

	box_layout = QHBoxLayout()
	for toggle_button in toggle_buttons:
		box_layout.addWidget(toggle_button)

	return toggle_buttons[0], toggle_buttons[1], box_layout

class HoverButton(QPushButton):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.setStyleSheet('color: white;'
						   'background-color: blue;'
						   'border-radius: 200px;')


