import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

class RedWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set window title
        self.setWindowTitle('Red Window')

        # Set window size
        self.setGeometry(100, 100, 400, 300)

        # Set background color
        self.setStyleSheet("background-color: red;")

        # Create buttons
        close_button = QPushButton('Close')
        close_button.clicked.connect(self.close)

        # Create layout and add buttons
        layout = QVBoxLayout()
        layout.addWidget(close_button)

        # Create central widget and set layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RedWindow()
    window.show()
    sys.exit(app.exec_())