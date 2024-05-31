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
        self.pixmap1 = None
        self.pixmap2 = None

        self.cap1 = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
        # self.cap1.set(cv2.CAP_PROP_FPS, 30)
        # self.cap1.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

        self.cap2 = cv2.VideoCapture(1 + cv2.CAP_DSHOW)
        # self.cap2.set(cv2.CAP_PROP_FPS, 30)
        # self.cap2.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

        self.setWindowTitle("Hello")
        self.resize(500, 350)
        self.layout = QVBoxLayout(self)

        self.lb_cam1 = QLabel("Cam1")
        self.layout.addWidget(self.lb_cam1)

        self.lb_cam2 = QLabel("Cam2")
        self.layout.addWidget(self.lb_cam2)

        self.btn_stop_start = QPushButton("Stop")
        self.layout.addWidget(self.btn_stop_start)
        self.btn_stop_start.clicked.connect(self.stop_start)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        if self.is_start:
            self.timer.start()

    def stop_start(self):
        self.is_start = not self.is_start
        if not self.is_start:
            self.btn_stop_start.setText("Start")
            self.cap1.release()
            self.timer.stop()
            timestamp = int(round(datetime.now().timestamp()))
            self.pixmap1.save(f"./temp/{timestamp}.png")

        else:
            self.btn_stop_start.setText("Stop")
            self.cap1 = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
            self.timer.start()

    def update_frame(self):
        ret, frame = self.cap1.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            self.pixmap1 = QPixmap.fromImage(img)
            self.lb_cam1.setPixmap(self.pixmap1)

        ret, frame = self.cap2.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            self.pixmap2 = QPixmap.fromImage(img)
            self.lb_cam2.setPixmap(self.pixmap2)


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
