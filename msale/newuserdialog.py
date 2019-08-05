from PyQt5 import QtWidgets, QtCore, QtGui, uic

from msale.database import db
from msale.icons import resources
from msale.authenticationdialog import AuthenticationDialog
from msale.changepassworddialog import ChangePasswordDialog

class NewUserDialog(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        
        self.widget = uic.loadUi("msale/forms/newuserdialog.ui",self)
        self.setWindowIcon(QtGui.QIcon(":/icons/icon.png"))


        self.widget.saveuserBtn.clicked.connect(self.save_new_acc)
        self.widget.updateuserBtn.clicked.connect(self.update_acc)
        self.widget.changepasswordBtn.clicked.connect(self.change_password)

        self.widget.updateuserBtn.hide()
        self.widget.changepasswordBtn.hide()

        val = QtGui.QIntValidator()
        self.widget.mobileLE.setValidator(val)

        self.username = ""


    def show_msg(self,msg):
        m = QtWidgets.QMessageBox()
        m.setText(msg)
        m.setStyleSheet("font: 12px;")
        m.setWindowTitle('Error')
        m.setIcon(QtWidgets.QMessageBox.Warning)
        m.exec_()

    def save_new_acc(self):

        self.db = db.Database().connect_db()
        self.cursor = self.db.cursor()

        if len(self.widget.fnameLE.text()) == 0:
            msg = 'Empty First Name Field'
            self.show_msg(msg)
        elif len(self.widget.lnameLE.text()) == 0:
            msg = 'Empty Last Name Field'
            self.show_msg(msg)
        elif len(self.widget.usernameLE.text()) < 5:
            msg = 'Short Username Field. It should be 5 characters or more'
            self.show_msg(msg)
        elif len(self.widget.mobileLE.text()) < 10:
            msg = 'Incomplete Mobile Number'
            self.show_msg(msg)
        elif len(self.widget.passLE.text()) < 5:
            msg = 'Short Password Field. It should be 5 characters or more'
            self.show_msg(msg)
        elif len(self.widget.confirmpassLE.text()) < 5:
            msg = 'Short username Field. It should be 5 characters or more'
            self.show_msg(msg)
            
        else:

            if self.widget.passLE.text() == self.widget.confirmpassLE.text():
                fname = self.widget.fnameLE.text()
                lname = self.widget.lnameLE.text()
                uname = self.widget.usernameLE.text()
                if self.widget.genderCbx.currentIndex() == 0:
                    g = 1
                else:
                    g = 0
                mb = self.widget.mobileLE.text()
                p = self.widget.passLE.text()
                psw = db.PasswordActions().hash_password(p)

                exist = db.Database().check_if_exists('user','username',uname)
                if exist == True:
                    msg = 'Another user exists with a similar username\nChoose a different username or login if you \nhave an account'
                    self.show_msg(msg)
                else:
                    sql = """INSERT INTO "user" (firstname,lastname,username,gender,mobile_no,password,admin) VALUES \
                        ('{}','{}','{}','{}','{}','{}',0)""".format(fname,lname,uname,g,mb,psw)
                    try:
                        self.cursor.execute(sql)
                        self.db.commit()
                        self.show_msg("Account Details Saved Successfully")
                        self.close()

                    except Exception as a:
                        self.show_msg("Error saving user ->"+str(a))
            else:
                msg = 'The two password fields do not match'
                self.show_msg(msg)

    def populate_inputs(self,u):
        # populate inputs
        self.db = db.Database().connect_db()
        self.cursor = self.db.cursor()

        sql = """SELECT firstname,lastname,gender,mobile_no FROM "user" WHERE username = '{}'""".format(u)
        try:
            self.cursor.execute(sql)
            ret = self.cursor.fetchone()

            self.widget.fnameLE.setText(ret[0])
            self.widget.lnameLE.setText(ret[1])
            self.widget.usernameLE.setText(u)
            mbl = "0{}".format(ret[3])
            self.widget.mobileLE.setText(mbl)
            if ret[2] == 0:
                self.widget.genderCbx.setCurrentIndex(1)
            else:
                self.widget.genderCbx.setCurrentIndex(0)

        except Exception as e:
            self.show_msg(str(e))
    
    def setUpdateAccount(self,username,daddy,user,father):
        self.username = username
        self.widget.saveuserBtn.hide()
        self.widget.changepasswordBtn.show()
        self.widget.updateuserBtn.show()
        self.widget.passLbl.hide()
        self.widget.cpassLbl.hide()
        self.widget.passLE.hide()
        self.widget.confirmpassLE.hide()
        self.user = user
        self.daddy = daddy
        self.father = father

        self.populate_inputs(username)

    def update_acc(self):
        self.db = db.Database().connect_db()
        self.cursor = self.db.cursor()

        if len(self.widget.fnameLE.text()) == 0:
            msg = 'Empty First Name Field'
            self.show_msg(msg)
        elif len(self.widget.lnameLE.text()) == 0:
            msg = 'Empty Last Name Field'
            self.show_msg(msg)
        elif len(self.widget.usernameLE.text()) < 5:
            msg = 'Short Username Field. It should be 5 characters or more'
            self.show_msg(msg)
        elif len(self.widget.mobileLE.text()) < 10:
            msg = 'Incomplete Mobile Number'
            self.show_msg(msg)
            
        else:
            fname = self.widget.fnameLE.text()
            lname = self.widget.lnameLE.text()
            uname = self.widget.usernameLE.text()
            if self.widget.genderCbx.currentIndex() == 0:
                g = 1
            else:
                g = 0
            mb = self.widget.mobileLE.text()
            
            # TODO authenticate before save

            sql = '''UPDATE "user" SET firstname = '{}',lastname = '{}',username = '{}',gender = '{}'\
                    ,mobile_no = '{}' WHERE username = '{}' '''.format(fname,lname,uname,g,mb,self.username)
            sql2 = '''UPDATE "orders" SET served_by = '{}' WHERE served_by = '{}' '''.format(uname,self.username)
            try:
                self.cursor.execute(sql)
                self.cursor.execute(sql2)

                _m = AuthenticationDialog(self)
                if self.user[0] == self.username:
                    _m.setUser(self.user[0])
                _m.exec()
                status = _m.returnStatus()
                
                if status == True:
                    self.db.commit()
                    self.close()
                    self.show_msg("Account Details Updated ...")

                    if self.user[0] == self.username:
                        self.updateUser(uname)
                else:
                    self.db.rollback()
                    self.close()
                    self.show_msg("The changes were not saved ...")

            except Exception as a:
                self.show_msg("Error Updating Account ->"+str(a))

    def change_password(self):
        ui = ChangePasswordDialog()
        ui.setUsername(self.username)
        ui.exec_()

    def updateUser(self,m):
        sql_login = """SELECT firstname,lastname,admin FROM "user" WHERE username = '{}' """.format(m)
        a = db.Database().connect_db()
        b = a.cursor()
        try:
            b.execute(sql_login)
            ret = b.fetchone()
            x = []
            x.append(m)
            x.append(ret[0]+" "+ret[1])
            x.append(ret[2])

            self.father.setNoUser()  
            self.father.setUser(x)

        except Exception as a_:
            print("Error at Login ::",a_)