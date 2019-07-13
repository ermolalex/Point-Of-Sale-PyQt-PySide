from PyQt5 import QtWidgets, QtCore, QtGui, uic

#Load other Ui's
from msale.search import Ui_Search

class Ui_Sell(QtWidgets.QWidget):
    def __init__(self):

        """
        Sell Widget for the MS Point of sale software
        //Initialize dynamically the ui
        //set the icons not loaded dynamically by the UiLoader
        //Setup slot functions for the signals sent by the dynamic Ui
        """
        QtWidgets.QWidget.__init__(self)
        
        self.widget = uic.loadUi("msale/forms/sell.ui",self)

        self.widget.AddToCartBtn.setIcon(QtGui.QIcon("msale/icons/add_shopping_cart_48px_gray.png"))
        self.widget.SearchBtn.setIcon(QtGui.QIcon("msale/icons/search_database_48px_grey.png"))

    @QtCore.pyqtSlot()
    def open_searchWindow(self):
        search = Ui_Search()
        search.show()