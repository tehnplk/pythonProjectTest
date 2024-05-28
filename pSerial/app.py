import sys
import time

from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QLineEdit
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice, QByteArray


class SerialApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initSerial()

    def initUI(self):
        self.setWindowTitle('QSerialPort Example')

        self.textEdit = QTextEdit(self)
        self.textEdit.setReadOnly(True)

        self.sendLineEdit = QLineEdit(self)
        self.sendLineEdit.setPlaceholderText("Type data to send")

        self.sendButton = QPushButton('Send', self)
        self.sendButton.clicked.connect(self.sendData)

        layout = QVBoxLayout()
        layout.addWidget(self.textEdit)
        layout.addWidget(self.sendLineEdit)
        layout.addWidget(self.sendButton)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def initSerial(self):
        self.serial = QSerialPort()
        self.serial.setPortName('COM3')  # Change this to your serial port
        self.serial.setBaudRate(QSerialPort.Baud9600)
        self.serial.setDataBits(QSerialPort.Data8)
        self.serial.setParity(QSerialPort.NoParity)
        self.serial.setStopBits(QSerialPort.OneStop)
        self.serial.setFlowControl(QSerialPort.NoFlowControl)

        self.serial.readyRead.connect(self.readData)

        if self.serial.open(QIODevice.ReadWrite):
            self.textEdit.append("Serial port opened successfully.")
        else:
            self.textEdit.append("Failed to open serial port.")

    def sendData(self):
        data = self.sendLineEdit.text()
        if self.serial.isOpen() and data:
            self.serial.write(data.encode('utf-8'))
            self.sendLineEdit.clear()

    def readData(self):
        #if self.serial.canReadLine():
        data = self.serial.readBufferSize()
        text = data.decode('utf-8').strip()
        self.textEdit.append(f"Received: {text}")

    def closeEvent(self, event):
        if self.serial.isOpen():
            self.serial.close()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SerialApp()
    ex.show()
    sys.exit(app.exec_())
