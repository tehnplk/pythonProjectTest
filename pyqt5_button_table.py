import sys
from PyQt5.QtCore import QPoint, QTimer, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QTableWidget
, QTableWidgetItem, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QLabel, QDialog, QMenu,
                             QAbstractItemView)
from functools import partial
from customClass import dbclickButton as dbBtn
from PyQt5 import Qt
import socketio

import requests
from datetime import datetime


def my_excepthook(type, value, tback):
    print(type, value, tback)
    with open('authen_plus_log_err.txt', 'a+') as f:
        f.write(f"{str(datetime.now())}, {str(type)} {str(value)} {str(tback)}\r\n")
    sys.__excepthook__(type, value, tback)


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 Table with Buttons")
        self.sio = socketio.Client()
        self.queue_signal_server = "http://192.168.199.34:3000"
        self.q_prefix = "A"
        # Create a QTableWidget
        self.table = QTableWidget(20, 5)
        self.table.setHorizontalHeaderLabels(["Name", "Queue", "Appoint", "Call", "Action"])
        self.table.cellDoubleClicked.connect(self.cell_db_click)
        self.table.horizontalHeader().sectionClicked.connect(self.header_click)
        self.table.setAlternatingRowColors(True)
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(3, 80)
        self.table.setColumnWidth(4, 80)
        self.table.setStyleSheet("""
                    QTableWidget {
                        alternate-background-color: None;
                        background-color: white;
                    }
                """)

        self.table.setStyleSheet("QTableWidget::item:selected { background-color: rgb(204, 232, 255); }")

        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.populate_data()

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(layout)
        self.resize(800, 540)

        self.setupSocketIO()

    def populate_data(self):
        for row in range(self.table.rowCount()):
            widget = QWidget()
            lay = QHBoxLayout()
            self.table.setRowHeight(row, 60)

            text = QLabel(f"ผู้รับบริการรายที่ {row}")
            lime = "lime"
            text.setStyleSheet(f"border:none;font-size:18px;margin-left:15px")
            text.setAccessibleName(f"HN {row}")
            lay.addWidget(text)
            # lay.setContentsMargins(100,100,100,100)

            widget.setLayout(lay)
            widget.setAccessibleName(str(row))
            self.table.setCellWidget(row, 0, text)

            button1 = QPushButton(self)
            button1.setAccessibleName(str(row))
            button1.clicked.connect(partial(self.btn1_click, row))
            button1.setFlat(True)
            button1.setStyleSheet("border: 1px solid red;border-radius:5px;font-size:18px")
            button1.setIcon(QIcon('icon/sound.png'))
            button1.setIconSize(QSize(32, 32))
            self.table.setCellWidget(row, 3, button1)

            button2 = QPushButton(self)
            button2.setAccessibleName(f"{row}")
            button2.clicked.connect(self.btn2_click)
            button2.setFlat(True)
            button2.setStyleSheet("border: 1px solid orange;border-radius:5px;font-size:18px")
            button2.setIcon(QIcon('icon/walking.png'))
            button2.setIconSize(QSize(48, 42))
            self.table.setCellWidget(row, 4, button2)

    def btn1_click(self, q):
        btn = self.sender()
        btn.setEnabled(False)
        q = str(q)
        n = len(q)
        q = f"000{q}"
        q = q[n:]
        q = f"{self.q_prefix}{q}"
        QTimer.singleShot(2000, lambda: btn.setEnabled(True))
        try:
            r = requests.get(f"{self.queue_signal_server}/sc1/{q}")
            print('signal resp', r.json())
        except Exception as e:
            print("err", e)

    def btn2_click(self, data):
        btn = self.sender()
        hn = btn.accessibleName()
        # row = self.table.currentRow()
        # self.table.selectRow(row)

        p = btn.mapToGlobal(QPoint(0, btn.height() - 5))
        menu = QMenu()
        menu.setStyleSheet("font-size:18px")

        action1 = menu.addAction("กลับบ้าน")
        menu.addSeparator()
        action2 = menu.addAction("ส่งต่อ : ห้องการเงิน")
        menu.addSeparator()
        action3 = menu.addAction("ส่งต่อ : แผนกอื่น")
        r = menu.exec(p)
        if r == action1:
            print(f"{hn} กลับบ้าน")

    def cell_db_click(self, row, column):
        if column != 0:
            return False
        item = self.table.cellWidget(row, column)
        print(item.accessibleName())

    def header_click(self, index):
        print(index)

    def setupSocketIO(self):

        @self.sio.event
        def connect():
            print("Connected to server")

        @self.sio.event
        def disconnect():
            print("Disconnected from server")

        @self.sio.event
        def message(data):
            print(f"Message from server: {data}")

        try:
            self.sio.connect('http://localhost:3000')
        except:
            pass

    def send_message(self):
        message = self.input_line.text()
        self.text_edit.append(f"Sending message: {message}")
        self.sio.emit('message', message)
        self.input_line.clear()

    def closeEvent(self, event):
        self.sio.disconnect()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.excepthook = my_excepthook
    sys.exit(app.exec_())
