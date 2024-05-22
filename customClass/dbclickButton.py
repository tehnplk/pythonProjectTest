from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
import sys


class DoubleClickButton(QPushButton):
    signalDoubleClicked = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.clicked.connect(self.checkDoubleClick)
        self.double_clicked = False

    def checkDoubleClick(self):
        if self.timer.isActive():
            self.double_clicked = True
            self.signalDoubleClicked.emit()
        else:
            self.double_clicked = False
        self.timer.start(300)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.double_clicked:
            self.double_clicked = False
            return
        super().mousePressEvent(event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Double Click Button")

        self.button = DoubleClickButton("Double Click Me!")
        self.button.signalDoubleClicked.connect(self.on_double_click)
        self.setCentralWidget(self.button)

    def on_double_click(self):
        print("Double clicked!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
