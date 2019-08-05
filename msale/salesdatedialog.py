from PyQt5 import QtWidgets, QtCore, QtGui, uic

from msale.database import db
from msale.icons import resources
import pendulum

class SalesDateDialog(QtWidgets.QDialog):
    def __init__(self,daddy,title,ind):
        QtWidgets.QDialog.__init__(self)
        self.daddy = daddy

        self.widget = uic.loadUi("msale/forms/salesdatedialog.ui",self)
        self.widget.label.setText(title)
        self.setWindowIcon(QtGui.QIcon(":/icons/icon.png"))


        if ind == 1:
            self.widget.periodWdg.hide()
            self.index = 1

        else:
            self.widget.onWdg.hide()
            self.index = 2

        self.widget.openBtn.clicked.connect(self.open)
        self.widget.cancelBtn.clicked.connect(self.close_)

        a = pendulum.now()
        dte = "{}-{}-{}".format(a.month,a.day,a.year)
        self.widget.dateEdit_salesOn.setDateTime(QtCore.QDateTime(QtCore.QDate.fromString(dte,"M-d-yyyy"), QtCore.QTime(0, 0, 0)))
        self.widget.dateEdit_salesFro.setDateTime(QtCore.QDateTime(QtCore.QDate.fromString(dte,"M-d-yyyy"), QtCore.QTime(0, 0, 0)))
        self.widget.dateEdit_salesTo.setDateTime(QtCore.QDateTime(QtCore.QDate.fromString(dte,"M-d-yyyy"), QtCore.QTime(0, 0, 0)))

    #def closeEvent(self,event):
    #    self.close_()

    def open(self):
        if self.index == 1:
            date = self.dateEdit_salesOn.date() 
            sql_date = '{}-{}-{}'.format(date.year(),date.month(),date.day())
            self.daddy.setOndte(sql_date)

            self.daddy.load_btn_clicked()
            self.close()

        else:
            date1 = self.dateEdit_salesFro.date()
            sql_date1 = '{}-{}-{}'.format(date1.year(),date1.month(),date1.day())
            date2 = self.dateEdit_salesTo.date()
            sql_date2 = '{}-{}-{}'.format(date2.year(),date2.month(),date2.day())
            self.daddy.setFrodte(sql_date1)
            self.daddy.setTodte(sql_date2)

            self.daddy.load_btn_clicked()
            self.close()

    def close_(self):
        self.daddy.salesonCB.setCurrentIndex(0)
        self.daddy.load_btn_clicked()
        self.close()