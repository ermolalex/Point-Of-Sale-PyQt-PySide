from PyQt5 import QtWidgets, QtCore, QtGui, uic

#Load other Ui's
from msale.search import Ui_Search
from msale.database import db
from msale.selltools import SellToolWidget
from msale.paymentdialog import PaymentDialog
from msale.icons import resources

import pendulum

class Ui_Sell(QtWidgets.QWidget):
    def __init__(self,user):

        """
        Sell Widget for the MS Point of sale software
        //Initialize dynamically the ui
        //set the icons not loaded dynamically by the UiLoader
        //Setup slot functions for the signals sent by the dynamic Ui
        """
        QtWidgets.QWidget.__init__(self)
        
        self.widget = uic.loadUi("msale/forms/sell.ui",self)
        self.user = user

        self.widget.AddToCartBtn.setIcon(QtGui.QIcon(":/icons/add_shopping_cart_48px_gray.png"))
        self.widget.SearchBtn.setIcon(QtGui.QIcon(":/icons/search_database_48px_grey.png"))

        self.widget.AddToCartBtn.clicked.connect(self.add_item_to_table)
        self.widget.payoptionBtn.clicked.connect(self.open_other_payments)
        self.widget.cashpaymentBtn.clicked.connect(self.complete_transaction_cash)
        self.widget.cashamountLE.textChanged.connect(self.update_balance)
        
        self.possible_list = []
        self.sum = 0.0
        self.set_AutoComplete() # Set Autocompleter

        QtWidgets.QShortcut(QtGui.QKeySequence("F7"),self,self.complete_transaction_cash)
        QtWidgets.QShortcut(QtGui.QKeySequence("F5"),self,self.add_item_to_table)
        QtWidgets.QShortcut(QtGui.QKeySequence("F6"),self,self.open_other_payments)

    @QtCore.pyqtSlot()
    def open_searchWindow(self):
        search = Ui_Search()
        search.show()

    def set_AutoComplete(self):
        self.possible_list.clear() 
        self.mydb = db.Database().connect_db()
        self.cursor = self.mydb.cursor()

        sql = """SELECT item_name FROM "item" """
        try:
            self.cursor.execute(sql)
            ret = self.cursor.fetchall()
            for i in ret:
                self.possible_list.append(i[0])
            
            self.completer = QtWidgets.QCompleter(self.possible_list)
            self.completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
            self.completer.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
            self.searchLE.setCompleter(self.completer)
                
        except Exception as e:
            print("Exception at Autocompletion>>",str(e))

    def reload_totals(self):
        # function to reload totals display label
        self.sum = 0.0
        rows = self.widget.tableWidget.rowCount()
        _sum = 0.0
        if rows != 0:
            for x in range(rows):
                _qty = int(self.widget.tableWidget.item(x,2).text())
                _price = float(self.widget.tableWidget.item(x,1).text())

                _sum += _qty * _price

            self.sum = _sum

        txt =  '{}'.format(_sum)
        self.widget.totalsLabel.setText(txt)

    def add_item_to_table(self):
        
        # function to search for entered item and add the items particulars 
        # to the sell window
        self.mydb = db.Database().connect_db()
        self.cursor = self.mydb.cursor()

        item_name = self.widget.searchLE.text()
        item_qty = 1

        sql = """SELECT count(*) FROM "item" INNER JOIN "stock" ON "item".item_name\
             = "stock".item_name WHERE "item".item_name = '{}'""".format(item_name)

        try:
            self.cursor.execute(sql)
            ret = self.cursor.fetchall()

            if ret[0][0] == 0:
                y = "Input is either empty or selected item has no stock quantity added"
                self.show_msg(y)

            else:
                sql1_ = """SELECT item.item_name,item_sp,stock_qty FROM "item" INNER JOIN "stock" ON \
                    item.item_name = stock.item_name WHERE item.item_name ='{}'""".format(item_name)
                try:
                    self.cursor.execute(sql1_)
                    ret = self.cursor.fetchone()
                    name = ret[0]
                    sp = ret[1]
                    qty = ret[2]
                    if qty >= item_qty:
                        y_rows = self.widget.tableWidget.rowCount()
                        qty_sum = 0
                        for x in range(y_rows):
                            _name = self.widget.tableWidget.item(x,0).text()
                            if _name == name:
                                _qty = int(self.widget.tableWidget.item(x,2).text())
                                qty_sum += _qty
                            else:
                                continue
                        n_item_qty = qty_sum + item_qty

                        if qty >= n_item_qty:
                            total_cost = item_qty * sp
                            self.sum += total_cost
                            try:
                                tools = SellToolWidget(self,self.widget.tableWidget)
                                
                                rowAt = self.widget.tableWidget.rowCount()
                                self.widget.tableWidget.insertRow(rowAt)
                                self.widget.tableWidget.setItem(rowAt,0,QtWidgets.QTableWidgetItem(name))
                                self.widget.tableWidget.setItem(rowAt,1,QtWidgets.QTableWidgetItem(str(sp)))
                                self.widget.tableWidget.setCellWidget(rowAt,3,tools)
                                self.widget.tableWidget.setItem(rowAt,2,QtWidgets.QTableWidgetItem(str(item_qty)))
                                self.widget.tableWidget.setItem(rowAt,4,QtWidgets.QTableWidgetItem(str(total_cost)))
                                
                                
                                self.widget.totalsLabel.setText(str(self.sum))
                                self.widget.searchLE.setText('')

                            except Exception as a:
                                y = "Error Commiting changes to database\n "+str(a)
                                self.show_msg(y)
                        else:
                            y = "Quantity remaining is not enough to complete the transaction.\nCheck on the quantity remaining on Stock.!"
                            self.show_msg(y)
                    else:
                        y = "The quantity requested exceeds the quantity available!"
                        self.show_msg(y)

                except Exception as a2:
                    y ="Error fetching the item [SELL_WIN] : "+str(a2)
                    self.show_msg(y)

        except Exception as e3:
            y = "Error Collecting the requested Item [SELL_WIN] : "+str(e3)
            self.show_msg(y)

    def clear_all_(self):
        self.widget.searchLE.setText('')
        self.widget.tableWidget.setRowCount(0)
        self.widget.totalsLabel.setText(str(0.0))
        self.widget.cashamountLE.setText("")
        self.widget.changeamountLE.setText("")
        self.sum = 0

    def complete_transaction_cash(self):
        # complete a cash transaction
        # orders table: item_name, bp,sp, order_qty, payment_by, timestamp_,order_date, served-by
        # on_cash : timestamp_, date, cash_cost
        if self.widget.tableWidget.rowCount() == 0:
            self.show_msg("Failed, no Item Has been added to Cart!")

        else:
            tm = pendulum.now()

            self.db = db.Database().connect_db()
            self.cursor = self.db.cursor()

            tm_now = "{}-{}-{}".format(tm.year,tm.month,tm.day)

            cash_paid_ = self.widget.cashamountLE.text()
            if len(str(cash_paid_)) == 0:
                self.cash_paid = 0.00
            else:
                self.cash_paid = float(cash_paid_)

            if self.cash_paid >= self.sum:
                rows = self.widget.tableWidget.rowCount()
                for x in range(rows):
                    name = self.widget.tableWidget.item(x,0).text()
                    sp = self.widget.tableWidget.item(x,1).text()
                    qty = self.widget.tableWidget.item(x,2).text()

                    get_bp = """SELECT item_bp FROM "item" WHERE item_name = '{}'""".format(name)
                    get_qty = """SELECT stock_qty FROM "stock" WHERE item_name = '{}'""".format(name)
                    try:
                        self.cursor.execute(get_bp)
                        get = self.cursor.fetchone()
                        bp = get[0]
                        self.cursor.execute(get_qty)
                        get_ = self.cursor.fetchone()
                        qty_ = get_[0]

                        orders_sql = """INSERT INTO "orders"(item_name,item_bp,item_sp,order_qty,payment_by,timestamp_,order_date,served_by)\
                            VALUES('{}','{}','{}','{}','{}','{}','{}','{}')""".format(name,bp,sp,qty,'cash',tm,tm_now,self.user[0])
                        stock_sql = """UPDATE "stock" SET stock_qty = '{}' WHERE item_name = '{}'""".format(qty_ - int(qty),name)
                        

                        self.cursor.execute(orders_sql)
                        self.cursor.execute(stock_sql)
                        
                    except Exception as a:
                        self.s = False
                        self.success = False
                        self.message(">> Error saving to on_cash :: ",str(a))
                on_cash_sql = """INSERT INTO "on_cash"(timestamp_,date,cash_cost) \
                            VALUES('{}','{}','{}')""".format(tm,tm_now,self.sum)

                self.cursor.execute(on_cash_sql)
                self.db.commit()
                self.clear_all_()
                
                print(">> Saved to cash table Successfuly >>")

            else:
                err = "Amount entered is not enough to complete transaction ..."
                self.message(err,"amount entered is less than cost of the item(s)")

            self.db.close()

    def update_balance(self):
        paid = self.widget.cashamountLE.text()
        if len(paid) == 0:
            self.widget.changeamountLE.setText(str(0.0))
        elif float(paid) <= self.sum:
            self.widget.changeamountLE.setText(str(0.0))
        else:
            self.widget.changeamountLE.setText(str(float(paid)-self.sum))

    def message(self,x,y):
        msg = QtWidgets.QMessageBox()
        msg.setText(x)
        msg.setStyleSheet("font:12pt")
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setInformativeText(y)
        msg.setWindowTitle("Error")
        msg.exec_()

    def open_other_payments(self):
        if self.widget.tableWidget.rowCount() == 0:
            self.show_msg("Failed, no Item Has been added to Cart!")

        else:
            dlg = PaymentDialog(self.widget.tableWidget,self.sum,self,self.user)
            dlg.exec_()

    def show_msg(self,msg):
        m = QtWidgets.QMessageBox()
        m.setText(msg)
        m.setWindowTitle('...')
        m.setIcon(QtWidgets.QMessageBox.Warning)
        m.exec_()

    


