from PyQt5 import QtWidgets, QtCore, QtGui, uic

from msale.database import db
from msale.icons import resources

class NewCrediteeDialog(QtWidgets.QDialog):
    def __init__(self,daddy):

        """
        """
        QtWidgets.QDialog.__init__(self)
        self.daddy = daddy
        
        self.widget = uic.loadUi("msale/forms/newcreditee.ui",self)
        self.setWindowIcon(QtGui.QIcon(":/icons/icon.png"))


        # Setup Icons
        self.widget.iconBtn.setIcon(QtGui.QIcon(":/icons/add_user_w.png"))
        self.widget.saveBtn.clicked.connect(self.save_new_creditee)
        self.widget.updateBtn.clicked.connect(self.update_creditee)
        self.widget.updateBtn.hide()

        val = QtGui.QIntValidator()
        self.widget.phonenoLE.setValidator(val)

        self.mobile = 0
    
    def save_new_creditee(self):
        # function to retrieve inputs, verify 
        # and save to database
        # credit_person: cp_mobile_no, cp_firstname,cp_lastname,cp_balance
        self.db = db.Database().connect_db()
        self.cursor = self.db.cursor()

        fname = self.widget.firstnameLE.text()
        lname = self.widget.lastnameLE.text()
        mobile_ = self.widget.phonenoLE.text()

        if len(fname) != 0 and len(lname) != 0:
            mobile = int("{}".format(mobile_))
            if len(str(mobile)) > 8:
                sql_creditee = """INSERT INTO "credit_person"(cp_mobile_no, cp_firstname,cp_lastname,cp_balance)\
                     VALUES('{}','{}','{}','{}')""".format(mobile,fname,lname,0)
        
                ret = db.Database().check_if_exists('credit_person','cp_mobile_no',mobile)

                if ret == False:
                    try:
                        self.cursor.execute(sql_creditee)
                        self.db.commit()

                        txt = "New creditee account saved successfully!"
                        
                        self.daddy.auto_complete()
                        self.close()

                    except Exception as a:
                        txt = "Error saving the user ::\n{}".format(str(a))
                        print(txt)
                else:
                    print("Another user exists with the same mobile number!")
            else:
                print("Mobile number entered is short!")
        else:
            print("One of the name field is empty!")

    def populate(self,no):
        
        self.mobile = int(no)

        cursor = db.Database().connect_db().cursor()

        sql = """SELECT cp_firstname,cp_lastname,cp_balance FROM "credit_person" WHERE cp_mobile_no = '{}'""".format(no)
        try:
            cursor.execute(sql)
            ret = cursor.fetchone()

            self.widget.firstnameLE.setText(ret[0])
            self.widget.lastnameLE.setText(ret[1])
            self.widget.phonenoLE.setText("0"+str(no))

            self.widget.saveBtn.hide()
            self.widget.updateBtn.show()

        except Exception as e:
            print(e)

    def update_creditee(self):

        fname = self.widget.firstnameLE.text()
        lname = self.widget.lastnameLE.text()
        mobile_ = self.widget.phonenoLE.text()

        sql = """ UPDATE "credit_person" SET cp_firstname='{}',\
            cp_lastname = '{}' WHERE cp_mobile_no='{}'""".format(fname,lname,self.mobile)
        sql1 = """ UPDATE "credit_person" SET cp_mobile_no='{}',cp_firstname='{}',\
            cp_lastname = '{}' WHERE cp_mobile_no='{}'""".format(mobile_,fname,lname,self.mobile)
        sql2 = """UPDATE "on_credit" SET cp_mobile_no='{}' WHERE \
            cp_mobile_no='{}'""".format(mobile_,self.mobile)
        sql3 = """UPDATE "debt_pay" SET cp_mobile_no='{}' WHERE \
            cp_mobile_no='{}'""".format(mobile_,self.mobile)
        sql4 = """UPDATE "debt" SET cp_mobile_no = '{}' WHERE \
            cp_mobile_no='{}'""".format(mobile_,self.mobile)

        self.db = db.Database().connect_db()
        self.cursor = self.db.cursor()

        if len(fname) != 0 and len(lname) != 0 and len(str(mobile_)) > 8:
            check = """SELECT count(cp_firstname) FROM "credit_person" \
                WHERE cp_mobile_no = '{}' AND cp_mobile_no != '{}' """.format(mobile_,self.mobile)
            try:
                if self.mobile != mobile_:
                    self.cursor.execute(check)
                    ret = self.cursor.fetchone()
                    if len(ret) == 0:
                        x_ = 0
                    else:
                        x_ = ret[0]

                    if x_ == 0:
                        self.cursor.execute(sql1)
                        self.cursor.execute(sql2)
                        self.cursor.execute(sql3)
                        self.cursor.execute(sql4)
                        self.db.commit()
                        print("Updated ...")
                        self.close()
                    else:
                        txt = "The New Phone Number already exists"
                        print(txt)

                else:
                    self.cursor.execute(sql)
                    self.db.commit()
                    print("Updated ...")
                    self.close()

            except Exception as a:
                txt = "Error saving the user ::\n{}".format(str(a))
                print(txt)

        else:
            print("One of the name field is empty or the mobile number is short!")

        