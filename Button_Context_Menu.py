from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu
from PyQt5.QtCore import QEvent
import sys

def my_excepthook(type, value, tback):
    print(type, value, tback)
    sys.__excepthook__(type, value, tback)

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.createWidgets()

    def createWidgets(self):
        self.my_button = QtWidgets.QPushButton(self)
        self.my_button.setText("My Button")
        self.my_button.installEventFilter(self)

    def eventFilter(self, source, event):
        if event.type() == QEvent.ContextMenu and source is self.my_button:
            menu = QMenu()
            action1 = menu.addAction("Option 1")
            action2 = menu.addAction("Option 2")
            action3 = menu.addAction("Option 3")
            selected_action = menu.exec_(event.globalPos())

            if selected_action == action1:
                print("You have selected the first option")
            elif selected_action == action2:
                print("You have selected the second option")
            elif selected_action == action3:
                print("You have selected the third option")

            return super().eventFilter(source, event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.excepthook = my_excepthook
    sys.exit(app.exec_())
