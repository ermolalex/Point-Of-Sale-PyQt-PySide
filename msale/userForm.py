from PyQt5 import QtCore, QtGui, QtWidgets, uic
import sys, os

class UserForm(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.widget = uic.loadUi("msale/forms/userform.ui",self)

        #self.widget.editUserBtn.setIcon(QtGui.QIcon(x+"\\edit_user_w.png"))
        #self.widget.deleteUserBtn.setIcon(QtGui.QIcon(x+"\\remove_user_w.png"))

    def setFields(self):
        pass
