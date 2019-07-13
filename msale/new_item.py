from PyQt5 import QtWidgets, QtCore, QtGui, uic
import os


class NewItemForm(QtWidgets.QDialog):
    def __init__(self):

        """
        New Item Dialog for the MS Point of sale software
        //Initialize dynamically the ui
        //set the icons not loaded dynamically by the UiLoader
        //Setup slot functions for the signals sent by the dynamic Ui
        """
        QtWidgets.QDialog.__init__(self)
        
        self.dialog = uic.loadUi("msale/forms/new_item.ui",self)

        
        #@QtCore.pyqtSlot()
        #def open_searchWindow(self):