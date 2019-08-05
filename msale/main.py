from PyQt5 import QtWidgets, QtCore, QtGui, uic
import os

# Load the dynamic uis
from msale.sell import Ui_Sell
from msale.home import Ui_Home
from msale.helpform import HelpForm
from msale.products import ProductsForm
from msale.settings import SettingsForm
from msale.loginform import LoginForm
from msale.aboutform import AboutForm
from msale.infoform import InfoForm
from msale.stockform import StockForm
from msale.salesform import SalesForm
from msale.notificationdialog import NotificationDialog
from msale.debtscreditsform import CreditsForm
from msale.accountsform import AccountsForm

from msale.database import db
from msale.icons import resources
import pendulum

class MainForm(QtWidgets.QMainWindow):
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

        self.widget.HomeBtn.setIcon(QtGui.QIcon(":/icons/home_48px_grey.png"))
        self.widget.StockMenu.setIcon(QtGui.QIcon(":/icons/move_by_trolley_52px_grey.png"))
        self.widget.SalesMenu.setIcon(QtGui.QIcon(":/icons/sales_60px_grey.png"))
        self.widget.SellMenu.setIcon(QtGui.QIcon(":/icons/icons8_sell_52px.png"))
        self.widget.ProductsMenu.setIcon(QtGui.QIcon(":/icons/product_60px_grey.png"))
        self.widget.AccountsMenu.setIcon(QtGui.QIcon(":/icons/user_menu_64px_grey.png"))
        self.widget.CreditsMenu.setIcon(QtGui.QIcon(":/icons/creditsdebts.png"))
        self.widget.HelpMenu.setIcon(QtGui.QIcon(":/icons/help_64px_grey.png"))
        self.widget.SettingsMenu.setIcon(QtGui.QIcon("msale/icons/settings_100px_grey.png"))
        self.widget.MenuToggle.setIcon(QtGui.QIcon(":/icons/back.png"))
        self.widget.UserPicture.setIcon(QtGui.QIcon(":/icons/user_male_circle_100px_pink.png"))
        self.widget.CloseBtn.setIcon(QtGui.QIcon(":/icons/close_x_48px_white.png"))
        self.widget.MinimizeBtn.setIcon(QtGui.QIcon(":/icons/minimize_48px_white.png"))
        self.widget.aboutBtn.setIcon(QtGui.QIcon(":/icons/info_w.png"))
        self.widget.helpBtn.setIcon(QtGui.QIcon(":/icons/help_w.png"))
        self.widget.LOGOLABEL.setIcon(QtGui.QIcon(":/icons/icon3.png"))
        self.widget.notificationBtn.setIcon(QtGui.QIcon(":/icons/notify_white.png"))

        self.widget.aboutBtn.clicked.connect(self.OpenAboutDialog)
        self.widget.helpBtn.clicked.connect(self.OpenInfoDialog)
        self.widget.notificationBtn.clicked.connect(self.OpenNotification)
        self.widget.CreditsMenu.clicked.connect(self.OpenDebts)

        self.widget.SettingsMenu.hide()
        #Initialize the home window
        self.active_win = QtWidgets.QWidget()
        self.setLogin()
        self.check_notifications()

        self.user = []
        self.time_ = ''
        self.set_datetime()

        self.showMaximized()
    
    def setLogin(self):
        self.uncheck_all()
        self.widget.TitleWindow.setText("Login Window")
        self.widget.LeftMenu.hide()
        self.widget.MenuToggle.hide()
        self.widget.notificationBtn.setDisabled(True)

        # Add login Screen
        self.active_win.close()
        self.active_win = LoginForm(self)
        self.widget.bodylayout.addWidget(self.active_win)

    def unset_login(self):
        # Undo settings done by the login screen
        self.widget.LeftMenu.show()
        self.widget.MenuToggle.show()
        self.OpenDashboard()
        self.widget.notificationBtn.setDisabled(False)

    def uncheck_all(self):
        self.widget.HomeBtn.setChecked(False)
        self.widget.StockMenu.setChecked(False)
        self.widget.SalesMenu.setChecked(False)
        self.widget.SellMenu.setChecked(False)
        self.widget.ProductsMenu.setChecked(False)
        self.widget.AccountsMenu.setChecked(False)
        self.widget.HelpMenu.setChecked(False)
        self.widget.SettingsMenu.setChecked(False)
        self.widget.CreditsMenu.setChecked(False)

    @QtCore.pyqtSlot()
    def OpenDashboard(self):
        self.widget.TitleWindow.setText("Home Window")
        self.uncheck_all()
        self.widget.HomeBtn.setChecked(True)

        self.active_win.close()
        self.active_win = Ui_Home(self,self.time_)
        self.widget.bodylayout.addWidget(self.active_win)

    @QtCore.pyqtSlot()
    def OpenProducts(self):
        self.widget.TitleWindow.setText("Products Window")
        self.uncheck_all()
        self.widget.ProductsMenu.setChecked(True)

        self.active_win.close()
        self.active_win = ProductsForm(self.user)
        self.widget.bodylayout.addWidget(self.active_win)

    @QtCore.pyqtSlot()
    def OpenStock(self):
        self.widget.TitleWindow.setText("Stock Window")
        self.uncheck_all()
        self.widget.StockMenu.setChecked(True)

        self.active_win.close()
        self.active_win = StockForm(self.user)
        self.widget.bodylayout.addWidget(self.active_win)

    @QtCore.pyqtSlot()
    def OpenSales(self):
        self.widget.TitleWindow.setText("Sales Window")

        self.uncheck_all()
        self.widget.SalesMenu.setChecked(True)
        self.active_win.close()

        self.active_win = SalesForm()
        self.widget.bodylayout.addWidget(self.active_win)


    @QtCore.pyqtSlot()
    def OpenSell(self):
        #Set Window Title, clear the layout widget and add a new widget
        self.widget.TitleWindow.setText("Sell Window")
        self.uncheck_all()
        self.widget.SellMenu.setChecked(True)

        self.active_win.close()
        self.active_win = Ui_Sell(self.user)
        self.widget.bodylayout.addWidget(self.active_win)

    @QtCore.pyqtSlot()
    def OpenAccounts(self):
        self.widget.TitleWindow.setText("Accounts Window")
        self.uncheck_all()
        self.widget.AccountsMenu.setChecked(True)

        self.active_win.close()
        self.active_win = AccountsForm(self.user,self)
        self.widget.bodylayout.addWidget(self.active_win)

    def OpenDebts(self):
        self.widget.TitleWindow.setText("Credit And Debts Window")
        self.uncheck_all()
        self.widget.CreditsMenu.setChecked(True)

        self.active_win.close()
        self.active_win = CreditsForm()
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
            self.widget.MenuToggle.setIcon(QtGui.QIcon(":/icons/back.png"))

        else:
            self.widget.LeftMenu.hide()
            self.widget.MenuToggle.setIcon(QtGui.QIcon(":/icons/foward.png"))

    @QtCore.pyqtSlot()
    def MinimizeWindow(self):
        self.setMinimized(True)

    @QtCore.pyqtSlot()
    def CloseWindow(self):
        self.close()

    
    def OpenAboutDialog(self):
        about = AboutForm()
        about.exec_()

    def OpenInfoDialog(self):
        about = InfoForm()
        about.exec_()
    
    def OpenNotification(self):
        ui = NotificationDialog()
        ui.exec()

    def check_notifications(self):
        self.cursor = db.Database().connect_db().cursor()

        a = pendulum.now()
        tm = "{}-{}-{}".format(a.year,a.month,a.day)

        sql = """ SELECT count(credit_person.cp_mobile_no) from "credit_person"\
            INNER JOIN "debt" ON "credit_person".cp_mobile_no = "debt".cp_mobile_no WHERE debt_due = '{}'""".format(tm)

        sql1 = """SELECT count(date) FROM "on_cheque" WHERE cheque_maturity_date = '{}'""".format(tm)

        try:
            self.cursor.execute(sql)
            ret = self.cursor.fetchone()
            self.cursor.execute(sql1)
            ret1 = self.cursor.fetchone()
            
            if (ret[0] > 0)or(ret1[0] > 0):
                self.widget.notificationBtn.setIcon(QtGui.QIcon(":/icons/notify_red.png"))
            else:
                self.widget.notificationBtn.setIcon(QtGui.QIcon(":/icons/notify_white.png"))
        
        except Exception as e:
            print(e)

    def setUser(self,x):
        for i in x:
            self.user.append(i)

        if self.user[2] == 0:
            role = "Teller"

        elif self.user[2] == 1:
            role = "Admin"

        else:
            role = "Database Admin"

        self.widget.FullNameLabel.setText(self.user[1])
        self.widget.RoleLabel.setText(role)

    def setNoUser(self):
        self.user.clear()

        self.widget.FullNameLabel.setText("Full Name")
        self.widget.RoleLabel.setText("Role")

    def set_datetime(self):
        import pendulum
        a = pendulum.now()
        self.time_ = '{}/{}/{} at {}:{}:{}'.format(a.day,a.month,a.year,a.hour,a.minute,a.second)

def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = MainForm()
    ui.show()
    sys.exit(app.exec_())
