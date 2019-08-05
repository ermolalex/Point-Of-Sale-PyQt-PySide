from PyQt5 import QtWidgets, QtCore, QtGui, uic
import os, pendulum
from msale.database import db
from msale.icons import resources

class NewItemForm(QtWidgets.QDialog):
    def __init__(self):

        """
        New Item Dialog for the MS Point of sale software
        //Initialize dynamically the ui
        //set the icons not loaded dynamically by the UiLoader
        //Setup slot functions for the signals sent by the dynamic Ui
        """
        QtWidgets.QDialog.__init__(self)
        
        self.widget = uic.loadUi("msale/forms/newitem.ui",self)
        self.setWindowIcon(QtGui.QIcon(":/icons/icon.png"))

        self.widget.saveItemBtn.clicked.connect(self.add_new_item)
        self.widget.clearFieldsBtn.clicked.connect(self.clear_fields)

    def clear_fields(self):
        self.widget.itemNameineEdit.setText("")
        self.widget.bpLineEdit.setText("")
        self.widget.splineEdit.setText("")
        self.widget.stockLineEdit.setText("")
        self.widget.companyLineEdit.setText("")

    def add_new_item(self):
        i_name = self.widget.itemNameineEdit.text()
        i_bp = self.widget.bpLineEdit.text()
        i_sp = self.widget.splineEdit.text()
        i_qty = self.widget.stockLineEdit.text()
        i_company = self.widget.companyLineEdit.text()

        if len(i_name) == 0 or len(i_bp) == 0 or len(i_sp) == 0 or len(i_qty) == 0:
            print('One of required field is empty')

        else:
            b = db.Database().check_if_exists('item','item_name',i_name)
            self.mydb = db.Database().connect_db()
            self.cursor = self.mydb.cursor()

            if b == True:
                print('An Item With a similar name already Exists in the database')
            
            else:
                a = pendulum.now()
                i_date = '{}-{}-{}'.format(a.year,a.month,a.day)
                sql = ''' INSERT INTO "item" (item_name,item_bp,item_sp,item_company)\
                    VALUES ('{}','{}','{}','{}')'''.format(i_name,float(i_bp),float(i_sp),i_company)
                sql1 = '''INSERT INTO "stock" (item_name,stock_qty,stock_last_update) \
                    VALUES ('{}','{}','{}')'''.format(i_name,int(i_qty),i_date)
                try:
                    self.cursor.execute(sql)
                    try:
                        self.cursor.execute(sql1)
                        self.mydb.commit()
                        self.display_added_to_table(i_name,i_bp,i_sp,i_qty,i_company)
                        self.clear_fields()

                    except Exception as b:
                        self.mydb.rollback()
                        print('Error2 : Changes Rollback\n'+str(b))
                        
                except Exception as b1:
                    self.mydb.rollback()
                    print('Error1 : Changes Rollback\n'+str(b1))
    
    def display_added_to_table(self,name,bp,sp,qty,c):
        row_at = self.widget.tableWidget.rowCount()
        self.widget.tableWidget.insertRow(row_at)

        self.widget.tableWidget.setItem(row_at,0,QtWidgets.QTableWidgetItem(name))
        self.widget.tableWidget.setItem(row_at,1,QtWidgets.QTableWidgetItem(bp))
        self.widget.tableWidget.setItem(row_at,2,QtWidgets.QTableWidgetItem(sp))
        self.widget.tableWidget.setItem(row_at,3,QtWidgets.QTableWidgetItem(qty))
        self.widget.tableWidget.setItem(row_at,4,QtWidgets.QTableWidgetItem(c))
