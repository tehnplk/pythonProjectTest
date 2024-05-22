import sys

from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import (QApplication, QTableWidget
, QTableWidgetItem, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QLabel, QDialog, QMenu)
from functools import partial
from customClass import dbclickButton as dbBtn


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 Table with Buttons")

        # Create a QTableWidget
        self.table = QTableWidget(self)
        self.table.setRowCount(3)
        self.table.setColumnCount(4)

        # Add buttons to each row
        for row in range(self.table.rowCount()):
            text = dbBtn.DoubleClickButton(f"ผู้รับบริการรายที่ {row}")
            text.signalDoubleClicked.connect(partial(print, row))
            text.setStyleSheet("border:none")

            widget = QWidget()
            lay = QHBoxLayout()
            lay.addWidget(text)
            lay.addStretch(10)
            b = QPushButton("...")
            lay.addWidget(b)
            widget.setLayout(lay)
            self.table.setCellWidget(row, 0, widget)

            button1 = QPushButton("เรียกคิว")
            button1.setAccessibleName(str(row))
            button1.clicked.connect(partial(self.clicked, row))
            self.table.setCellWidget(row, 2, button1)

            button2 = QPushButton("จบคิว")
            button2.setAccessibleName(str(row))
            button2.clicked.connect(partial(self.btn2_click), row)
            self.table.setCellWidget(row, 3, button2)

        # Create a layout and add the table
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.resize(600, 500)

    def clicked(self, data):
        print(data)

    def btn2_click(self, data):
        b = self.sender()
        p = b.mapToGlobal(QPoint(0, b.height()-5))
        menu = QMenu()
        menu.move(p)
        action1 = menu.addAction("Option 1")
        action2 = menu.addAction("Option 2")
        action3 = menu.addAction("Option 3")
        r = menu.exec_()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
