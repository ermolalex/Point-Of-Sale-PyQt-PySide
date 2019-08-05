from PyQt5 import QtCore, QtGui, QtWidgets, uic

from msale.database import db
from msale.repaydialog import RepayDialog
from msale.newcreditee import NewCrediteeDialog

from msale.icons import resources

class CrediteeForm(QtWidgets.QWidget):
    def __init__(self,daddy,name,no,bal):
        QtWidgets.QWidget.__init__(self)
        self.daddy = daddy
        self.widget = uic.loadUi("msale/forms/crediteeform.ui",self)

        self.widget.editUserBtn.setIcon(QtGui.QIcon(":/icons/edit_user_w.png"))
        self.widget.deleteUserBtn.setIcon(QtGui.QIcon(":/icons/delete_user_w.png"))
        self.widget.userPicture.setIcon(QtGui.QIcon(":/icons/user_w.png"))
        self.widget.repayBtn.setIcon(QtGui.QIcon(":/icons/repay.png"))
        self.widget.cleardebtBtn.setIcon(QtGui.QIcon(":/icons/cleardebt.png"))

        self.widget.editUserBtn.clicked.connect(self.update_account)
        self.widget.deleteUserBtn.clicked.connect(self.delete_account)
        self.widget.repayBtn.clicked.connect(self.repay_debt)
        self.widget.cleardebtBtn.clicked.connect(self.waive_debt)
        self.setFields(name,no,bal)

    def setFields(self,name,no,bal):
        self.widget.fullNameLabel.setText(name)
        self.widget.mobileNoLabel.setText("0"+str(no))
        self.widget.roleLabel.setText(str(bal))

    def update_account(self):
        no = int(self.widget.mobileNoLabel.text())
        ui = NewCrediteeDialog(self)
        ui.populate(no)
        ui.exec_()
        self.daddy.load_crediteeaccounts()

    def delete_account(self):
        '''no = self.widget.mobileNoLabel.text()

        sql = """DELETE FROM "credit_person" WHERE cp_mobile_no = '{}'""".format(no)
        sql = """DELETE FROM "credit_person" WHERE cp_mobile_no = '{}'""".format(no)
        try:
            k = db.Database().connect_db()
            k.cursor().execute(sql)
            k.commit()
            self.daddy.load_accounts()
        
        except Exception as e:
            print(e)'''
        pass

    def repay_debt(self):
        ui = RepayDialog(self)
        ui.exec_()

    def waive_debt(self):
        pass

