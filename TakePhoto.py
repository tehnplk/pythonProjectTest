import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel
from PyQt5.QtGui import QImage, QPixmap
import cv2
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread


def excepthook(exctype, value, traceback):
    # Handle the exception here
    print(f"Exception Type: {exctype}")
    print(f"Exception Value: {value}")
    print(f"Traceback: {traceback}")


class CameraThread(QThread):
    change_pixmap = pyqtSignal(QImage)

    def __init__(self):
        super(CameraThread, self).__init__()
        self.cap = cv2.VideoCapture(0)

    def run(self):
        while True:
            ret, frame = self.cap.read()
            if ret:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_frame.shape
                img = QImage(rgb_frame.data, w, h, ch * w, QImage.Format_RGB888)
                self.change_pixmap.emit(img)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Webcam Photo Taker")
        self.setGeometry(400, 300, 400, 300)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.button = QPushButton("Take Photo", self)
        self.layout.addWidget(self.button)
        self.button.clicked.connect(self.take_photo)

        self.button3 = QPushButton("Video", self)
        self.layout.addWidget(self.button3)
        self.button3.clicked.connect(self.thread_vdo)

        self.button2 = QPushButton("Clear", self)
        self.button2.clicked.connect(self.clear_photo)
        self.layout.addWidget(self.button2)

        self.label = QLabel("กดปุ่มเพื่อถ่ายรูป")
        self.layout.addWidget(self.label)

        self.video_label = QLabel("วิดิโอ")
        self.layout.addWidget(self.video_label)

        # Create the camera thread and connect the signal
        self.camera_thread = CameraThread()
        self.camera_thread.change_pixmap.connect(self.set_image)
        # self.camera_thread.start()

    def thread_vdo(self):
        self.camera_thread.start()

    def set_image(self, image):
        self.video_label.setPixmap(QPixmap.fromImage(image))

    def clear_photo(self):
        self.label.clear()
        self.label.setText("wait...")

    def take_photo(self):
        self.label.clear()
        ret , frame = cv2.VideoCapture(0).read()
        cv2.imwrite("./temp/temp.jpg", frame)

        pixmap = QPixmap("./temp/temp.jpg")
        self.label.setPixmap(pixmap)

        return 0

        self.label.setText("wait...")
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
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
            self.label.setPixmap(pixmap)
            cap.release()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.excepthook = excepthook
    sys.exit(app.exec_())
