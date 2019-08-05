from PyQt5 import QtCore, QtGui, QtWidgets, uic

from msale.newuserdialog import NewUserDialog
from msale.database import db
from msale.icons import resources

class UserForm(QtWidgets.QWidget):
    def __init__(self,uname,name,no,admin,daddy,user,father):
        QtWidgets.QWidget.__init__(self)
        self.daddy = daddy
        self.father = father
        self.user = user
        self.widget = uic.loadUi("msale/forms/userform.ui",self)

        self.widget.editUserBtn.setIcon(QtGui.QIcon(":/icons/edit_user_w.png"))
        self.widget.deleteUserBtn.setIcon(QtGui.QIcon(":/icons/delete_user_w.png"))
        self.widget.userPicture.setIcon(QtGui.QIcon(":/icons/user_w.png"))

        self.widget.editUserBtn.clicked.connect(self.update_account)
        self.widget.deleteUserBtn.clicked.connect(self.delete_account)

        self.setFields(uname,name,no,admin)

    def setFields(self,uname,name,no,admin):

        if admin == 0:
            status = "Teller"
        elif admin == 1:
            status = "Admin"
        else:
            status = "Database Admin"
            
        self.widget.fullNameLabel.setText(name)
        self.widget.usernameLabel.setText(uname)
        self.widget.mobileNoLabel.setText("0"+str(no))
        self.widget.roleLabel.setText(status)

    def update_account(self):
        user = self.widget.usernameLabel.text()
        ui = NewUserDialog()
        ui.setUpdateAccount(user,self,self.user,self.father)
        ui.exec_()
        self.daddy.load_accounts()
        

    def delete_account(self):
        user = self.widget.usernameLabel.text()

        sql = """DELETE FROM "user" WHERE username = '{}'""".format(user)
        try:
            k = db.Database().connect_db()
            k.cursor().execute(sql)

            if self.user[0] == user:
                #Authenticate
                self.show_msg("Can't delete this account, user is currently logged in!\nSwitch user then try again.")
            
            elif self.user[2] == 3:
                k.commit()
                self.daddy.load_accounts()

            else:
                self.show_msg("Can't delete this account, the action can be done by Database \
                    Administrators only, switch to such account or contact database administrator")
        
        except Exception as e:
            print(e)

    def show_msg(self,msg):
        m = QtWidgets.QMessageBox()
        m.setText(msg)
        m.setWindowTitle('Error')
        m.setIcon(QtWidgets.QMessageBox.Warning)
        m.exec_()