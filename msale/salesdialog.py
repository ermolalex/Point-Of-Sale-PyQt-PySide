from PyQt5 import QtWidgets, QtCore, QtGui, uic

from msale.salesdatedialog import SalesDateDialog
from msale.database import db
from msale.icons import resources
import pendulum

class SalesDialog(QtWidgets.QDialog):
    def __init__(self,title):
        QtWidgets.QDialog.__init__(self)
        
        self.widget = uic.loadUi("msale/forms/salesdialog.ui",self)
        self.widget.label.setText(title)
        self.widget.treeWidget.hide()

        self.widget.comboBox.setDisabled(True)
        self.widget.salesonCB.activated.connect(self.selectionCB)
        self.widget.reloadBtn.clicked.connect(self.load_btn_clicked)

        self.setWindowIcon(QtGui.QIcon(":/icons/icon.png"))


        self.on_dte = ""
        self.fro_dte = ""
        self.to_dte = ""

    def setOndte(self,x):
        self.on_dte = x

    def setFrodte(self,x):
        self.fro_dte = x

    def setTodte(self,x):
        self.to_dte = x

    def load_btn_clicked(self):
        # function to load sales for a particular day

        self.widget.tableWidget_sales.setRowCount(0)
        index = self.widget.salesonCB.currentIndex()

        if index == 0:
            # get todays sales
            d = pendulum.now()
            date = '{}-{}-{}'.format(d.year,d.month,d.day)
            self.load_sales_table(1,date,"")

        elif index == 1:
            # get sales for a particular date
            self.load_sales_table(1, self.on_dte,"")

        else:
            # get sales from a particular range of dates
            self.load_sales_table(2,self.fro_dte,self.to_dte)

    def todays_sales(self):
        self.load_btn_clicked()
        self.widget.salesonCB.setCurrentIndex(0)
        self.widget.salesonCB.hide()

    def selectionCB(self):
        # selection time period for the sales
        self.widget.tableWidget_sales.setRowCount(0)
        index = self.widget.salesonCB.currentIndex()

        if index == 0:
            self.load_btn_clicked()
        elif index == 1:
            ui = SalesDateDialog(self,"Choose Date",1)
            ui.exec_()
            self.load_btn_clicked()
        else:
            ui = SalesDateDialog(self,"Date Period selection",2)
            ui.exec_()
            self.load_btn_clicked

    def load_sales_table(self,id,dte1,dte2):
        # load all sold data to sales table

        self.widget.tableWidget_sales.setRowCount(0)

        if id == 2:
            sql = """SELECT item_name,sum(order_qty),item_bp,item_sp FROM "orders" WHERE order_date \
                BETWEEN '{}' AND '{}' GROUP BY item_name,item_bp,item_sp""".format(dte1,dte2)
        else:
            sql = """SELECT item_name,sum(order_qty),item_bp,item_sp FROM "orders" WHERE order_date ='{}' \
                GROUP BY item_name,item_bp,item_sp""".format(dte1)
        try:
            self.widget.tableWidget_sales.setSortingEnabled(False)
            self.cursor = db.Database().connect_db().cursor()
            self.cursor.execute(sql)
            ret = self.cursor.fetchall()
            for row in ret:
                name = row[0]
                qty = row[1]
                #bp = row[2]
                sp = row[3]
                #u_profit = sp - bp
                t_cost = qty * sp
                #t_profit = qty * u_profit

                rowAt = self.tableWidget_sales.rowCount()
                self.widget.tableWidget_sales.insertRow(rowAt)
                self.widget.tableWidget_sales.setItem(rowAt,0,QtWidgets.QTableWidgetItem(name))
                self.widget.tableWidget_sales.setItem(rowAt,2,QtWidgets.QTableWidgetItem(str(qty)))
                self.widget.tableWidget_sales.setItem(rowAt,1,QtWidgets.QTableWidgetItem(str(sp)))
                #self.widget.tableWidget_sales.setItem(rowAt,3,QtWidgets.QTableWidgetItem(str(u_profit)))
                self.widget.tableWidget_sales.setItem(rowAt,3,QtWidgets.QTableWidgetItem(str(t_cost)))
                #self.widget.tableWidget_sales.setItem(rowAt,5,QtWidgets.QTableWidgetItem(str(t_profit)))
            self.widget.tableWidget_sales.setSortingEnabled(True)

            try:
                self.get_totals(id,dte1,dte2)

            except Exception as abb:
                txt = "Error [1E5] \n"+str(abb)
                self.show_msg(txt)

        except Exception as aa:
            txt = "Error [1E6] \n"+str(aa)
            self.show_msg(txt)

    def get_totals(self,id,dte1,dte2):
        # function to calculate totals for each sales section

        if self.widget.tableWidget_sales.rowCount() == 0:
            self.widget.cashLbl.setText(str(0.0))
            self.widget.mpesaLbl.setText(str(0.0))
            self.widget.cashmpesaLbl.setText(str(0.0))
            self.widget.creditLbl.setText(str(0.0))
            self.widget.creditpaidLbl.setText(str(0.0))
            self.widget.chequeLbl.setText(str(0.0))
            self.widget.totalsLbl.setText(str(0.0))
            self.widget.totalspaidLbl.setText(str(0.0))

        else:
            if id == 2:
                sql_get_cash_tot = """SELECT item_name,sum(order_qty),item_bp,item_sp,count(item_name) FROM "orders" WHERE order_date \
                    BETWEEN '{}' AND '{}' AND payment_by = '{}' GROUP BY item_name,item_bp,item_sp""".format(dte1,dte2,'cash')
                sql_get_cashmpesa_tot = """SELECT item_name,sum(order_qty),item_bp,item_sp,count(item_name) FROM "orders" WHERE order_date \
                    BETWEEN '{}' AND '{}' AND payment_by = '{}' GROUP BY item_name,item_bp,item_sp""".format(dte1,dte2,'cashmpesa')
                sql_get_mpesa_tot = """SELECT item_name,sum(order_qty),item_bp,item_sp,count(item_name) FROM "orders" WHERE order_date \
                    BETWEEN '{}' AND '{}' AND payment_by = '{}' GROUP BY item_name,item_bp,item_sp""".format(dte1,dte2,'mpesa')
                sql_get_credit_tot = """SELECT item_name,sum(order_qty),item_bp,item_sp,count(item_name) FROM "orders" WHERE order_date \
                    BETWEEN '{}' AND '{}' AND payment_by = '{}' GROUP BY item_name,item_bp,item_sp""".format(dte1,dte2,'credit')
                sql_get_cheque_tot = """SELECT item_name,sum(order_qty),item_bp,item_sp,count(item_name) FROM "orders" WHERE order_date \
                    BETWEEN '{}' AND '{}' AND payment_by = '{}' GROUP BY item_name,item_bp,item_sp""".format(dte1,dte2,'cheque')
                sql_tot_paid = """SELECT count(*),sum(debt_pay_amount) FROM "debt_pay" WHERE debt_pay_date \
                    BETWEEN '{}' AND '{}'""".format(dte1,dte2)
            else:
                sql_get_cash_tot = """SELECT item_name,sum(order_qty),item_bp,item_sp ,count(item_name) FROM "orders" WHERE order_date ='{}'\
                    AND payment_by = '{}' GROUP BY item_name,item_bp,item_sp""".format(dte1,'cash')
                sql_get_mpesa_tot = """SELECT item_name,sum(order_qty),item_bp,item_sp,count(item_name) FROM "orders" WHERE order_date ='{}'\
                    AND payment_by = '{}' GROUP BY item_name,item_bp,item_sp""".format(dte1,'mpesa')
                sql_get_cashmpesa_tot = """SELECT item_name,sum(order_qty),item_bp,item_sp,count(item_name) FROM "orders" WHERE order_date = '{}'\
                     AND payment_by = '{}' GROUP BY item_name,item_bp,item_sp""".format(dte1,'cashmpesa')
                sql_get_credit_tot = """SELECT item_name,sum(order_qty),item_bp,item_sp,count(item_name) FROM "orders" WHERE order_date ='{}'\
                    AND payment_by = '{}' GROUP BY item_name,item_bp,item_sp""".format(dte1,'credit')
                sql_get_cheque_tot = """SELECT item_name,sum(order_qty),item_bp,item_sp,count(item_name) FROM "orders" WHERE order_date ='{}'\
                    AND payment_by = '{}' GROUP BY item_name,item_bp,item_sp""".format(dte1,'cheque')
                sql_tot_paid = """SELECT count(*),sum(debt_pay_amount) FROM "debt_pay" WHERE debt_pay_date = '{}'""".format(dte1)

            try:
                sum_ = 0
                self.cursor = db.Database().connect_db().cursor()
                # get cash totals
                try:
                    self.cursor.execute(sql_get_cash_tot)
                    ret_cash = self.cursor.fetchall()
                    cash = 0.0
                    profits = 0.0
                    money = 0.0
                    if len(ret_cash) != 0:
                        for row in ret_cash:
                            qty_cash = row[1]
                            bp_cash = row[2]
                            sp_cash = row[3]
                            u_profit_cash = sp_cash - bp_cash
                            t_cost_cash = qty_cash * sp_cash
                            t_profit_cash = qty_cash * u_profit_cash
                            cash += t_cost_cash
                            sum_ += t_cost_cash
                            profits += t_profit_cash
                            money += t_cost_cash
                    self.widget.cashLbl.setText(str(cash))
                    del cash

                except Exception as e1:
                    print("E1 :"+ str(e1))
                
                # get mpesa totals
                try:
                    self.cursor.execute(sql_get_mpesa_tot)
                    ret_mpesa = self.cursor.fetchall()
                    mpesa = 0.0
                    if len(ret_mpesa) != 0:
                        for row in ret_mpesa:
                            qty_mpesa = row[1]
                            bp_mpesa = row[2]
                            sp_mpesa = row[3]
                            u_profit_mpesa = sp_mpesa - bp_mpesa
                            t_cost_mpesa = qty_mpesa * sp_mpesa
                            t_profit_mpesa = qty_mpesa * u_profit_mpesa
                            sum_ += t_cost_mpesa
                            mpesa += t_cost_mpesa
                            profits += t_profit_mpesa
                            money += t_cost_mpesa

                    self.widget.mpesaLbl.setText(str(mpesa))
                    mpesa = 0.0

                except Exception as e2:
                    print("E2 :"+ str(e2))
                
                # get cashmpesa totals
                try:
                    self.cursor.execute(sql_get_cashmpesa_tot)
                    ret_cashmpesa = self.cursor.fetchall()
                    cashmpesa = 0.0
                    if len(ret_cashmpesa) != 0:
                        for row in ret_cashmpesa:
                            qty_cashmpesa = row[1]
                            bp_cashmpesa = row[2]
                            sp_cashmpesa = row[3]
                            u_profit_cashmpesa = sp_cashmpesa - bp_cashmpesa
                            t_cost_cashmpesa = qty_cashmpesa * sp_cashmpesa
                            t_profit_cashmpesa = qty_cashmpesa * u_profit_cashmpesa
                            sum_ += t_cost_cashmpesa
                            cashmpesa += t_cost_cashmpesa
                            profits += t_profit_cashmpesa
                            money += t_cost_cashmpesa

                    self.widget.cashmpesaLbl.setText(str(cashmpesa))

                except Exception as cashmpesa_e:
                    print("E2 :"+ str(cashmpesa_e))

                # get credit totals
                try:
                    self.cursor.execute(sql_get_credit_tot)
                    ret_credit = self.cursor.fetchall()
                    credits = 0.0
                    if len(ret_credit) != 0:
                        for row in ret_credit:
                            qty_credit = row[1]
                            sp_credit = row[3]
                            t_cost_credit = qty_credit * sp_credit
                            sum_ += t_cost_credit
                            credits += t_cost_credit
                        
                        
                    self.widget.creditLbl.setText(str(credits))
                except Exception as e3:
                    print("E3 :"+ str(e3))
                
                try:
                    self.cursor.execute(sql_tot_paid)
                    paid_credit = 0.00 # paid money
                    ret_paid_credit = self.cursor.fetchone()
                    if ret_paid_credit[0] != 0:
                        money += ret_paid_credit[1]
                        paid_credit = ret_paid_credit[1]
                    
                    self.widget.creditpaidLbl.setText(str(paid_credit))
                    credits = paid_credit = 0.0

                except Exception as e4:
                    print("E4 :"+ str(e4))

                # get cheque totals
                try:
                    self.cursor.execute(sql_get_cheque_tot)
                    cheque_ret = self.cursor.fetchall()
                    cheque = 0.0
                    
                    if len(cheque_ret) != 0:
                        for row in cheque_ret:
                            qty_cheque = row[1]
                            bp_cheque = row[2]
                            sp_cheque = row[3]
                            u_profit_cheque = sp_cheque - bp_cheque
                            t_cost_cheque = qty_cheque * sp_cheque
                            t_profit_cheque = qty_cheque * u_profit_cheque
                            sum_ += t_cost_cheque
                            cheque += t_cost_cheque 
                            profits += t_profit_cheque
                            money += t_cost_cheque
                    self.widget.chequeLbl.setText(str(cheque))
            
                except Exception as e5:
                    print("E5 :"+str(e5))
                
                #self.costs.set_t_profits(profits)
                self.widget.totalsLbl.setText(str(sum_))
                self.widget.totalspaidLbl.setText(str(money))

            except Exception as aa:
                print('>> Error at compute totals :: '+str(aa))

    def show_msg(self,msg):

        m = QtWidgets.QMessageBox()
        m.setText(msg)
        m.setStyleSheet("font: 12px;")
        m.setWindowTitle('Error')
        m.setIcon(QtWidgets.QMessageBox.Warning)
        m.exec_()
