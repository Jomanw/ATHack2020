import sys

from PySide2.QtGui import *
from PySide2.QtCore import *

from PySide2.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QVBoxLayout, QSlider, QScrollArea, QFileDialog
from PySide2 import QtWidgets, QtCore, QtGui
import cv2
import numpy as np

import ui
import processing as p
from PIL import Image

class PhotoViewer(QtWidgets.QGraphicsView):
    photoClicked = QtCore.Signal(QtCore.QPoint)

    def __init__(self, parent):
        super(PhotoViewer, self).__init__(parent)
        self._zoom = 0
        self._empty = True
        self._scene = QtWidgets.QGraphicsScene(self)
        self._photo = QtWidgets.QGraphicsPixmapItem()
        self._scene.addItem(self._photo)
        self.setScene(self._scene)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(30, 30, 30)))
        self.setFrameShape(QtWidgets.QFrame.NoFrame)

    def hasPhoto(self):
        return not self._empty

    def fitInView(self, scale=True):
        rect = QtCore.QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.hasPhoto():
                unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                self.scale(factor, factor)
            self._zoom = 0

    def setPhoto(self, pixmap=None):
        self._zoom = 0
        if pixmap and not pixmap.isNull():
            self._empty = False
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
            self._photo.setPixmap(pixmap)
        else:
            self._empty = True
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self._photo.setPixmap(QtGui.QPixmap())
        self.fitInView()

    def setPhotoContinuous(self, pixmap):
        self._empty = False
        self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        self._photo.setPixmap(pixmap)

    def wheelEvent(self, event):
        if self.hasPhoto():
            if event.angleDelta().y() > 0:
                # factor = 1.25
                factor = 1.125
                self._zoom += 1
            else:
                # factor = 0.8
                factor = 0.9
                self._zoom -= 1
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom == 0:
                self.fitInView()
            else:
                self._zoom = 0

    def toggleDragMode(self):
        if self.dragMode() == QtWidgets.QGraphicsView.ScrollHandDrag:
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        elif not self._photo.pixmap().isNull():
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

    def mousePressEvent(self, event):
        if self._photo.isUnderMouse():
            self.photoClicked.emit(self.mapToScene(event.pos()).toPoint())
        super(PhotoViewer, self).mousePressEvent(event)

class MainApp(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.initial_x = 100
        self.initial_y = 100
        self.video_size = QSize(640, 480)
        # self.video_size = QSize(1024.0, 768.0)
        # self.video_size = QSize(1280, 1024)

        self.scale = 1.0
        self.pause = False

        self.setup_ui()
        self.setup_camera()

    def setup_ui(self):
        """Initialize widgets.
        """
        # self.setStyleSheet('background-color: rgb(50, 50, 50);')

        self.image_label = QLabel()
        self.image_label.setGeometry(self.initial_x, self.initial_y, self.initial_x + self.video_size.width(), self.initial_y + self.video_size.height())
        self.image_label.setMinimumSize(640,480)
        # self.image_label.setMinimumSize(1024,768)
        # self.image_label.setMinimumSize(1280, 1024)

        self.scrolling_image_label = QScrollArea()
        self.scrolling_image_label.setBackgroundRole(QPalette.Dark)
        self.scrolling_image_label.setWidget(self.image_label)
        # self.scrolling_image_label.setDragMode(True)
        self.img = cv2.imread('test_imgs/4.jpg')

        # initialize quit button
        # self.quit_button = ui.LegibleButton("Quit")
        # self.quit_button.setMinimumSize(10, 30)
        # self.quit_button.clicked.connect(self.close)

        # # initialize capture button
        # self.capture_button = ui.LegibleButton("Capture")
        # self.capture_button.setMinimumSize(10, 30)
        # self.capture_button.clicked.connect(self.capture_photo)

        _, _, self.quit_and_save_layout = ui.create_save_and_quit(self.capture_photo, self.capture_video, self.close)

        self.photo = PhotoViewer(self)
        self.photo.setMinimumSize(640,480)

        self.contrast_slider, self.contrast_layout = ui.create_slider('contrast', 33, 99, self.change_contrast)
        self.brightness_slider, self.brightness_layout = ui.create_slider('brightness', 1, 100, self.change_brightness)
        self.trace_slider, self.trace_layout = ui.create_slider('trace', 20, 300, self.change_trace_threshold)

        self.sharpen_button, self.enhance_button, self.trace_button, self.pause_button, self.toggle_layout = ui.create_toggle(self.change_sharpen, self.change_enhance, self.change_trace, self.pause_stream)

        self.main_layout = QVBoxLayout()
        # self.main_layout.addWidget(self.scrolling_image_label)
        self.main_layout.addWidget(self.photo)
        # self.main_layout.addWidget(self.image_label)
        # self.main_layout.addWidget(self.quit_button)
        # self.main_layout.addWidget(self.capture_button)
        self.main_layout.addLayout(self.quit_and_save_layout)
        self.main_layout.addLayout(self.contrast_layout)
        self.main_layout.addLayout(self.brightness_layout)
        self.main_layout.addLayout(self.trace_layout)
        self.main_layout.addLayout(self.toggle_layout)

        self.setLayout(self.main_layout)

    def setup_camera(self):
        """Initialize camera.
        """
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.video_size.width())
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.video_size.height())

        self.contrast = 1.0
        self.brightness = 1.0
        self.trace_threshold = 20.0
        self.sharpen = False
        self.enhance = False
        self.trace = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.display_video_stream)
        self.timer.start(30)
        # self.timer.timeout.connect(self.display_image_stream)
        # self.timer.start(1000)

    def display_image_stream(self):
        # self.beta = (self.beta + 10) % 100
        self.frame = p.process_contrast_frame(self.img, self.contrast, self.brightness, enhance=self.enhance, sharpen=self.sharpen, trace=self.trace)

        image = QImage(self.frame, self.frame.shape[1], self.frame.shape[0],
                       # self.frame.strides[0], self.QImage.Format_RGB888)
                       self.frame.strides[0], QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(image).scaledToWidth(self.video_size.width())
        self.scrolling_image_label.setGeometry(self.initial_x, self.initial_y, self.initial_x + self.video_size.width(), self.initial_y + self.video_size.height())
        self.scrolling_image_label.setPixmap(pixmap)
        self.photo.setPhoto(pixmap)

    def display_video_stream(self):
        """Read frame from camera and repaint QLabel widget.
        """
        if self.pause == False:
            _, self.raw_img = self.capture.read()
        
        self.frame = p.process_contrast_frame(self.raw_img, self.contrast, self.brightness, self.trace_threshold, enhance=self.enhance, sharpen=self.sharpen, trace=self.trace)
        
        image = QImage(self.frame, self.frame.shape[1], self.frame.shape[0],
                       # self.frame.strides[0], self.QImage.Format_RGB888)
                       self.frame.strides[0], QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(image).scaledToWidth(self.video_size.width())
        # self.image_label.setGeometry(self.initial_x, self.initial_y, self.initial_x + self.video_size.width(), self.initial_y + self.video_size.height())
        # self.image_label.setPixmap(pixmap)
        # self.photo._photo.setPixmap(pixmap)
        self.photo.setPhotoContinuous(pixmap)


    def resizeEvent(self, event):
        # Resize the video_size based on the current window size
        # Don't set the size here directly, though
        self.video_size = QSize(self.frameGeometry().width() - 40, self.frameGeometry().height() - 96)

    def capture_photo(self):
        im = Image.fromarray(self.frame)
        fname = QFileDialog.getSaveFileName(self, 'Save File As', "Captures/untitled.png", "Images (*.png *.jpg)")
        im.save(fname[0])

    def capture_video(self):
        pass

    def pause_stream(self):
        self.pause = not self.pause

    def change_contrast(self):
        self.contrast = self.contrast_slider.value()
        self.contrast = self.contrast / 33.0 # keep range in 1.0-3.0

    def change_brightness(self):
        self.brightness = self.brightness_slider.value()

    def change_trace_threshold(self):
        self.trace_threshold = self.trace_slider.value()

    def change_sharpen(self):
        self.sharpen = not self.sharpen

    def change_enhance(self):
        self.enhance = not self.enhance

    def change_trace(self):
        self.trace = not self.trace


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(QPixmap('proclear_logo.png')))
    win = MainApp()
    win.setWindowTitle('ProClear')
    win.show()
    sys.exit(app.exec_())
