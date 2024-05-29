import sys
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel
from PyQt5.QtGui import QImage, QPixmap
import cv2
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread
import time


def excepthook(exctype, value, traceback):
    # Handle the exception here
    print(f"Exception Type: {exctype}")
    print(f"Exception Value: {value}")
    print(f"Traceback: {traceback}")


class CameraThread(QThread):
    change_pixmap = pyqtSignal(QImage)

    def __init__(self):
        super(CameraThread, self).__init__()
        self.running = True
        print("Cap init")

    def run(self):
        print("Cap run")
        cap = cv2.VideoCapture(0)
        self.running = True
        while self.running:
            ret, frame = cap.read()
            if ret:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_frame.shape
                img = QImage(rgb_frame.data, w, h, ch * w, QImage.Format_RGB888)
                self.change_pixmap.emit(img)
                time.sleep(0.001)

    def stop(self):
        self.running = False
        print('Cap stop')


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Webcam Photo Taker")
        self.setGeometry(400, 300, 400, 300)

        self.clip = None

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.btn_start_vdo = QPushButton("Start Video", self)
        self.layout.addWidget(self.btn_start_vdo)
        self.btn_start_vdo.clicked.connect(self.start_thread_vdo)

        self.btn_stop_vdo = QPushButton("Stop Video", self)
        self.layout.addWidget(self.btn_stop_vdo)
        self.btn_stop_vdo.clicked.connect(self.stop_thread_vdo)

        self.btn_photo = QPushButton("Take Photo", self)
        self.layout.addWidget(self.btn_photo)
        self.btn_photo.clicked.connect(self.take_photo)

        self.btn_clear = QPushButton("Clear", self)
        self.layout.addWidget(self.btn_clear)

        self.label_vdo = QLabel("วิดิโอ")
        self.layout.addWidget(self.label_vdo)

        self.label_photo = QLabel("กดปุ่มเพื่อถ่ายรูป")
        self.layout.addWidget(self.label_photo)

        # Create the camera thread and connect the signal
        self.camera_thread = CameraThread()
        self.camera_thread.change_pixmap.connect(self.set_vdo)
        self.camera_thread.start()

    def stop_thread_vdo(self):
        self.camera_thread.stop()

    def start_thread_vdo(self):
        self.camera_thread.start()

    def set_vdo(self, image):
        pixmap = QPixmap.fromImage(image)
        pixmap = pixmap.scaled(380, 280)
        self.clip = pixmap
        self.label_vdo.setPixmap(pixmap)

    def take_photo(self):
        # method 1
        # self.camera_thread.stop()
        img = self.clip.toImage()
        img.save("./temp/a.png", "PNG")
        pixmap = QPixmap("./temp/a.png")
        pixmap = pixmap.scaled(380, 280)
        self.label_photo.setPixmap(pixmap)
        self.camera_thread.stop()
        QTimer.singleShot(500, self.start_thread_vdo)
        return 0

        # method 2
        if not self.cap.isOpened():
            self.cap = cv2.VideoCapture(0)
        ret, frame = self.cap.read()
        cv2.imwrite("./temp/temp.jpg", frame)

        pixmap = QPixmap("./temp/temp.jpg")
        self.label_photo.setPixmap(pixmap)
        # self.cap.release()

        return 0

        # method 3
        ret, frame = self.cap.read()
        if ret:
            """height, width, channel = frame.shape
            bytes_per_line = 3 * width
            image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(image)
            pixmap = pixmap.scaled(320, 240)"""
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            image = QImage(frame.data, w, h, ch * w, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(image)
            self.label_photo.setPixmap(pixmap)
            cap.release()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.excepthook = excepthook
    sys.exit(app.exec_())
