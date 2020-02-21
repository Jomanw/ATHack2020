import sys

from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QVBoxLayout

import cv2
import numpy as np

import processing as p

class MainApp(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        # self.video_size = QSize(320, 240)
        self.initial_x = 100
        self.initial_y = 100
        self.video_size = QSize(640, 480)
        self.setup_ui()
        self.setup_camera()

    def setup_ui(self):
        """Initialize widgets.
        """
        # self.setStyleSheet('background-color: rgb(50, 50, 50);')

        self.image_label = QLabel()
        self.image_label.setGeometry(self.initial_x, self.initial_y, self.initial_x + self.video_size.width(), self.initial_y + self.video_size.height())
        self.image_label.setMinimumSize(640,480)

        self.quit_button = QPushButton("Quit")
        self.quit_button.clicked.connect(self.close)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.image_label)
        self.main_layout.addWidget(self.quit_button)

        self.setLayout(self.main_layout)

    def setup_camera(self):
        """Initialize camera.
        """
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.video_size.width())
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.video_size.height())

        self.timer = QTimer()
        self.timer.timeout.connect(self.display_video_stream)
        self.timer.start(30)

    def display_video_stream(self):
        """Read frame from camera and repaint QLabel widget.
        """
        _, frame = self.capture.read()
        # self.frame = p.no_process_frame(frame)
        # self.frame = p.process_threshold_frame(frame)
        self.frame = p.process_contrast_frame(frame)

        image = QImage(self.frame, self.frame.shape[1], self.frame.shape[0],
                       # frame.strides[0], QImage.Format_RGB888)
                       self.frame.strides[0], QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(image).scaledToWidth(self.video_size.width())
        self.image_label.setGeometry(self.initial_x, self.initial_y, self.initial_x + self.video_size.width(), self.initial_y + self.video_size.height())
        self.image_label.setPixmap(pixmap)

    def resizeEvent(self, event):
        # Resize the video_size based on the current window size
        # Don't set the size here directly, though
        self.video_size = QSize(self.frameGeometry().width() - 40, self.frameGeometry().height() - 96)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainApp()
    win.show()
    sys.exit(app.exec_())
