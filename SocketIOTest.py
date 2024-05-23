import sys
import socketio
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit, QLineEdit


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 Socket.IO Client")
        self.setGeometry(100, 100, 400, 300)

        self.sio = socketio.Client()

        self.initUI()
        self.setupSocketIO()

    def initUI(self):
        layout = QVBoxLayout()

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        layout.addWidget(self.text_edit)

        self.input_line = QLineEdit()
        layout.addWidget(self.input_line)

        self.send_button = QPushButton("Send SC")
        self.send_button.clicked.connect(self.send_sc)
        layout.addWidget(self.send_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def setupSocketIO(self):
        @self.sio.event
        def connect():
            self.text_edit.append("Connected to server")

        @self.sio.event
        def disconnect():
            self.text_edit.append("Disconnected from server")

        @self.sio.event
        def sc(data):
            self.text_edit.append(f"Message from server: {data}")

        try:
            self.sio.connect('http://localhost:3000')
        except:
            pass

    def send_sc(self):
        message = self.input_line.text()
        self.text_edit.append(f"Sending sc: {message}")
        try:
            self.sio.emit('sc', message)
        except:
            pass
        self.input_line.clear()

    def closeEvent(self, event):
        self.sio.disconnect()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
