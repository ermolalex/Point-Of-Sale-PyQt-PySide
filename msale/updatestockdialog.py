from PyQt5 import QtWidgets, QtCore, QtGui, uic

import pendulum
from msale.database import db
from msale.authenticationdialog import AuthenticationDialog
from msale.icons import resources


class StockUpdateDialog(QtWidgets.QDialog):
    def __init__(self,title,mode,daddy,user):
        QtWidgets.QDialog.__init__(self)
        self.daddy = daddy
        self.user = user
        
        self.widget = uic.loadUi("msale/forms/updatestockdialog.ui",self)
        self.setWindowTitle(title)

        if mode == "add":
            self.widget.updateStockTearBtn.hide()

        else:
            self.widget.updateStockAddBtn.hide()
            self.widget.label.setText("Quantity to Remove")

        self.widget.updateStockAddBtn.clicked.connect(self.add_stock)
        self.widget.updateStockTearBtn.clicked.connect(self.tear_stock)
        self.widget.addBtn.clicked.connect(self.add_item_to_table)
        self.possible_list = []
        self.setAutoComplete()
        self.setWindowIcon(QtGui.QIcon(":/icons/icon.png"))


    def setAutoComplete(self):
        try:
            self.mydb = db.Database().connect_db()
            self.cursor = self.mydb.cursor()

            sql = '''SELECT item_name FROM "item" '''
            self.cursor.execute(sql)
            ret = self.cursor.fetchall()
            self.possible_list.clear()

            for i in ret:
                self.possible_list.append(i[0])

        except Exception as e:
            print("Exception at Autocompletion>>",str(e))
        
        self.set_completer(self.possible_list)


    def set_completer(self,ls):
        self.completer = QtWidgets.QCompleter(ls)
        self.completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.completer.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
        self.widget.searchLineEdit.setCompleter(self.completer)
        self.widget.clearBtn.clicked.connect(self.clear_fields)
    
    # Add the searched item to table
    def add_item_to_table(self):
        name = self.widget.searchLineEdit.text()
        if len(name) == 0:
            print('Empty Search Input Field!')
        
        else:
            a = db.Database().check_if_exists('item','item_name',name)
            if a == True:
                sql = """SELECT item.item_name,stock_qty FROM "item" INNER JOIN \
                    "stock" ON item.item_name = stock.item_name  WHERE item.item_name = '{}'""".format(name)
                try:
                    self.cursor.execute(sql)
                    ret = self.cursor.fetchall()
                    for x in ret:
                        name = x[0]
                        qty = x[1]

                        self.widget.tableWidget.setRowCount(0)
                        rows = self.widget.tableWidget.rowCount()
                        self.widget.tableWidget.insertRow(rows)
                        self.widget.tableWidget.setItem(rows,0,QtWidgets.QTableWidgetItem(name))
                        self.widget.tableWidget.setItem(rows,1,QtWidgets.QTableWidgetItem(str(qty)))
                        
                except Exception as aa:
                    print("XOXOX :: ",aa)

            else:
                print('Item Doesn\'t Exist')

    # Add Stock Quantity
    def add_stock(self):
        if self.widget.tableWidget.rowCount() != 0:
            qty = self.widget.spinBox.value()
            self.db = db.Database().connect_db()
            self.cursor = self.db.cursor()

            name = self.widget.tableWidget.item(0,0).text()
            querry = """SELECT stock_qty,item_name FROM "stock" WHERE item_name = '{}'""".format(name)
            try:
                a = self.cursor.execute(querry)
                n = self.cursor.fetchone()

                new_qty = n[0] + int(qty)

                s = pendulum.now()

                d_day = "{}-{}-{}".format(s.year,s.month,s.day)
                sql = """Update "stock" set stock_qty = '{}', stock_last_update = '{}' WHERE\
                    item_name = '{}'""".format(new_qty,d_day,name)

                self.cursor.execute(sql)
                self.db.commit()
                self.widget.tableWidget.setItem(0,1,QtWidgets.QTableWidgetItem(str(new_qty)))
                self.widget.spinBox.setValue(1)
            except Exception as a:
                print('Error updating stock -> '+str(a))
            
            #self.widget.spinBox.setValue(1)
            self.setAutoComplete()
            self.daddy.reload_stock()
        else:
            print("No Item Selected!")

    # Reduce Stock Quantity
    def tear_stock(self):

        if self.widget.tableWidget.rowCount() != 0:
            qty = self.widget.spinBox.value()
            self.db = db.Database().connect_db()
            self.cursor = self.db.cursor()

            name = self.widget.tableWidget.item(0,0).text()
            querry = """SELECT stock_qty,item_name FROM "stock" WHERE item_name = '{}'""".format(name)
            try:
                a = self.cursor.execute(querry)
                n = self.cursor.fetchone()

                if int(qty) > n[0]:
                    print("Quantity Availabele Less Than Quantity to Remove!")

                else:
                    new_qty = n[0] - int(qty)

                    s = pendulum.now()

                    d_day = "{}-{}-{}".format(s.year,s.month,s.day)
                    sql = """Update "stock" set stock_qty = '{}', stock_last_update = '{}' WHERE\
                        item_name = '{}'""".format(new_qty,d_day,name)

                    self.cursor.execute(sql)

                    if self.user[2] == 3:
                        self.db.commit()
                        self.widget.tableWidget.setItem(0,1,QtWidgets.QTableWidgetItem(str(new_qty)))
                        self.widget.spinBox.setValue(1)
                        self.close()
                    
                    else:
                        self.show_msg("Could not complete your request, login using a Database Administrator\n\
                            account to do this action or contact the system Administrator!")
                        self.db.rollback()
                        self.widget.spinBox.setValue(1)
                        self.close()

            except Exception as a:
                print('Error updating stock -> '+str(a))

            self.setAutoComplete()
            self.daddy.reload_stock()
        else:
            print("No Item Selected!")

    def clear_fields(self):
        self.widget.spinBox.setValue(1)
        self.widget.tableWidget.setRowCount(0)
        self.widget.searchLineEdit.setText("")

    def show_msg(self,msg):
        m = QtWidgets.QMessageBox()
        m.setText(msg)
        m.setWindowTitle('Error')
        m.setIcon(QtWidgets.QMessageBox.Warning)
        m.exec_()
                