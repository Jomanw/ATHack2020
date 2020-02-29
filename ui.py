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
	slider.setStyleSheet("background-color:black;");
	
	low_label = QLabel()
	low_label.setText('LOW {}'.format(slider_name.upper()))
	low_label.setAlignment(Qt.AlignLeft)

	high_label = QLabel('HIGH {}'.format(slider_name.upper()))
	high_label.setAlignment(Qt.AlignRight)

	font = QFont("Arial", 14, QFont.Bold)
	low_label.setFont(font)
	high_label.setFont(font)

	midpoint = (max_value - min_value) / 2


	grid_layout.addWidget(slider, 0, 0, 1, max_value)
	grid_layout.addWidget(low_label, 1, 0, 1, midpoint)
	grid_layout.addWidget(high_label, 1, min_value + midpoint, 1, midpoint + 0.5) # 0.5 bc of magic number

	return slider, grid_layout

def create_toggle(sharpen_fn, enhance_fn, trace_fn, pause_fn):
	options = ['sharpen', 'enhance', 'trace', 'pause']
	toggle_buttons = [ToggleButton(option.upper()) for option in options]

	box_layout = QHBoxLayout()
	for toggle_button in toggle_buttons:
		box_layout.addWidget(toggle_button)

	toggle_buttons[0].clicked.connect(sharpen_fn)
	toggle_buttons[1].clicked.connect(enhance_fn)
	toggle_buttons[2].clicked.connect(trace_fn)
	toggle_buttons[3].clicked.connect(pause_fn)

	return toggle_buttons[0], toggle_buttons[1], toggle_buttons[2], toggle_buttons[3], box_layout

def create_save_and_quit(save_img_fn, save_video_fn, quit_fn):
	options = ['capture', 'record', 'quit']
	toggle_buttons = [LegibleButton(option.upper()) if option != 'record' 
					  else RecordButton(option.upper()) 
					  for option in options]

	box_layout = QHBoxLayout()
	for toggle_button in toggle_buttons:
		box_layout.addWidget(toggle_button)

	toggle_buttons[0].clicked.connect(save_img_fn)
	toggle_buttons[1].clicked.connect(save_video_fn)
	toggle_buttons[2].clicked.connect(quit_fn)
	toggle_buttons[2].setStyleSheet('color: white; background-color: red;')

	return toggle_buttons[0], toggle_buttons[1], box_layout

class LegibleButton(QPushButton):
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.setStyleSheet('color: white;'
						   'background-color: black;')
		
		font = QFont("Arial", 20, QFont.Bold) 
		self.setFont(font)

class RecordButton(QPushButton):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.is_recording = False
		self.high_alpha_color = 'background-color: rgba(248, 174, 33, 1.0);'
		self.low_alpha_color = 'background-color: rgba(248, 174, 33, 0.5)'
		self.active_color = self.high_alpha_color

		self.setStyleSheet('color: white;' + self.active_color)
		
		font = QFont("Arial", 20, QFont.Bold) 
		self.setFont(font)
		self.timer = QTimer()
		self.timer.timeout.connect(self.changeColor)

	def mousePressEvent(self, event):
		QPushButton.mousePressEvent(self,event)
		self.is_recording = not self.is_recording
		if self.is_recording:
			self.timer.start(1000)
		else:
			self.timer.stop()

	def changeColor(self):
		if self.active_color == self.high_alpha_color:
			self.active_color = self.low_alpha_color
		else:
			self.active_color = self.high_alpha_color
		self.setStyleSheet(self.active_color)

class ToggleButton(QPushButton):
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.is_selected = False
		self.setStyleSheet('color: black;'
						   'background-color: rgba(150, 150, 150, 1.0);')
		
		font = QFont("Arial", 20, QFont.Bold) 
		self.setFont(font)

	def mousePressEvent(self, event):
		QPushButton.mousePressEvent(self,event)
		self.is_selected = not self.is_selected
		if self.is_selected:
			self.setStyleSheet('color: white;'
							   'background-color: rgba(0, 0, 0, 1.0);')
		else:
			self.setStyleSheet('color: white;'
							   'background-color: rgba(150, 150, 150, 1.0);')







