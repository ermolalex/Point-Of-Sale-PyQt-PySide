from PyQt5 import QtWidgets, QtCore, QtGui, uic

from msale.new_item import NewItemForm
from msale.deletedialog import DeleteDialog
from msale.allitemsdialog import AllItemsDialog
from msale.updateitemdialog import ItemUpdateDialog
from msale.icons import resources

class ProductsForm(QtWidgets.QWidget):
    def __init__(self,user):

        """
        Settings Widget for the MS Point of sale software
        //Initialize dynamically the ui
        //set the icons not loaded dynamically by the UiLoader
        //Setup slot functions for the signals sent by the dynamic Ui
        """
        QtWidgets.QWidget.__init__(self)
        self.user = user
        
        self.widget = uic.loadUi("msale/forms/products.ui",self)
        #self.widget.productsTableWidget.setStyleSheet("QHeaderView::section{background-color:rgb(90,90,90);color:white;}")


        self.widget.viewBtn.setIcon(QtGui.QIcon(":/icons/database_48px_white.png"))
        self.widget.viewLabel.setIcon(QtGui.QIcon(":/icons/database_48px_white.png"))
        self.widget.viewBtn.clicked.connect(self.all_items)

        self.widget.addBtn.setIcon(QtGui.QIcon(":/icons/add_database_48px_white.png"))
        self.widget.newLabel.setIcon(QtGui.QIcon(":/icons/add_database_48px_white.png"))
        self.widget.addBtn.clicked.connect(self.OpenAddNewItem)

        self.widget.editBtn.setIcon(QtGui.QIcon(":/icons/database_import_48px_white.png"))
        self.widget.editLabel.setIcon(QtGui.QIcon(":/icons/database_import_48px_white.png"))
        self.widget.editBtn.clicked.connect(self.OpenUpdateItem)

        self.widget.deleteBtn.setIcon(QtGui.QIcon(":/icons/delete_database_48px_white.png"))
        self.widget.deleteLabel.setIcon(QtGui.QIcon(":/icons/delete_database_48px_white.png"))
        self.widget.deleteBtn.clicked.connect(self.delete_items)
        

    def OpenAddNewItem(self):
        window = NewItemForm()
        window.exec_()

    def OpenUpdateItem(self):
        window = ItemUpdateDialog(self.user)
        window.exec_()

    def all_items(self):
        window = AllItemsDialog()
        window.exec_()

    def delete_items(self):
        window = DeleteDialog(self.user)
        window.exec_()
        