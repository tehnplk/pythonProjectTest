from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
from main_ui import Ui_MainWindow


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.okButton.setText('ตกลง')
        self.okButton.clicked.connect(lambda b: print('AAAA'))


if __name__ == '__main__':
    app = QApplication([])
    win = Main()
    win.show()
    app.exec()
