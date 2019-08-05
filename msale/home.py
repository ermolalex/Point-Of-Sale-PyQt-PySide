from PyQt5 import QtWidgets, QtCore, QtGui, uic

from msale.database import db
import pendulum
from msale.icons import resources

class Ui_Home(QtWidgets.QWidget):
    def __init__(self,father,time_):

        """
        Home Window for the MS Point of sale software
        //Initialize dynamically the ui
        //set the icons not loaded dynamically by the UiLoader
        //Setup slot functions for the signals sent by the dynamic Ui
        """
        QtWidgets.QWidget.__init__(self)
        self.father = father
        
        self.widget = uic.loadUi("msale/forms/home.ui",self)

        self.widget.backupDbBtn.setIcon(QtGui.QIcon(":/icons/database_backup_48px_white.png"))
        self.widget.switchUserBtn.setIcon(QtGui.QIcon(":/icons/change_user_white.png"))
        self.widget.logoutBtn.setIcon(QtGui.QIcon(":/icons/logout_white.png"))

        self.widget.switchUserBtn.clicked.connect(self.switch_user)
        self.widget.logoutBtn.clicked.connect(self.logout_user)
        #self.widget.logoutBtn.setEnabled(True)
        #self.widget.switchUserBtn.setEnabled(True)

        self.notify()
        self.count_cashsales()
        self.count_mpesasales()
        self.count_cashmpesasales()
        self.count_creditsales()
        self.count_chequesales()
        self.time_ = time_
        self.setupTime()

    def setupTime(self):
        self.widget.datetimeLbl.setText(self.time_)

    def switch_user(self):
        # Switch to login window
        self.father.setNoUser()
        self.father.setLogin()

    def logout_user(self):
        # Close Application
        self.father.CloseWindow()

    def notify(self):
        self.cursor = db.Database().connect_db().cursor()

        a = pendulum.now()
        tm = "{}-{}-{}".format(a.year,a.month,a.day)

        sql = """ SELECT count(credit_person.cp_mobile_no) from "credit_person"\
            INNER JOIN "debt" ON "credit_person".cp_mobile_no = "debt".cp_mobile_no WHERE debt_due = '{}'""".format(tm)

        sql1 = """SELECT count(date) FROM "on_cheque" WHERE cheque_maturity_date = '{}'""".format(tm)

        try:
            self.cursor.execute(sql)
            ret = self.cursor.fetchone()
            self.widget.debtRemindersBadgeLabel.setText(str(ret[0]))
            if ret[0] > 0:
                self.widget.debtRemindersBadgeLabel.setStyleSheet("background-color:#df0000;border-radius:20px;")
            
            self.cursor.execute(sql1)
            ret1 = self.cursor.fetchone()
            self.widget.chequeRemindersBadgeLabel.setText(str(ret1[0]))
            if ret1[0] > 0:
                self.widget.chequeRemindersBadgeLabel.setStyleSheet("background-color:#df0000;border-radius:20px;")
        
        except Exception as _a:
            print(_a)

    def count_cashsales(self):
        cursor = db.Database().connect_db().cursor()

        a = pendulum.now()
        tm = "{}-{}-{}".format(a.year,a.month,a.day)

        sql = """ SELECT count(order_qty), sum(order_qty) from "orders" WHERE payment_by = 'cash' AND order_date = '{}' """.format(tm)
        try:
            cursor.execute(sql)
            ret = cursor.fetchone()
            if ret[0] != 0:
                self.widget.cashSalesBadge.setText(str(ret[1]))
            else:
                self.widget.cashSalesBadge.setText(str(0))
            
        except Exception as e:
            print(e)

    def count_mpesasales(self):
        cursor = db.Database().connect_db().cursor()

        a = pendulum.now()
        tm = "{}-{}-{}".format(a.year,a.month,a.day)

        sql = """ SELECT count(order_qty), sum(order_qty) from "orders" WHERE payment_by = 'mpesa' AND order_date = '{}' """.format(tm)
        try:
            cursor.execute(sql)
            ret = cursor.fetchone()

            if ret[0] != 0:
                self.widget.mpesaBadgeLabel.setText(str(ret[1]))
            else:
                self.widget.mpesaBadgeLabel.setText(str(0))
            
        except Exception as e:
            print(e)

    def count_cashmpesasales(self):
        cursor = db.Database().connect_db().cursor()

        a = pendulum.now()
        tm = "{}-{}-{}".format(a.year,a.month,a.day)

        sql = """ SELECT count(order_qty), sum(order_qty) from "orders" WHERE payment_by = 'cashmpesa' AND order_date = '{}' """.format(tm)
        try:
            cursor.execute(sql)
            ret = cursor.fetchone()

            if ret[0] != 0:
                self.widget.cashmpesaLbl.setText(str(ret[1]))
            else:
                self.widget.cashmpesaLbl.setText(str(0))
            
        except Exception as e:
            print(e)

    def count_creditsales(self):
        cursor = db.Database().connect_db().cursor()

        a = pendulum.now()
        tm = "{}-{}-{}".format(a.year,a.month,a.day)

        sql = """ SELECT count(order_qty), sum(order_qty) from "orders" WHERE payment_by = 'credit' AND order_date = '{}' """.format(tm)
        try:
            cursor.execute(sql)
            ret = cursor.fetchone()

            if ret[0] != 0:
                self.widget.creditBadgeLabel.setText(str(ret[1]))
            else:
                self.widget.creditBadgeLabel.setText(str(0))
            
        except Exception as e:
            print(e)

    def count_chequesales(self):
        cursor = db.Database().connect_db().cursor()

        a = pendulum.now()
        tm = "{}-{}-{}".format(a.year,a.month,a.day)

        sql = """ SELECT count(order_qty), sum(order_qty) from "orders" WHERE payment_by = 'cheque' AND order_date = '{}' """.format(tm)
        try:
            cursor.execute(sql)
            ret = cursor.fetchone()

            if ret[0] != 0:
                self.widget.chequebadgelbl.setText(str(ret[1]))
            else:
                self.widget.chequebadgelbl.setText(str(0))
            
        except Exception as e:
            print(e)
