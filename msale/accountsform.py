from PyQt5 import QtCore, QtGui, QtWidgets, uic

from msale.database import db
from msale.userForm import UserForm
from msale.crediteeform import CrediteeForm
from msale.newcreditee import NewCrediteeDialog
from msale.newuserdialog import NewUserDialog
from msale.changepassworddialog import ChangePasswordDialog

from msale.icons import resources


class AccountsForm(QtWidgets.QWidget):
    def __init__(self,user,daddy):
        QtWidgets.QWidget.__init__(self)
        self.widget = uic.loadUi("msale/forms/accountsform.ui",self)
        self.user = user
        self.daddy = daddy

        self.widget.newAccountBtn.setIcon(QtGui.QIcon(":/icons/add_user_w.png"))
        self.widget.reloadAccountsBtn.setIcon(QtGui.QIcon(":/icons/reload_w.png"))
        self.widget.newcAccountBtn.setIcon(QtGui.QIcon(":/icons/add_user_w.png"))
        self.widget.reloadcAccountsBtn.setIcon(QtGui.QIcon(":/icons/reload_w.png"))

        self.widget.newcAccountBtn.clicked.connect(self.new_crediteeAccount)
        self.widget.reloadAccountsBtn.clicked.connect(self.load_accounts)
        self.widget.reloadcAccountsBtn.clicked.connect(self.load_crediteeaccounts)
        self.widget.newAccountBtn.clicked.connect(self.new_userAccount)
        self.widget.changepasswordBtn.clicked.connect(self.change_password)
        
        self.load_accounts()
        self.load_crediteeaccounts()

    def load_accounts(self):
        
        sql_user = """SELECT username, firstname, lastname, mobile_no, admin FROM "user" """
        
        cursor = db.Database().connect_db().cursor()

        try:
            cursor.execute(sql_user)
            ret2 = cursor.fetchall()

            self.widget.userTbl.setRowCount(0)
            rows = len(ret2)-2
            self.widget.userTbl.setRowCount(rows)

            i = 0
            for x in range(len(ret2)):
                uname = ret2[x][0]
                name = "{} {}".format(ret2[x][1], ret2[x][2])
                no =ret2[x][3]
                admin = ret2[x][4]

                if admin == 3:
                    continue

                else:
                    tile = UserForm(uname,name,no,admin,self,self.user,self.daddy)
                    self.widget.userTbl.setCellWidget(i,0,tile)
                    i= i+1

        except Exception as e:
            print(e)

    def load_crediteeaccounts(self):

        sql_user = """SELECT cp_firstname, cp_lastname, cp_mobile_no, cp_balance FROM "credit_person" """
        cursor = db.Database().connect_db().cursor()
        try:  
            cursor.execute(sql_user)
            ret2 = cursor.fetchall()

            self.widget.crediteeTbl.setRowCount(0)
            self.widget.crediteeTbl.setRowCount(len(ret2))

            for x in range(len(ret2)):
                name = "{} {}".format(ret2[x][0], ret2[x][1])
                no =ret2[x][2]
                bal = ret2[x][3]

                tile = CrediteeForm(self,name,no,bal)
                self.widget.crediteeTbl.setCellWidget(x,0,tile)

        except Exception as e:
            print(e)

    def new_crediteeAccount(self):
        ui = NewCrediteeDialog(self)
        ui.exec_()
        self.load_crediteeaccounts()

    def auto_complete(self):
        pass

    def new_userAccount(self):
        ui = NewUserDialog()
        ui.exec_()
        self.load_accounts()

    def change_password(self):
        ui = ChangePasswordDialog()
        ui.exec_()

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
