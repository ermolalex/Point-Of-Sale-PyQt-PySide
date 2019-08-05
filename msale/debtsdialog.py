
from PyQt5 import QtCore, QtGui, QtWidgets, uic

import pendulum
from msale.database import db
from msale.icons import resources

class DebtsDialog(QtWidgets.QDialog):
    def __init__(self,mobile):
        QtWidgets.QDialog.__init__(self)
        self.no = mobile
        
        self.widget = uic.loadUi("msale/forms/debtsdialog.ui",self)

        self.widget.comboBox_filter.currentIndexChanged.connect(self.load_details)
        self.widget.pushButton_quit_debt_items.clicked.connect(lambda: self.close())

        self.widget.tableWidget_debt_items.setColumnWidth(0,150)
        self.widget.tableWidget_debt_items.setColumnWidth(2,50)
        self.widget.tableWidget_debt_items.setColumnWidth(5,150)

        self.load_details()
        self.setWindowIcon(QtGui.QIcon(":/icons/icon.png"))


    def load_details(self):
        # to load creditee loaned items and populate onto the table
        
        ind = self.widget.comboBox_filter.currentIndex()
        _p = pendulum.now()
        date_tday = "{}-{}-{}".format(_p.year,_p.month,_p.day)

        if ind == 0:
            # all items taken
            self.widget.tableWidget_debt_items.setRowCount(0)
            sql = """SELECT item_name, order_qty, item_sp, order_date, timestamp_ FROM "orders" WHERE timestamp_ IN (\
                SELECT timestamp_ FROM "on_credit" WHERE cp_mobile_no = '{}')""".format(self.no)
            self.load_table_data(sql)

        elif ind == 1:
            self.widget.tableWidget_debt_items.setRowCount(0)
            # items taken today
            sql = """SELECT item_name, order_qty, item_sp, order_date, timestamp_ FROM "orders" WHERE timestamp_ IN (\
                SELECT timestamp_ FROM "on_credit" WHERE cp_mobile_no = '{}' AND date = '{}')""".format(self.no,date_tday)
            self.load_table_data(sql)

        else:
            self.widget.tableWidget_debt_items.setRowCount(0)
            a = _p.start_of('month')
            dte_start = "{}-{}-{}".format(a.year,a.month,a.day)
            a_ = _p.end_of('month')
            dte_end = "{}-{}-{}".format(a_.year,a_.month,a_.day)

            sql = """SELECT item_name, order_qty, item_sp, order_date, timestamp_ FROM "orders" WHERE timestamp_ IN (\
                SELECT timestamp_ FROM "on_credit" WHERE cp_mobile_no = '{}' AND date BETWEEN '{}' AND '{}'\
                    )""".format(self.no,dte_start, dte_end)
            self.load_table_data(sql)

    
    def load_table_data(self,sql):
        sql_bal = """SELECT cp_balance FROM "credit_person" WHERE cp_mobile_no = '{}'""".format(self.no)
        self.cursor = db.Database().connect_db().cursor()

        try:
            self.cursor.execute(sql)
            ret = self.cursor.fetchall()

            self.cursor.execute(sql_bal)
            bal = self.cursor.fetchone()

            _totals = 0.0
            
            for row in ret:
                _name = row[0]
                _qty = row[1]
                _sp = row[2]
                _date =  row[3]
                _tm_stamp = row[4]
                _totals += _qty * _sp

                _rows = self.widget.tableWidget_debt_items.rowCount()
                self.widget.tableWidget_debt_items.insertRow(_rows)

                self.widget.tableWidget_debt_items.setItem(_rows,0, QtWidgets.QTableWidgetItem(_name))
                self.widget.tableWidget_debt_items.setItem(_rows,1, QtWidgets.QTableWidgetItem(str(_sp)))
                self.widget.tableWidget_debt_items.setItem(_rows,2, QtWidgets.QTableWidgetItem(str(_qty)))
                self.widget.tableWidget_debt_items.setItem(_rows,3, QtWidgets.QTableWidgetItem(str(_date)))
                self.widget.tableWidget_debt_items.setItem(_rows,4, QtWidgets.QTableWidgetItem(str(_qty * _sp)))
                self.widget.tableWidget_debt_items.setItem(_rows,5, QtWidgets.QTableWidgetItem(str(_tm_stamp)))
            
            if len(ret) != 0:
                _bal = bal[0]
                _paid = _totals - _bal
            else:
                _bal = 0.0
                _paid = 0.0

            self.widget.label_totalCost.setText(str(_totals))
            self.widget.label_amnt_paid.setText(str(_paid))
            self.widget.label_amnt_due.setText(str(_bal))

        except Exception as a:
            print(a)
