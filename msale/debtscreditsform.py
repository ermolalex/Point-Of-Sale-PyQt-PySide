from PyQt5 import QtWidgets, QtCore, QtGui, uic

from msale.database import db
import pendulum
from msale.newcreditee import NewCrediteeDialog
from msale.crediteewidget import CrediteeWidget
from msale.debtsdialog import DebtsDialog


class CreditsForm(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        """
        Credits And Debts Window for the MS Point of sale software
        //Initialize dynamically the ui
        //set the icons not loaded dynamically by the UiLoader
        //Setup slot functions for the signals sent by the dynamic Ui
        """
        QtWidgets.QWidget.__init__(self)
        
        self.widget = uic.loadUi("msale/forms/creditsform.ui",self)

        self.db = db.Database().connect_db()
        self.cursor = self.db.cursor()

        self.widget.viewcredititemsBtn.clicked.connect(self.open_view_details) # on_clicked
        self.widget.pushButton_credit_pay_update.clicked.connect(self.update_account_amount_paid) # on_clicked
        self.widget.pushButton_credits_back.clicked.connect(self.go_back_to_tab1)
        self.widget.pushButton_credits_new_creditee.clicked.connect(self.open_new_creditee) # on_clicked
        self.load_creditees()

        self.widget.stackedWidget.setCurrentIndex(0)

    def load_creditees(self):
        # open database read all creditess and add them to the table
        
        sql_load = """SELECT cp_mobile_no, cp_firstname, cp_lastname FROM "credit_person" """
        
        self.db = db.Database().connect_db()
        self.cursor = self.db.cursor()

        try:
            self.cursor.execute(sql_load)
            ret = self.cursor.fetchall()

            for row in ret:
                mble = row[0]
                fname = row[1]
                lname = row[2]

                # make string to display in the list widget

                name = "{} {}".format(fname, lname)
                widgt = CrediteeWidget(self,name,mble)

                x = QtWidgets.QListWidgetItem() 
                x.setSizeHint(QtCore.QSize(x.sizeHint().width(),62))
                self.widget.listWidget_all_creditees.addItem(x)
                self.widget.listWidget_all_creditees.setItemWidget(x,widgt)

        except Exception as a:
            print('Error Adding to list',a)

    def open_new_creditee(self):
        # register new creditee account
        a = NewCrediteeDialog(self)
        a.exec_()

        self.widget.listWidget_all_creditees.clear()
        self.load_creditees()
    
    def auto_complete(self):
        pass

    def open_creditee_items(self):
        # to open the view details tab
        
        self.widget.groupBox_credits_admin.hide()
        self.widget.stackedWidget.setCurrentIndex(1)

    def open_user(self,mobile):
        self.widget.lineEdit_credit_details_mobile.setText(mobile)
        self.load_debt_paid(mobile)
        self.widget.stackedWidget.setCurrentIndex(1)


    def load_debt_paid(self, mobile):
        # load debt data and payments done
        '''
        "debt_pay": debt_pay_id   SERIAL, cp_mobile_no  BIGINT, debt_pay_amount   REAL, debt_pay_date DATE, debt_balance REAL
        "debt": debt_id   SERIAL, cp_mobile_no  BIGINT, debt_amount   REAL, debt_day  DATE, debt_due  DATE, debt_balance REAL
        '''

        self.db = db.Database().connect_db()
        self.cursor = self.db.cursor()

        sql_debt = """SELECT debt_amount, debt_day, debt_due,debt_balance FROM "debt" \
          WHERE cp_mobile_no = '{}' """.format(mobile)
        sql_pay = """SELECT debt_pay_amount, debt_pay_date, debt_balance FROM "debt_pay" WHERE \
          cp_mobile_no = '{}' """.format(mobile)

        self.tableWidget_pay_debt_details_3.setRowCount(0)
        self.widget.tableWidget_pay_debt_details_2.setRowCount(0)

        try:
            self.cursor.execute(sql_debt)
            ret = self.cursor.fetchall()

            self.cursor.execute(sql_pay)
            ret1 = self.cursor.fetchall()

            # debt table
            for row in ret:
                d_amnt = row[0]
                d_day = row[1]
                d_due = row[2]
                d_bal = row[3]

                r = self.tableWidget_pay_debt_details_3.rowCount()
                self.tableWidget_pay_debt_details_3.insertRow(r)
                self.tableWidget_pay_debt_details_3.setItem(r,0,QtWidgets.QTableWidgetItem(str(d_bal)))
                self.tableWidget_pay_debt_details_3.setItem(r,1,QtWidgets.QTableWidgetItem(str(d_amnt)))
                self.tableWidget_pay_debt_details_3.setItem(r,2,QtWidgets.QTableWidgetItem(str(d_day)))
                self.tableWidget_pay_debt_details_3.setItem(r,3,QtWidgets.QTableWidgetItem(str(d_due)))

            # payments table
            for row in ret1:
                dp_amnt = row[0]
                dp_day = row[1]
                dp_bal = row[2]

                s = self.widget.tableWidget_pay_debt_details_2.rowCount()
                self.widget.tableWidget_pay_debt_details_2.insertRow(s)
                self.widget.tableWidget_pay_debt_details_2.setItem(s,0,QtWidgets.QTableWidgetItem(str(dp_bal)))
                self.widget.tableWidget_pay_debt_details_2.setItem(s,1,QtWidgets.QTableWidgetItem(str(dp_amnt)))
                self.widget.tableWidget_pay_debt_details_2.setItem(s,2,QtWidgets.QTableWidgetItem(str(dp_day)))
            
        except Exception as a:
            print(a)

    def open_view_details(self):
        # show all taken items
        mobile = self.lineEdit_credit_details_mobile.text()
        mble = mobile
        debt_items = DebtsDialog(mble)
        debt_items.exec_()

    def update_account_amount_paid(self):
        # to update the account status but not commit
        # "debt_pay": debt_pay_id   SERIAL, cp_mobile_no  BIGINT, debt_pay_amount   REAL, debt_pay_date DATE, debt_balance REAL
        
        self.db = db.Database().connect_db()
        self.cursor = self.db.cursor()

        amnt_ = self.widget.lineEdit_credit_pay_amount.text()
        mble = self.widget.lineEdit_credit_details_mobile.text()

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
                                self.db.commit()
                                self.widget.lineEdit_credit_pay_amount.setText("")

                                print(">> Record Updated Successfully... >>")
                                self.load_debt_paid(mobile)

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

    def go_back_to_tab1(self):
        # close current tab and goes to 1st tab
        self.widget.stackedWidget.setCurrentIndex(0)

    def show_info(self,msg):
        a = QtWidgets.QMessageBox()
        a.setStyleSheet("font: 12px;")
        a.setIcon(QtWidgets.QMessageBox.Warning)
        a.setText(msg)
        a.exec_()