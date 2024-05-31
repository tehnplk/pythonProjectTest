from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer
from datetime import datetime
import cv2
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.is_start = True
        self.pixmap = None

        #self.cap = cv2.VideoCapture(1)
        self.cap = cv2.VideoCapture(1 + cv2.CAP_DSHOW)
        """self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 600)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))"""
        self.setWindowTitle("Hello")
        self.resize(500, 350)
        self.layout = QVBoxLayout(self)

        self.label = QLabel("Cam")
        self.layout.addWidget(self.label)

        self.btn_stop_start = QPushButton("Stop")
        self.layout.addWidget(self.btn_stop_start)
        self.btn_stop_start.clicked.connect(self.stop_start)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        if self.is_start:
            self.timer.start(1)

    def stop_start(self):
        self.is_start = not self.is_start
        if not self.is_start:
            self.btn_stop_start.setText("Start")
            self.cap.release()
            self.timer.stop()
            timestamp = int(round(datetime.now().timestamp()))
            self.pixmap.save(f"./temp/{timestamp}.png")

        else:
            self.btn_stop_start.setText("Stop")
            self.cap = cv2.VideoCapture(1 + cv2.CAP_DSHOW)
            self.timer.start()

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            self.pixmap = QPixmap.fromImage(img)
            self.label.setPixmap(self.pixmap)


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
