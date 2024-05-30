from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer
import cv2
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.start = True

        self.cap = cv2.VideoCapture(0)
        self.setWindowTitle("Hello")
        self.resize(500, 350)
        self.layout = QVBoxLayout(self)

        self.label = QLabel("Cam")
        self.layout.addWidget(self.label)

        self.btn_stop_start = QPushButton("Stop Start")
        self.layout.addWidget(self.btn_stop_start)
        self.btn_stop_start.clicked.connect(self.stop_start)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        if self.start:
            self.timer.start(1)

    def stop_start(self):
        if self.start:
            self.cap.release()
            self.timer.stop()
            self.start = False
        else:
            self.cap = cv2.VideoCapture(0)
            self.timer.start()
            self.start = True

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(img)
            self.label.setPixmap(pixmap)


def catch_exceptions(t, val, tb):
    print(None,
          "An exception was raised",
          f"Exception type: {t}")


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.excepthook = catch_exceptions
    sys.exit(app.exec())
