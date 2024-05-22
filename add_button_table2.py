import sys
from functools import partial

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt5 Table with Buttons")
        self.setGeometry(100, 100, 600, 400)

        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(5)
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(["Column 1", "Column 2", "Actions"])

        for row in range(5):
            self.table_widget.setItem(row, 0, QTableWidgetItem(f"Item {row + 1}, 1"))
            self.table_widget.setItem(row, 1, QTableWidgetItem(f"Item {row + 1}, 2"))

            button = QPushButton("Click Me")
            #button.clicked.connect(lambda ch, r=row: self.on_button_clicked(r))
            button.clicked.connect(partial(self.on_button_clicked, row))
            self.table_widget.setCellWidget(row, 2, button)

        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def on_button_clicked(self, row):
        print(f"Button in row {row + 1} clicked")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
