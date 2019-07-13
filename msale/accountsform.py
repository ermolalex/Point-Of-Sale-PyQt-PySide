from PyQt5 import QtCore, QtGui, QtWidgets, uic
import sys, os

from msale.userForm import UserForm

class AccountsForm(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.widget = uic.loadUi("msale/forms/accountsform.ui",self)

        self.grid = QtWidgets.QGridLayout()
        self.load_accounts()
        self.widget.userAccountsScrollArea.setLayout(self.grid)

    def load_accounts(self):
        for i in range(1):
            for j in range (2):
                tile = UserForm()
                self.grid.addWidget(tile,i,j)