
from PyQt5 import QtCore, QtGui, QtWidgets, uic

import pendulum
from msale.database import db
from msale.icons import resources

class NotificationDialog(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.widget = uic.loadUi("msale/forms/notificationdialog.ui",self)
        self.notify()
        self.setWindowIcon(QtGui.QIcon(":/icons/icon.png"))

        
    def notify(self):
        self.cursor = db.Database().connect_db().cursor()

        a = pendulum.now()
        tm = "{}-{}-{}".format(a.year,a.month,a.day)

        sql = """ SELECT credit_person.cp_mobile_no,cp_firstname, cp_lastname,debt_balance from "credit_person"\
            INNER JOIN "debt" ON "credit_person".cp_mobile_no = "debt".cp_mobile_no WHERE debt_due = '{}'""".format(tm)

        sql1 = """SELECT date,cheque_amount FROM "on_cheque" WHERE cheque_maturity_date = '{}'""".format(tm)

        try:
            flag = 0
            self.cursor.execute(sql)
            ret = self.cursor.fetchall()
            for row in ret:
                flag = 1
                self.get = True
                self.widget.groupBox_no.hide()
                self.widget.groupBox_debts.show()
                self.widget.groupBox_cheque.hide()
                a = row[0]
                b = row[1]
                c = row[2]
                d = row[3]

                txt = "{} {} (0{}) Amount : {}Ksh".format(b,c,a,d)
                self.widget.listView_debts.addItem(txt)
            
            self.cursor.execute(sql1)
            ret1 = self.cursor.fetchall()
            for row in ret1:
                self.get = True
                if flag == 1:
                    self.widget.groupBox_debts.show()
                    self.widget.groupBox_cheque.show()
                    self.setMinimumWidth(460)
                else:
                    self.widget.groupBox_debts.hide()
                    self.widget.groupBox_no.hide()
                    self.setMinimumWidth(460)

                a = row[0]
                b = row[1]

                txt = "Cheque date :{}, Cheque Amount : {}Ksh".format(a,b)
                self.widget.listView_cheque.addItem(txt)
        
        except Exception as _a:
            print(_a)

