from PyQt5 import QtCore, QtGui, QtWidgets, uic
from msale import version
from msale.icons import resources

class InfoForm(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.widget = uic.loadUi("msale/forms/infoform.ui",self)

        self.widget.myBtn.setIcon(QtGui.QIcon(":/icons/lalan-ke.png"))
        self.setWindowIcon(QtGui.QIcon(":/icons/icon.png"))

        self.widget.versionLabel.setText(version.__version__)