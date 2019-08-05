from PyQt5 import QtWidgets, QtCore, QtGui, uic

from msale.database import db
from msale.icons import resources
import pendulum


class RepayDialog(QtWidgets.QDialog):
    def __init__(self,daddy):

        """
        Repay Dialog for the MS Point of sale software
        //Initialize dynamically the ui
        //set the icons not loaded dynamically by the UiLoader
        """
        QtWidgets.QDialog.__init__(self)
        self.daddy = daddy
        
        self.widget = uic.loadUi("msale/forms/repay.ui",self)
        self.widget.repayBtn.clicked.connect(self.update_account_amount_paid)
        self.widget.costLbl.setText(self.daddy.roleLabel.text())

        val = QtGui.QIntValidator()
        self.widget.amountpaidLE.setValidator(val)

        self.setWindowIcon(QtGui.QIcon(":/icons/icon.png"))


    def update_account_amount_paid(self):
        # to update the account status but not commit
        # "debt_pay": debt_pay_id   SERIAL, cp_mobile_no  BIGINT, debt_pay_amount   REAL, debt_pay_date DATE, debt_balance REAL
        
        self.db = db.Database().connect_db()
        self.cursor = self.db.cursor()

        amnt_ = self.widget.amountpaidLE.text()
        mble = self.daddy.mobileNoLabel.text()

        if len(str(amnt_)) > 0:
            amnt = float(amnt_)
            if len(mble) > 7:
                if len(str(amnt)) != 0:
                    a = pendulum.now()
                    tday = "{}-{}-{}".format(a.year,a.month,a.day)
                    mobile = int(mble) ##

                    sql_get_bal = """ SELECT cp_balance FROM "credit_person" WHERE cp_mobile_no = '{}'""".format(mobile)
                    try:
                        self.cursor.execute(sql_get_bal)
                        ret = self.cursor.fetchone()
                        bal = ret[0]

                        if bal >= float(amnt):
                            new_balance = bal - amnt
                            sql_update_bal = """ UPDATE "credit_person" SET cp_balance = '{}' WHERE\
                            cp_mobile_no = '{}'""".format(new_balance,mobile)

                            sql_pay1 = """INSERT INTO "debt_pay"(cp_mobile_no, debt_pay_amount,debt_pay_date, debt_balance)\
                            VALUES('{}','{}','{}','{}') """.format(mobile,amnt,tday,new_balance)

                            try:
                                self.cursor.execute(sql_update_bal)
                                self.cursor.execute(sql_pay1)
                                self.daddy.roleLabel.setText(str(new_balance))
                                self.db.commit()
                                print(">> Record Updated Successfully... >>")
                                self.close()

                            except Exception as c:
                                print(">> Error updating debt records :: " + str(c) + " >>")
                                txt = " Error updating debt records :: "+ str(c) 
                                self.show_info(txt)

                        else:
                            print(">> Amount paid exceeds amount owed! >>")
                            txt = " Amount paid exceeds amount owed! "
                            self.show_info(txt)

                    except Exception as b:
                        print(">> Error fetching balance :: "+ str(b)+" >>")
                        txt = "Error fetching balance :: "+ str(b)
                        self.show_info(txt)

                else:
                    print(">> Amount field is empty! >>")
                    txt = "Amount field is empty! "
                    self.show_info(txt)
            else:
                print(">> No creditee selected yet! >>")
                txt = " No creditee selected yet! "
                self.show_info(txt)
        else:
            print(">> Amount field is empty! >>")
            txt = " Amount field is empty! "
            self.show_info(txt)

    def show_info(self,msg):
        a = QtWidgets.QMessageBox()
        a.setStyleSheet("font: 12px;")
        a.setIcon(QtWidgets.QMessageBox.Warning)
        a.setText(msg)
        a.exec_()
