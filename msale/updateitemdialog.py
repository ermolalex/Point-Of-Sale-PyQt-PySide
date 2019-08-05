from PyQt5 import QtWidgets, QtCore, QtGui, uic

from msale.database import db
from msale.authenticationdialog import AuthenticationDialog
from msale.icons import resources

class ItemUpdateDialog(QtWidgets.QDialog):
    def __init__(self,user):
        QtWidgets.QDialog.__init__(self)
        self.user = user
        self.widget = uic.loadUi("msale/forms/updateitemdialog.ui",self)

        self.widget.cancelBtn.clicked.connect(lambda:self.close())
        self.widget.updateItemBtn.clicked.connect(self.update_item)
        self.widget.addBtn.clicked.connect(self.add_item)
        self.widget.spLineEdit.textChanged.connect(self.changed)

        val = QtGui.QIntValidator()
        self.widget.bpLineEdit.setValidator(val)
        self.widget.spLineEdit.setValidator(val)

        self.possible_list = []
        self.setAutoComplete()

        self.priceChanged = False
        self.setWindowIcon(QtGui.QIcon(":/icons/icon.png"))

    
    def changed(self):
        self.priceChanged = True

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
    
    # Add the searched item to table
    def add_item(self):
        name = self.widget.searchLineEdit.text()
        if len(name) == 0:
            print('Empty Search Input Field!')
        
        else:
            a = db.Database().check_if_exists('item','item_name',name)
            if a == True:
                sql = """SELECT item_bp,item_sp,item_company \
                FROM "item" WHERE item_name = '{}'""".format(name)
                try:
                    self.cursor.execute(sql)
                    ret = self.cursor.fetchone()

                    bp = ret[0]
                    sp = ret[1]
                    company = ret[2]

                    self.widget.companyLineEdit.setText(company)
                    self.widget.spLineEdit.setText(str(sp))
                    self.widget.bpLineEdit.setText(str(bp))
                    self.widget.itemNameLineEdit.setText(name)
                        
                except Exception as aa:
                    print("XOXOX :: ",aa)

            else:
                print('Item Doesn\'t Exist')

    def clear_fields(self):
        self.widget.searchLineEdit.setText("")
        self.widget.companyLineEdit.setText("")
        self.widget.spLineEdit.setText("")
        self.widget.bpLineEdit.setText("")
        self.widget.itemNameLineEdit.setText("")
        self.priceChanged = False

    # Add Item To table
    def add_table_data(self,name):
        sql = """SELECT item_bp,item_sp,item_company \
           FROM "item" WHERE item_name = '{}'""".format(name)

        try:
            self.cursor.execute(sql)
            ret = self.cursor.fetchone()

            bp = ret[0]
            sp = ret[1]
            company = ret[2]

            rows = self.widget.tableWidget.rowCount()
            self.widget.tableWidget.insertRow(rows)

            self.widget.tableWidget.setItem(rows,0,QtWidgets.QTableWidgetItem(name))
            self.widget.tableWidget.setItem(rows,1,QtWidgets.QTableWidgetItem(str(bp)))
            self.widget.tableWidget.setItem(rows,2,QtWidgets.QTableWidgetItem(str(sp)))
            self.widget.tableWidget.setItem(rows,3,QtWidgets.QTableWidgetItem(company))
                        
        except Exception as aa:
            print("XOXOX :: ",aa)


    def update_item(self):
        o_name = self.widget.searchLineEdit.text()
        i_name = self.widget.itemNameLineEdit.text()
        i_bp = self.widget.bpLineEdit.text()
        i_sp = self.widget.spLineEdit.text()
        i_company = self.widget.companyLineEdit.text()

        if len(i_name) == 0 or len(i_bp) == 0 or len(i_sp) == 0 :
            print('One of required field is empty')

        else:
            if db.Database().check_if_exists('item','item_name',o_name) == True:
                self.mydb = db.Database().connect_db()
                self.cursor = self.mydb.cursor()

                sql = ''' UPDATE "item" SET item_name = '{}',item_bp = '{}',\
                    item_sp = '{}',item_company = '{}' WHERE item_name = '{}' \
                        '''.format(i_name,i_bp,i_sp,i_company,o_name)
                sql1 = '''UPDATE "stock" SET item_name = '{}' WHERE item_name = '{}' \
                    '''.format(i_name,o_name)
                sql2 = '''UPDATE "orders" SET item_name = '{}' WHERE item_name = '{}' \
                    '''.format(i_name,o_name)
                try:
                    self.cursor.execute(sql)
                    self.cursor.execute(sql1)
                    self.cursor.execute(sql2)

                    if self.user[2] == 3:
                        self.mydb.commit()
                        self.setAutoComplete()
                        self.add_table_data(i_name)
                        self.clear_fields()

                    else:
                        x = AuthenticationDialog(self)
                        x.setWindowTitle("Login As Database Administrator")
                        x.exec_()

                        ret = x.returnStatus()
                        ret1 = x.returnAdmin()

                        if (ret == True) and (ret1 == True):
                            self.mydb.commit()
                            self.setAutoComplete()
                            self.add_table_data(i_name)
                            self.clear_fields()
                            

                        else:
                            self.mydb.rollback()
                            self.show_msg("Change to Item Details can only be done by Database Administrators\nKindly contact your administrator for assistance ...")
                            self.clear_fields()
                    

                except Exception as f1:
                    self.mydb.rollback()
                    print('<<Error1 : Changes Rollback>>'+str(f1))

            else:
                print("\""+o_name+ "\" Doesn't Exist In Database")

    def show_msg(self,msg):
        m = QtWidgets.QMessageBox()
        m.setText(msg)
        m.setWindowTitle('Error')
        m.setIcon(QtWidgets.QMessageBox.Warning)
        m.exec_()
