from PyQt5 import QtWidgets, QtCore, QtGui, uic

class Ui_Home(QtWidgets.QWidget):
    def __init__(self):

        """
        Home Window for the MS Point of sale software
        //Initialize dynamically the ui
        //set the icons not loaded dynamically by the UiLoader
        //Setup slot functions for the signals sent by the dynamic Ui
        """
        QtWidgets.QWidget.__init__(self)
        
        self.widget = uic.loadUi("msale/forms/home.ui",self)

        self.widget.backupDbBtn.setIcon(QtGui.QIcon("msale/icons/database_backup_48px_white.png"))
        self.widget.switchUserBtn.setIcon(QtGui.QIcon("msale/icons/change_user_white.png"))
        self.widget.logoutBtn.setIcon(QtGui.QIcon("msale/icons/logout_white.png"))