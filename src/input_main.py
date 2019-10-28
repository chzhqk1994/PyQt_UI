from PyQt5 import QtWidgets, uic
import sys

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__() # call the inherited classes __init__ method
        uic.loadUi('main.ui', self)
        self.show()


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
app.exec_()