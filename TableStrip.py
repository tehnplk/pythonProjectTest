from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QVBoxLayout, QWidget
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Striped Rows Example")

        # Create the table view
        self.table = QTableView()

        # Create the data model
        self.model = QStandardItemModel(5, 3)
        self.model.setHorizontalHeaderLabels(["Column 1", "Column 2", "Column 3"])

        # Populate the table with some data
        for row in range(5):
            for col in range(3):
                item = QStandardItem(f"Row {row}, Col {col}")
                self.model.setItem(row, col, item)

        # Set the model for the table view
        self.table.setModel(self.model)

        # Enable alternating row colors
        self.table.setAlternatingRowColors(True)

        # Set the background color for odd and even rows
        self.table.setStyleSheet("""
            QTableView {
                alternate-background-color: lightgray;
                background-color: white;
            }
        """)

        # Create the main layout and add the table view
        layout = QVBoxLayout()
        layout.addWidget(self.table)

        # Create the central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()