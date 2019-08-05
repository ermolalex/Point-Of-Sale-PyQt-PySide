from PyQt5 import QtWidgets, QtCore, QtGui, uic

import pendulum
from msale.database import db
from msale.newcreditee import NewCrediteeDialog
from msale.icons import resources

class PaymentDialog(QtWidgets.QDialog):
    def __init__(self,table,totals,daddy,user):

        """
        """
        QtWidgets.QDialog.__init__(self)
        self.table = table
        self.daddy = daddy
        self.user = user
        
        self.widget = uic.loadUi("msale/forms/paymentdialog.ui",self)
        self.widget.totalsLbl.setText(str(totals))
        self.setWindowIcon(QtGui.QIcon(":/icons/icon.png"))


        # Setup Icons
        self.widget.comboBox.currentIndexChanged.connect(self.options)
        self.widget.stackedWidget.setCurrentIndex(0)
        self.widget.transactBtn.clicked.connect(self.complete_transaction)
        self.widget.newcrediteeBtn.clicked.connect(self.open_newcreditee)

        self.db = db.Database().connect_db()
        self.cursor = self.db.cursor()
        
        self.ls = []
        self.auto_complete()
        
        self.sum = totals

        self.widget.chequeDateEdit.setMinimumDate(QtCore.QDate(QtCore.QDate.currentDate()))
        self.widget.creditduedateDateEdit.setMinimumDate(QtCore.QDate(QtCore.QDate.currentDate()))
    

    def options(self):
        index = self.widget.comboBox.currentIndex()

        if index == 0:
            self.widget.stackedWidget.setCurrentIndex(0)

        elif index == 1:
            self.widget.stackedWidget.setCurrentIndex(1)

        elif index == 2:
            self.widget.stackedWidget.setCurrentIndex(2)

        else:
            self.widget.stackedWidget.setCurrentIndex(3)

    def complete_transaction(self):
        index = self.widget.comboBox.currentIndex()

        if index == 0:
            self.mpesa_payment()

        elif index == 1:
            self.cashmpesa_payment()

        elif index == 2:
            self.credit_payment()

        else:
            self.cheque_payment()
    
    def mpesa_payment(self):
        # complete an mpesa transaction
        # on_mpesa : timestamp_, date, mpesa_amount, mpesa_id

        self.db = db.Database().connect_db()
        self.cursor = self.db.cursor()

        self.s = False
        amount_paid_ = self.widget.mpesaAmountLineEdit.text()
        mpesa_code = self.widget.mpesaCodeLineEdit.text()
        #disc_ = 0.0

        if len(str(amount_paid_)) == 0:
            amount_paid = 0
        else:
            amount_paid = float(amount_paid_)

        if len(mpesa_code) > 9 and len(str(amount_paid_)) != 0:
            disc = 0.0
            if float(amount_paid) + disc == self.sum:
                # check if amount paid plus discount is equal to the cost

                tm = pendulum.now()
                tm_now = "{}-{}-{}".format(tm.year,tm.month,tm.day)

                rows = self.table.rowCount()
                for x in range(rows):
                    name = self.table.item(x,0).text()
                    sp = self.table.item(x,1).text()
                    qty = self.table.item(x,2).text()

                    get_bp = """SELECT item_bp FROM "item" WHERE item_name = '{}'""".format(name)
                    get_qty = """SELECT stock_qty FROM "stock" WHERE item_name = '{}'""".format(name)
                    try:
                        self.cursor.execute(get_bp)
                        get = self.cursor.fetchone()
                        bp = get[0]
                        self.cursor.execute(get_qty)
                        get_ = self.cursor.fetchone()
                        qty_ = get_[0]

                        orders_sql = """INSERT INTO "orders"(item_name,item_bp,item_sp,order_qty,payment_by,timestamp_,order_date,served_by)\
                            VALUES('{}','{}','{}','{}','{}','{}','{}','{}')""".format(name,bp,sp,qty,'mpesa',tm,tm_now,self.user[0])
                        stock_sql = """UPDATE "stock" SET stock_qty = '{}' WHERE item_name = '{}'""".format(qty_ - int(qty),name)

                        self.cursor.execute(orders_sql)
                        self.cursor.execute(stock_sql)
                        self.s = True

                    except Exception as a:
                        self.success = False
                        self.s = False
                        self.message(">> Error saving to on_mpesa table",str(a))

                if self.s == True:
                    try:
                        # update/ insert amount discount figures into db
                        # insert on_mpesa data into db
                        
                        disc = 0

                        on_mpesa_sql = """INSERT INTO "on_mpesa"(timestamp_,date,mpesa_amount,mpesa_id) \
                            VALUES('{}','{}','{}','{}')""".format(tm,tm_now,amount_paid,mpesa_code)
                        a = db.Database().check_if_exists('discount','date',tm_now)

                        if a== False:
                            d_sql = """INSERT INTO "discount"(date,amount) VALUES('{}','{}')""".format(tm_now,disc)
                            
                        else:
                            get_val = """SELECT amount FROM "discount" WHERE date = '{}'""".format(tm_now)
                            self.cursor.execute(get_val)
                            r_ = self.cursor.fetchone()
                            n_amnt = r_[0] + disc
                            d_sql = """UPDATE "discount" SET amount = '{}' WHERE date = '{}'""".format(n_amnt,tm_now)

                        self.cursor.execute(on_mpesa_sql)
                        self.cursor.execute(d_sql)
                        self.db.commit()
                        self.success = True

                        print(">> Saved to mpesa table Successfuly >>")
                        self.daddy.clear_all()
                        self.close()

                    except Exception as b:
                        self.db.rollback()
                        self.success = False
                        self.message(">> Write Failed, mpesa operation rollback :: ",str(b))
            else:
                self.message("Amount Paid is not equal to the total cost!"\
                    ,"M-Pesa amount paid should be equal to total cost of the items")
        else:
            self.message("Amount field is empty or M-Pesa Code is short","M-Pesa codes are 10 digits long")

        self.db.close()

    def cashmpesa_payment(self):
        # complete an cash-mpesa transaction
        # on_cashmpesa : timestamp_, date, cash_paid, mpesa_amount, mpesa_id

        self.db = db.Database().connect_db()
        self.cursor = self.db.cursor()

        self.s = False
        cash_paid_ = self.widget.mcCashAmountLineEdit.text()
        amount_paid_ = self.widget.mcMpesaAmountLineEdit.text()
        mpesa_code = self.widget.mcMpesaCodeLineEdit.text()

        if len(str(amount_paid_)) == 0:
            amount_paid = 0
        else:
            amount_paid = float(amount_paid_)

        if len(str(cash_paid_)) == 0:
            cash_paid = 0
        else:
            cash_paid = float(cash_paid_)

        if len(mpesa_code) > 9 and len(str(amount_paid_)) != 0:
            disc = 0.0
            if float(amount_paid) + disc + cash_paid == self.sum:
                # check if amount paid plus discount is equal to the cost

                tm = pendulum.now()
                tm_now = "{}-{}-{}".format(tm.year,tm.month,tm.day)

                rows = self.table.rowCount()
                for x in range(rows):
                    name = self.table.item(x,0).text()
                    sp = self.table.item(x,1).text()
                    qty = self.table.item(x,2).text()

                    get_bp = """SELECT item_bp FROM "item" WHERE item_name = '{}'""".format(name)
                    get_qty = """SELECT stock_qty FROM "stock" WHERE item_name = '{}'""".format(name)
                    try:
                        self.cursor.execute(get_bp)
                        get = self.cursor.fetchone()
                        bp = get[0]
                        self.cursor.execute(get_qty)
                        get_ = self.cursor.fetchone()
                        qty_ = get_[0]

                        orders_sql = """INSERT INTO "orders"(item_name,item_bp,item_sp,order_qty,payment_by,timestamp_,order_date,served_by)\
                            VALUES('{}','{}','{}','{}','{}','{}','{}','{}')""".format(name,bp,sp,qty,'cashmpesa',tm,tm_now,self.user[0])
                        stock_sql = """UPDATE "stock" SET stock_qty = '{}' WHERE item_name = '{}'""".format(qty_ - int(qty),name)

                        self.cursor.execute(orders_sql)
                        self.cursor.execute(stock_sql)
                        self.s = True

                    except Exception as a:
                        self.success = False
                        self.s = False
                        self.message(">> Error saving to on_cashmpesa table",str(a))

                if self.s == True:
                    try:
                        # update/ insert amount discount figures into db
                        # insert on_cashmpesa data into db
                        
                        disc = 0
                        on_mpesa_sql = """INSERT INTO "on_cashmpesa"(timestamp_,date,cash_paid,mpesa_amount,mpesa_id) \
                            VALUES('{}','{}','{}','{}','{}')""".format(tm,tm_now,cash_paid,amount_paid,mpesa_code)
                        a = db.Database().check_if_exists('discount','date',tm_now)

                        if a== False:
                            d_sql = """INSERT INTO "discount"(date,amount) VALUES('{}','{}')""".format(tm_now,disc)
                            
                        else:
                            get_val = """SELECT amount FROM "discount" WHERE date = '{}'""".format(tm_now)
                            self.cursor.execute(get_val)
                            r_ = self.cursor.fetchone()
                            n_amnt = r_[0] + disc
                            d_sql = """UPDATE "discount" SET amount = '{}' WHERE date = '{}'""".format(n_amnt,tm_now)

                        self.cursor.execute(on_mpesa_sql)
                        self.cursor.execute(d_sql)
                        self.db.commit()
                        self.success = True

                        print(">> Saved to cashmpesa table Successfuly >>")
                        self.daddy.clear_all()
                        self.close()

                    except Exception as b:
                        self.db.rollback()
                        self.success = False
                        self.message(">> Write Failed, cash-mpesa operation rollback :: ",str(b))
            else:
                self.message("M-Pesa Amount Paid + Cash Paid is not equal to the total cost!"\
                    ,"M-Pesa amount + Cash Paid paid should be equal to total cost of the items")
        else:
            self.message("M-Pesa Amount field is empty or M-Pesa Code is short","M-Pesa codes are 10 digits long")

        self.db.close()

    def credit_payment(self):
        #complete credit Transaction
        # orders table: item_name, bp,sp, order_qty, payment_by, timestamp_,order_date, served-by
        # on_credit : timestamp_, credit_cost, cp_mobile_no,date
        # debt : cp_mobile_no, debt_amount, debt_day, debt_due,debt_balance
        self.db = db.Database().connect_db()
        self.cursor = self.db.cursor()

        creditee_name = self.widget.crediteenameLineEdit.text()
        credit_amount = self.widget.amountpaidSpinBox.value()
        debt_pay = float(credit_amount)

        _a = self.widget.creditduedateDateEdit.date()
        credit_due_date = "{}-{}-{}".format(_a.year(),_a.month(),_a.day())

        self.s = False
        tm = pendulum.now()
        tm_now = "{}-{}-{}".format(tm.year,tm.month,tm.day)

        if len(creditee_name) > 10:
            if credit_due_date >= tm_now:
                rows = self.table.rowCount()
                for x in range(rows):
                    name = self.table.item(x,0).text()
                    sp = self.table.item(x,1).text()
                    qty = self.table.item(x,2).text()

                    get_bp = """SELECT item_bp FROM "item" WHERE item_name = '{}'""".format(name)
                    get_qty = """SELECT stock_qty FROM "stock" WHERE item_name = '{}'""".format(name)
                    try:
                        self.cursor.execute(get_bp)
                        get = self.cursor.fetchone()
                        bp = get[0]
                        self.cursor.execute(get_qty)
                        get_ = self.cursor.fetchone()
                        qty_ = get_[0]

                        orders_sql = """INSERT INTO "orders"(item_name,item_bp,item_sp,order_qty,payment_by,timestamp_,order_date,served_by)\
                            VALUES('{}','{}','{}','{}','{}','{}','{}','{}')""".format(name,bp,sp,qty,'credit',tm,tm_now,self.user[0])
                        stock_sql = """UPDATE "stock" SET stock_qty = '{}' WHERE item_name = '{}'""".format(qty_ - int(qty),name)

                        self.cursor.execute(orders_sql)
                        self.cursor.execute(stock_sql)
                        self.s = True

                    except Exception as a:
                        self.s = False
                        self.success = False
                        self.message(">> Error saving to on_credit table ",str(a))

                if self.s == True:
                    try:
                        # update/ insert amount discount figures into db
                        # insert on_credit data into db
                        a,b = creditee_name.split('+')

                        get_bal_sql = """ SELECT cp_balance from "credit_person" WHERE cp_mobile_no = '{}'""".format(int(b))

                        self.cursor.execute(get_bal_sql)
                        ret = self.cursor.fetchone()

                        dbt_bal = self.sum - debt_pay
                        dbt_bal_ = dbt_bal + ret[0]

                        on_credit_sql = """INSERT INTO "on_credit"(timestamp_,date,credit_cost, cp_mobile_no) \
                            VALUES('{}','{}','{}','{}')""".format(tm,tm_now,self.sum,int(b))

                        on_debt_sql = """INSERT INTO "debt"(cp_mobile_no, debt_amount, debt_day, debt_due,debt_balance) \
                            VALUES('{}','{}','{}','{}','{}') """.format(int(b),self.sum,tm_now,credit_due_date,dbt_bal)

                        set_bal_sql = """UPDATE "credit_person" SET cp_balance = '{}' WHERE cp_mobile_no = '{}'""".format(dbt_bal_,int(b))

                        sql_pay = """INSERT INTO "debt_pay"(cp_mobile_no,debt_pay_amount,debt_pay_date, debt_balance) \
                            VALUES('{}','{}','{}','{}')""".format(int(b),debt_pay,tm_now,dbt_bal)

                        try:
                            self.cursor.execute(on_debt_sql)
                            self.cursor.execute(on_credit_sql)
                            self.cursor.execute(set_bal_sql)
                            if debt_pay > 0:
                                self.cursor.execute(sql_pay)
                                
                            self.db.commit()
                            self.success = True
                            print(">> Saved to credit table Successfuly >>")
                            self.daddy.clear_all()
                            self.close()

                        except Exception as f:
                            self.success = False
                            self.db.rollback()
                            self.message(">> Write Failed [E01], credit operation rollback :: ",str(f))

                    except Exception as b:
                        self.success = False
                        self.db.rollback()
                        self.message(">> Write Failed [E002], credit operation rollback :: ",str(b))
            else:
                self.message(">> Due date cant be in the past >>","Select a date greater or equal to today")
        else:
            self.message(">> Creditee Name is Empty! >>","")
        
        self.db.close()

    def open_newcreditee(self):
        # open create new creditee account
        
        new = NewCrediteeDialog(self)
        new.exec_()
    
    def auto_complete(self):
        # load completer
        self.cursor = db.Database().connect_db().cursor()
        self.ls.clear()

        sql_load = """SELECT cp_mobile_no, cp_firstname, cp_lastname FROM "credit_person" """

        try:
            self.cursor.execute(sql_load)
            ret = self.cursor.fetchall()

            for row in ret:
                mble = row[0]
                fname = row[1]
                lname = row[2]

                # make string to display in the list widget
                word = "{} {} : +{}".format(fname, lname, mble)
                self.ls.append(word)

            compl = QtWidgets.QCompleter(self.ls)
            compl.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
            compl.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
            self.widget.crediteenameLineEdit.setCompleter(compl)

        except Exception as a:
            print('Error Adding to list : ==>',a)

    def cheque_payment(self):
        # complete a cheque transaction
        # complete an cheque transaction
        # on_cheque : timestamp_, date, cheque_amount, cheque_maturity_date

        self.db = db.Database().connect_db()
        self.cursor = self.db.cursor()

        self.s = False
        amount_paid_ = self.widget.chequeamountLineEdit.text()

        if len(str(amount_paid_)) == 0:
            amount_paid = 0
        else:
            amount_paid = float(amount_paid_)

        tm = pendulum.now() # get date today
        tm_now = "{}-{}-{}".format(tm.year,tm.month,tm.day)

        a = self.widget.chequeDateEdit.date()
        mdate = "{}-{}-{}".format(a.year(),a.month(),a.day())

        if len(str(self.widget.chequeamountLineEdit.text())) != 0:
            if amount_paid >= self.sum:
                if mdate >= tm_now:
                    rows = self.table.rowCount()
                    for x in range(rows):
                        name = self.table.item(x,0).text()
                        sp = self.table.item(x,1).text()
                        qty = self.table.item(x,2).text()

                        get_bp = """SELECT item_bp FROM "item" WHERE item_name = '{}'""".format(name)
                        get_qty = """SELECT stock_qty FROM "stock" WHERE item_name = '{}'""".format(name)
                        try:
                            self.cursor.execute(get_bp)
                            get = self.cursor.fetchone()
                            bp = get[0]
                            self.cursor.execute(get_qty)
                            get_ = self.cursor.fetchone()
                            qty_ = get_[0]

                            orders_sql = """INSERT INTO "orders"(item_name,item_bp,item_sp,order_qty,payment_by,timestamp_,order_date,served_by)\
                                VALUES('{}','{}','{}','{}','{}','{}','{}','{}')""".format(name,bp,sp,qty,'cheque',tm,tm_now,self.user[0])
                            stock_sql = """UPDATE "stock" SET stock_qty = '{}' WHERE item_name = '{}'""".format(qty_ - int(qty),name)

                            self.cursor.execute(orders_sql)
                            self.cursor.execute(stock_sql)
                            self.s = True

                        except Exception as a:
                            self.success = False
                            self.s = False
                            self.message(">> Error saving to on_cheque",a)

                    if self.s == True:
                        try:
                            # update/ insert amount discount figures into db
                            # insert on_cheque data into db
        
                            on_cheque_sql = """INSERT INTO "on_cheque"(timestamp_,date,cheque_amount,cheque_maturity_date) \
                                VALUES('{}','{}','{}','{}')""".format(tm,tm_now,amount_paid,mdate)
                        
                            self.cursor.execute(on_cheque_sql)
                            self.db.commit()
                            self.success = True

                            print(">> Saved to cheque table Successfuly >>")
                            self.daddy.clear_all()
                            self.close()

                        except Exception as b:
                            self.db.rollback()
                            self.success = False
                            self.message(">> Write to cheque table Failed, cheque operation rollback",b)
                else:
                    self.message("Cheque Maturity Date Cant be in the past","Select a date greater or equal to today")
            else:
                self.message("Amount paid is not sufficient to complete transaction",">> Amount entered is less than total cost")
        else:
            self.message(">> Amount field is empty","")
        
        self.db.close()

    def message(self,x,y):
        msg = QtWidgets.QMessageBox()
        msg.setText(x)
        msg.setStyleSheet("font:12pt")
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        #msg.setWindowIcon(QtGui.QIcon(":/icons/shopping.png"))
        msg.setInformativeText(y)
        msg.setWindowTitle("Error")
        msg.exec_()