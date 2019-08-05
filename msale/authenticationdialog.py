from PyQt5 import QtWidgets, QtCore, QtGui, uic

from msale.database import db
from msale.icons import resources

class AuthenticationDialog(QtWidgets.QDialog):
    def __init__(self,daddy):

        """
        """
        QtWidgets.QDialog.__init__(self)
        self.daddy = daddy
        
        self.widget = uic.loadUi("msale/forms/authenticate.ui",self)
        self.widget.confirmBtn.clicked.connect(self.authenticate_login)
        self.authenticate = False
        self.isAdmin = False
        self.setWindowIcon(QtGui.QIcon(":/icons/icon.png"))


    def setUser(self,user):
        self.widget.usernameLE.setText(user)
        self.widget.usernameLE.setReadOnly(True)

    def authenticate_login(self):
        user_n = self.widget.usernameLE.text()
        pass_w = self.widget.passwordLE.text()

        self.cursor = db.Database().connect_db().cursor()

        if len(user_n) < 5:
            msg = 'Short Username Entered!\n Usernames are 5 characters or more in length'
            self.show_msg(msg)
        elif len(pass_w) < 5:
            msg = 'Short Password Entered!\n Passwords are 5 characters or more in length'
            self.show_msg(msg)
        else:
            val = self.validate_(user_n)
            if val == True:

                a = db.Login().login(user_n,pass_w)
                if a == True:
                    self.authenticate = True
                    sql__ = """SELECT admin FROM "user" WHERE username = '{}' """.format(user_n)
                    self.cursor.execute(sql__)
                    ret = self.cursor.fetchone()

                    if ret[0] == 3:
                        self.isAdmin = True

                    else:
                        self.isAdmin = False

                    self.close()
                
                else:
                    self.authenticate = False
                    msg = "Wrong login details, couldn't authenticate the action"
                    self.show_msg(msg)

                    self.close()

            else:
                self.authenticate = False
                msg = 'Invalid Character In The Username Field\nOnly letters, numbers, @, \nfullstop and underscore(_) are allowed'
                self.show_msg(msg)

    def validate_(self,x):
        for char in x:
            an = char.isalnum()
            if an == True:
                continue
            else:
                if char == '_':
                    continue
                elif char == '@':
                    continue
                elif char == '.':
                    continue
                else: 
                    return False
        return True

    def show_msg(self,msg):
        m = QtWidgets.QMessageBox()
        m.setText(msg)
        m.setWindowTitle('Error')
        m.setIcon(QtWidgets.QMessageBox.Warning)
        m.exec_()

    def returnStatus(self):
        return self.authenticate

    def returnAdmin(self):
        return self.isAdmin