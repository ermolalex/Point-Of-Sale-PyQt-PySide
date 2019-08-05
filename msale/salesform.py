from PyQt5 import QtWidgets, QtCore, QtGui, uic

from msale.salesdialog import SalesDialog
from msale.dialog import Dialog
from msale.icons import resources

class SalesForm(QtWidgets.QWidget):
    def __init__(self):

        """
        Sales Window for the MS Point of sale software
        //Initialize dynamically the ui
        //set the icons not loaded dynamically by the UiLoader
        """
        QtWidgets.QWidget.__init__(self)
        
        self.widget = uic.loadUi("msale/forms/salesform.ui",self)

        # Setup Icons
        self.widget.todaysSalesBtn.setIcon(QtGui.QIcon(":/icons/today_sales_w.png"))
        self.widget.allSalesBtn.setIcon(QtGui.QIcon(":/icons/t_sales_w.png"))
        self.widget.undoSaleBtn.setIcon(QtGui.QIcon(":/icons/undo_w.png"))
        self.widget.compareSalesBtn.setIcon(QtGui.QIcon(":/icons/compare_w.png"))
        self.widget.btn4.setIcon(QtGui.QIcon(":/icons/compare_w.png"))
        self.widget.btn1.setIcon(QtGui.QIcon(":/icons/today_sales_w.png"))
        self.widget.btn2.setIcon(QtGui.QIcon(":/icons/undo_w.png"))
        self.widget.btn3.setIcon(QtGui.QIcon(":/icons/t_sales_w.png"))

        # Events
        self.widget.todaysSalesBtn.clicked.connect(self.show_todays_sales)
        self.widget.allSalesBtn.clicked.connect(self.show_all_sales)
        self.widget.undoSaleBtn.clicked.connect(self.undo_sale)
        self.widget.compareSalesBtn.clicked.connect(self.compare_sales)

    def undo_sale(self):
        dlg = Dialog("Undo Sale")
        dlg.exec_()

    def show_todays_sales(self):
        dlg = SalesDialog("Todays Sales")
        dlg.todays_sales()
        dlg.exec_()

    def show_all_sales(self):
        dlg = SalesDialog("All Sales")
        dlg.selectionCB()
        dlg.exec_()

    def compare_sales(self):
        dlg = Dialog("Compare Sales")
        dlg.exec_()