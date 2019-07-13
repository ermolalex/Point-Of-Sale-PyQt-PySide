from PyQt5 import QtWidgets, QtCore, QtGui, uic
import os

# Load the dynamic uis
from msale.sell import Ui_Sell
from msale.home import Ui_Home
from msale.helpform import HelpForm
from msale.products import ProductsForm
from msale.settings import SettingsForm
from msale.accountsform import AccountsForm

class MyUi(QtWidgets.QMainWindow):
    def __init__(self):

        """
        MainWindow for the MS Point of sale software
        //Initialize dynamically the ui
        //set the icons not loaded dynamically by the UiLoader
        //Setup slot functions for the signals sent by the dynamic Ui
        """
        QtWidgets.QMainWindow.__init__(self)
        self.setWindowFlags(QtCore.Qt.Window|QtCore.Qt.CustomizeWindowHint)

        self.widget = uic.loadUi("msale/forms/main.ui",self)

        self.widget.HomeBtn.setIcon(QtGui.QIcon("msale/icons/home_48px_grey.png"))
        self.widget.StockMenu.setIcon(QtGui.QIcon("msale/icons/move_by_trolley_52px_grey.png"))
        self.widget.SalesMenu.setIcon(QtGui.QIcon("msale/icons/sales_60px_grey.png"))
        self.widget.SellMenu.setIcon(QtGui.QIcon("msale/icons/icons8_sell_52px.png"))
        self.widget.ProductsMenu.setIcon(QtGui.QIcon("msale/icons/product_60px_grey.png"))
        self.widget.AccountsMenu.setIcon(QtGui.QIcon("msale/icons/user_menu_64px_grey.png"))
        self.widget.HelpMenu.setIcon(QtGui.QIcon("msale/icons/help_64px_grey.png"))
        self.widget.SettingsMenu.setIcon(QtGui.QIcon("msale/icons/settings_100px_grey.png"))
        self.widget.MenuToggle.setIcon(QtGui.QIcon("msale/icons/menu_48px_white.png"))
        self.widget.UserPicture.setIcon(QtGui.QIcon("msale/icons/user_male_circle_100px_pink.png"))
        self.widget.CloseBtn.setIcon(QtGui.QIcon("msale/icons/close_x_48px_white.png"))
        self.widget.MinimizeBtn.setIcon(QtGui.QIcon("msale/icons/minimize_48px_white.png"))
        self.widget.LOGOLABEL.setIcon(QtGui.QIcon("msale/icons/icon3.png"))

        #Initialize the home window
        self.active_win = Ui_Home()
        self.widget.bodylayout.addWidget(self.active_win)
        self.OpenDashboard()

        self.showMaximized()
    
    def uncheck_all(self):
        self.widget.HomeBtn.setChecked(False)
        self.widget.StockMenu.setChecked(False)
        self.widget.SalesMenu.setChecked(False)
        self.widget.SellMenu.setChecked(False)
        self.widget.ProductsMenu.setChecked(False)
        self.widget.AccountsMenu.setChecked(False)
        self.widget.HelpMenu.setChecked(False)
        self.widget.SettingsMenu.setChecked(False)

    @QtCore.pyqtSlot()
    def OpenDashboard(self):
        self.widget.TitleWindow.setText("Home Window")
        self.uncheck_all()
        self.widget.HomeBtn.setChecked(True)

        self.active_win.close()
        self.active_win = Ui_Home()
        self.widget.bodylayout.addWidget(self.active_win)

    @QtCore.pyqtSlot()
    def OpenProducts(self):
        self.widget.TitleWindow.setText("Products Window")
        self.uncheck_all()
        self.widget.ProductsMenu.setChecked(True)

        self.active_win.close()
        self.active_win = ProductsForm()
        self.widget.bodylayout.addWidget(self.active_win)

    @QtCore.pyqtSlot()
    def OpenStock(self):
        self.widget.TitleWindow.setText("Stock Window")
        self.uncheck_all()
        self.widget.StockMenu.setChecked(True)

        self.active_win.close()

    @QtCore.pyqtSlot()
    def OpenSales(self):
        self.widget.TitleWindow.setText("Sales Window")

        self.uncheck_all()
        self.widget.SalesMenu.setChecked(True)
        self.active_win.close()


    @QtCore.pyqtSlot()
    def OpenSell(self):
        #Set Window Title, clear the layout widget and add a new widget
        self.widget.TitleWindow.setText("Sell Window")
        self.uncheck_all()
        self.widget.SellMenu.setChecked(True)

        self.active_win.close()
        self.active_win = Ui_Sell()
        self.widget.bodylayout.addWidget(self.active_win)

    @QtCore.pyqtSlot()
    def OpenAccounts(self):
        self.widget.TitleWindow.setText("Accounts Window")
        self.uncheck_all()
        self.widget.AccountsMenu.setChecked(True)

        self.active_win.close()
        self.active_win = AccountsForm()
        self.widget.bodylayout.addWidget(self.active_win)

    @QtCore.pyqtSlot()
    def OpenHelp(self):
        self.widget.TitleWindow.setText("Help Window")
        self.uncheck_all()
        self.widget.HelpMenu.setChecked(True)

        self.active_win.close()
        self.active_win = HelpForm()
        self.widget.bodylayout.addWidget(self.active_win)

    @QtCore.pyqtSlot()
    def OpenSettings(self):
        self.widget.TitleWindow.setText("Settings Window")
        self.uncheck_all()
        self.widget.SettingsMenu.setChecked(True)

        self.active_win.close()
        self.active_win = SettingsForm()
        self.widget.bodylayout.addWidget(self.active_win)

    @QtCore.pyqtSlot()
    def ToggleMenu(self):
        if self.widget.LeftMenu.isHidden() == True:
            self.widget.LeftMenu.show()

        else:
            self.widget.LeftMenu.hide()

    @QtCore.pyqtSlot()
    def MinimizeWindow(self):
        self.setMinimized(True)

    @QtCore.pyqtSlot()
    def CloseWindow(self):
        self.close()

    

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = MyUi()
    ui.show()
    sys.exit(app.exec_())
