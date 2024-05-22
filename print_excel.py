from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QPushButton, QWidget
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
import win32api
import win32print
import os, sys
from datetime import datetime


def my_excepthook(type, value, tback):
    print(type, value, tback)
    with open('authen_plus_log_err.txt', 'a+') as f:
        f.write(f"{str(datetime.now())}, {str(type)} {str(value)} {str(tback)}\r\n")
    sys.__excepthook__(type, value, tback)


class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.resize(300,500)
        wid = QWidget(self)
        wid.resize(200,200)
        wid.setStyleSheet("background-color:lime;margin:15px")
        btn = QPushButton("print", wid)
        btn.resize(200,100)
        btn.clicked.connect(self.print_excel_file)

    def print_excel_file(self):
        # Open file dialog to select Excel file
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Excel files (*.xlsx *.xls)")
        if file_dialog.exec_():
            selected_file = file_dialog.selectedFiles()[0]

            # Create QPrinter object
            printer = QPrinter(QPrinter.HighResolution)

            # Create print dialog
            print_dialog = QPrintDialog(printer)
            if print_dialog.exec_():
                # Get default printer name
                default_printer = win32print.GetDefaultPrinter()

                # Print Excel file using win32api
                win32api.ShellExecute(
                    0,
                    "print",
                    selected_file,
                    f'/d:"{default_printer}"',
                    os.path.dirname(selected_file),
                    0
                )
                print(f"Printed {selected_file} to {default_printer}")
            else:
                print("Print canceled")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    m = Main()
    m.show()
    sys.excepthook = my_excepthook
    sys.exit(app.exec_())
