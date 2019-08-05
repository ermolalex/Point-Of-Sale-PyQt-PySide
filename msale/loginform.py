from PyQt5 import QtWidgets, QtCore, QtGui, uic

from msale.database import db
from msale.icons import resources

class LoginForm(QtWidgets.QMainWindow):
    def __init__(self,father):

        """
        Login Window for the MS Point of sale software
        Initialize dynamically the ui
        set the icons not loaded dynamically by the UiLoader
        """
        QtWidgets.QMainWindow.__init__(self)
        self.father = father

        # Load Ui
        self.widget = uic.loadUi("msale/forms/loginform.ui",self)

        self.widget.iconBtn.setIcon(QtGui.QIcon(":/icons/username_w.png"))
        self.widget.icon2Btn.setIcon(QtGui.QIcon(":/icons/key_w.png"))
        self.widget.loginBtn.setIcon(QtGui.QIcon(":/icons/unlock_w.png"))
        self.x = []
        self.widget.loginBtn.clicked.connect(self.login_account)

    def login_into(self):
        #open Dashboard if successful
        self.father.unset_login()
        self.father.setUser(self.x)

    def login_account(self):
        user_n = self.widget.usernameInput.text()
        pass_w = self.widget.passwordInput.text()

        if len(user_n) < 5:
            msg = 'Short Username Entered!\n Usernames are 5 characters or more in length'
            self.show_msg(msg)
        elif len(pass_w) < 5:
            msg = 'Short Password Entered!\n Passwords are 5 characters or more in length'
            self.show_msg(msg)
        else:
            b = db.Database().check_if_exists('user','username',user_n)
            if b == False:
                msg = 'Invalid Login Details'
                self.show_msg(msg)
            else:
                val = self.validate_(user_n)
                if val == True:
                    a = db.Login().login(user_n,pass_w)
                    if a == True:
                        sql_login = """SELECT firstname,lastname,admin FROM "user" WHERE username = '{}' """.format(user_n)
                        a = db.Database().connect_db()
                        b = a.cursor()
                        try:
                            b.execute(sql_login)
                            ret = b.fetchone()
                            self.x.append(user_n)
                            self.x.append(ret[0]+" "+ret[1])
                            self.x.append(ret[2])
                            
                            self.login_into()

                        except Exception as a_:
                            print("Error at Login ::",a_)
                    else:
                        msg = 'Invalid Login Details'
                        self.show_msg(msg)
                else:
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
        m.setWindowTitle('Error Logging In ')
        #icon = QtGui.QIcon()
        #icon.addPixmap(QtGui.QPixmap(":/icons/user.png"))
        #m.setWindowIcon(icon)
        m.setIcon(QtWidgets.QMessageBox.Warning)
        m.exec_()
            