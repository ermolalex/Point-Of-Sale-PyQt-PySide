from PyQt5 import QtWidgets, QtCore, QtGui, uic

from msale.database import db
from msale.icons import resources

class ChangePasswordDialog(QtWidgets.QDialog):
    def __init__(self,):

        """
        Delete Window for the MS Point of sale software
        //Initialize dynamically the ui
        //set the icons not loaded dynamically by the UiLoader
        """
        QtWidgets.QDialog.__init__(self)
        
        self.widget = uic.loadUi("msale/forms/changepassword.ui",self)
        self.widget.pushButton_change.clicked.connect(self.change_password)

        self.setWindowIcon(QtGui.QIcon(":/icons/icon.png"))

    
    def setUsername(self,username):
        self.widget.lineEdit_username.setText(username)

    def change_password(self):

        self.db = db.Database().connect_db()
        self.cursor = self.db.cursor()

        un = self.widget.lineEdit_username.text()
        np = self.widget.lineEdit_new_pass.text()
        op = self.widget.lineEdit_old_password.text()
        np_ = self.widget.lineEdit_newpass_2.text()

        if len(un) > 4 and len(op) > 4 and len(np) > 4 and len(np_) > 4:

            ret1 = db.Database().check_if_exists("user","username",un)

            if ret1 == True:
                if np == np_:
                    ret2 = db.Login().login(un,op)

                    if ret2 == True:
                        psw = db.PasswordActions().hash_password(np)
                        sql = """ UPDATE "user" SET password = '{}' WHERE username = '{}'""".format(psw,un)
                        try:
                            self.cursor.execute(sql)
                            self.db.commit()
                            print(">> Password Changed Successfully")
                            self.message(">> Password Changed Successfully",0)
                            self.close()
                            
                        except Exception as a:
                            txt = ">> Error changing password :: "+str(a)
                            self.message(txt,1)

                    else:
                        txt = "Wrong login details"
                        self.message(txt,1)
                else:
                    txt = "Two New passwords do not match!"
                    self.message(txt,1)
            else:
                txt = "Unknown User!"
                self.message(txt,1)

        else:
            pr = "One of the required field is empty or short!"
            self.message(pr,1)

        self.db.close()

    def message(self,x,y):
        a = QtWidgets.QMessageBox()
        a.setText(x)
        a.setWindowTitle('Password Change')
        a.setIcon(QtWidgets.QMessageBox.Warning)
        a.setStyleSheet("font: 12px;")
        a.exec_()
