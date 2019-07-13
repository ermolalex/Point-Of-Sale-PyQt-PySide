from PyQt5 import QtWidgets, QtCore, QtGui, uic

class HelpForm(QtWidgets.QWidget):
    def __init__(self):

        """
        Help Window for the MS Point of sale software
        //Initialize dynamically the ui
        //set the icons not loaded dynamically by the UiLoader
        //Setup slot functions for the signals sent by the dynamic Ui
        """
        QtWidgets.QWidget.__init__(self)
        
        self.widget = uic.loadUi("msale/forms/helpform.ui",self)