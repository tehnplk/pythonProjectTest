import sys

from PyQt5.QtCore import QPoint, QTimer
from PyQt5.QtWidgets import (QApplication, QTableWidget
, QTableWidgetItem, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QLabel, QDialog, QMenu)
from functools import partial
from customClass import dbclickButton as dbBtn
from PyQt5 import Qt


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 Table with Buttons")

        # Create a QTableWidget
        self.table = QTableWidget(20, 4)
        self.table.setHorizontalHeaderLabels(["Name", "Queue", "", "Action"])
        self.table.cellDoubleClicked.connect(self.cell_db_click)
        self.table.setAlternatingRowColors(True)
        self.table.setColumnWidth(0, 200)
        self.table.setStyleSheet("""
                    QTableWidget {
                        alternate-background-color: skyblue;
                        background-color: white;
                    }
                """)

        # Add buttons to each row
        for row in range(self.table.rowCount()):
            widget = QWidget()
            lay = QHBoxLayout()
            self.table.setRowHeight(row, 60)

            text = QLabel(f"ผู้รับบริการรายที่ {row}")
            lime = "lime"
            text.setStyleSheet(f"border:none;font-size:18px;margin-left:5px")
            text.setAccessibleName(f"HN {row}")
            lay.addWidget(text)

            widget.setLayout(lay)
            widget.setAccessibleName(str(row))
            self.table.setCellWidget(row, 0, text)

            button1 = QPushButton(f"เรียกคิว")
            button1.setAccessibleName(str(row))
            button1.clicked.connect(partial(self.btn1_click, row))
            button1.setFlat(True)
            button1.setStyleSheet("border: 1px solid red;border-radius:5px;")
            self.table.setCellWidget(row, 2, button1)

            button2 = QPushButton("จบคิว")
            button2.setAccessibleName(f"{row}")
            button2.clicked.connect(self.btn2_click)
            button2.setFlat(True)
            button2.setStyleSheet("border: 1px solid yellow;border-radius:5px;")
            self.table.setCellWidget(row, 3, button2)

        # Create a layout and add the table
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.resize(660, 540)

    def btn1_click(self, data):
        btn = self.sender()
        btn.setEnabled(False)
        print(data)
        # Perform time-consuming operation here
        QTimer.singleShot(2000, lambda: btn.setEnabled(True))

    def btn2_click(self, data):
        btn = self.sender()
        hn = btn.accessibleName()
        p = btn.mapToGlobal(QPoint(0, btn.height() - 5))
        menu = QMenu()

        action1 = menu.addAction("กลับบ้าน")
        action2 = menu.addAction("ส่งต่อ : ห้องการเงิน")
        action3 = menu.addAction("ส่งต่อ : แผนกอื่น")
        r = menu.exec(p)
        if r == action1:
            print(f"{hn} กลับบ้าน")

    def cell_db_click(self, row, column):
        if column != 0:
            return False
        item = self.table.cellWidget(row, column)
        print(item.accessibleName())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
