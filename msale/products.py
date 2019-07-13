from PyQt5 import QtWidgets, QtCore, QtGui, uic

from msale.new_item import NewItemForm

class ProductsForm(QtWidgets.QWidget):
    def __init__(self):

        """
        Settings Widget for the MS Point of sale software
        //Initialize dynamically the ui
        //set the icons not loaded dynamically by the UiLoader
        //Setup slot functions for the signals sent by the dynamic Ui
        """
        QtWidgets.QWidget.__init__(self)
        
        self.widget = uic.loadUi("msale/forms/products.ui",self)

        self.widget.viewBtn.setIcon(QtGui.QIcon("msale/icons/database_48px_white.png"))
        self.widget.viewLabel.setIcon(QtGui.QIcon("msale/icons/database_48px_white.png"))
        #self.widget.viewBtn.clicked.connect(self.OpenAddNewItem)

        self.widget.addBtn.setIcon(QtGui.QIcon("msale/icons/add_database_48px_white.png"))
        self.widget.newLabel.setIcon(QtGui.QIcon("msale/icons/add_database_48px_white.png"))
        self.widget.addBtn.clicked.connect(self.OpenAddNewItem)

        self.widget.editBtn.setIcon(QtGui.QIcon("msale/icons/database_import_48px_white.png"))
        self.widget.editLabel.setIcon(QtGui.QIcon("msale/icons/database_import_48px_white.png"))
        #self.widget.editBtn.clicked.connect(self.OpenAddNewItem)

        self.widget.deleteBtn.setIcon(QtGui.QIcon("msale/icons/delete_database_48px_white.png"))
        self.widget.deleteLabel.setIcon(QtGui.QIcon("msale/icons/delete_database_48px_white.png"))
        #self.widget.deleteBtn.clicked.connect(self.OpenAddNewItem)
        #@QtCore.pyqtSlot()
        #def open_searchWindow(self):

    def OpenAddNewItem(self):
        window = NewItemForm()
        window.exec_()
        