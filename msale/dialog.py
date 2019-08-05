from PyQt5 import QtWidgets, QtCore, QtGui, uic

from msale.icons import resources

class Dialog(QtWidgets.QDialog):
    def __init__(self,title):
        QtWidgets.QDialog.__init__(self)
        self.widget = uic.loadUi("msale/forms/dialog.ui",self)
        self.setWindowTitle(title)
        self.setWindowIcon(QtGui.QIcon(":/icons/icon.png"))
