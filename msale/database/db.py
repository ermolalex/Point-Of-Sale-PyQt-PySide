import hashlib, sys, os, uuid, psycopg2
from PyQt5 import QtWidgets,QtGui

class Database():
    # Connect to PostGress Database
    def __init__(self):
        self.connect_db()

    def connect_db(self):
        self.connected = False
        try:
            self.connection = psycopg2.connect(host = "localhost",  database = "mysale", user = "postgres_mysale", password = "postgresdb_mysale")#"8a603eee84d94fe0b83b678e80f0eede")
            self.cursor = self.connection.cursor()
            self.connected = True
            self.create_tables()
            return self.connection

        except Exception as a:
            self.connected = False
            print(">> Error Creating Database Connection :: ",a)
            '''
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Database")
            txt = "Could not connect to db, try checking if:\n>> Database server has started\n>>Database login credentials are correct\n Error:: {}".format(a)
            msg.setText(txt)
            msg.exec_()
            '''

    def is_connected(self):
        # returns database connection status
        return self.connected

    def super_admin(self):
        y = PasswordActions()
        z = y.hash_password("E5HIQFSn")

        admin_ = PasswordActions()
        admin = admin_.hash_password("tenai1993")

        try:
            a = self.check_if_exists("user","username",'MySale')
            b = self.check_if_exists("user","username",'Admin')
            if a == True:
                pass

            else:
                sql = """INSERT INTO "user"(firstname,lastname,gender,mobile_no,username,password,admin) \
                    VALUES('Server','Admin',2,254711498039,'MySale','{}',3);""".format(z)
                self.cursor.execute(sql)
                self.connection.commit()

            if b == True:
                pass

            else:
                sql_admin = """INSERT INTO "user"(firstname,lastname,gender,mobile_no,username,password,admin) \
                    VALUES('Admin','Admin',2,254711498039,'Admin','{}',3);""".format(admin)
                self.cursor.execute(sql_admin)
                self.connection.commit()

        except Exception as a:
            print(">> Error at super user: "+str(a))

    def check_connection(self):
        return self.connected

    def reconnect(self):
        try:
            self.connection.close()
            self.connect_db()
            self.create_tables()
        except:
            self.connect_db()
            self.create_tables()

    def create_tables(self):
        if self.connected == True:
            try:
                self.cursor.execute('''
                BEGIN TRANSACTION;
                CREATE TABLE IF NOT EXISTS "user" (
                    username	TEXT NOT NULL UNIQUE,
                    firstname	TEXT NOT NULL,
                    lastname	TEXT NOT NULL,
                    mobile_no	BIGINT NOT NULL,
                    gender	INTEGER NOT NULL,
                    password	TEXT NOT NULL,
                    admin	INTEGER NOT NULL DEFAULT 0,
                    PRIMARY KEY(username)
                );
                CREATE TABLE IF NOT EXISTS "item" (
                    item_name	TEXT NOT NULL UNIQUE,
                    item_bp	REAL NOT NULL,
                    item_sp	REAL NOT NULL,
                    item_company	TEXT,
                    PRIMARY KEY("item_name")
                );
                CREATE TABLE IF NOT EXISTS "stock" (
                    id	SERIAL PRIMARY KEY,
                    item_name	TEXT NOT NULL,
                    stock_qty	INTEGER NOT NULL,
                    stock_last_update	DATE NOT NULL,
                    stock_supplier	TEXT
                );
                CREATE TABLE IF NOT EXISTS "orders" (
                    order_id	SERIAL PRIMARY KEY,
                    item_name	TEXT NOT NULL,
                    item_bp	REAL NOT NULL,
                    item_sp	REAL NOT NULL,
                    order_qty	INTEGER NOT NULL,
                    payment_by	TEXT NOT NULL,
                    timestamp_	TIMESTAMP NOT NULL,
                    order_date	DATE NOT NULL,
                    served_by	TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS "credit_person" (
                    cp_mobile_no	BIGINT NOT NULL,
                    cp_firstname	TEXT NOT NULL,
                    cp_lastname	TEXT,
                    cp_balance	REAL NOT NULL,
                    PRIMARY KEY("cp_mobile_no")
                );
                CREATE TABLE IF NOT EXISTS "on_mpesa"(
                    timestamp_	TIMESTAMP NOT NULL PRIMARY KEY,
                    date	DATE NOT NULL,
                    mpesa_id	VARCHAR(15) NOT NULL UNIQUE,
                    mpesa_amount	REAL NOT NULL
                );

                CREATE TABLE IF NOT EXISTS "on_cashmpesa"(
                    timestamp_	TIMESTAMP NOT NULL PRIMARY KEY,
                    date	DATE NOT NULL,
                    cash_paid REAL NOT NULL DEFAULT 0,
                    mpesa_id	VARCHAR(15) NOT NULL UNIQUE,
                    mpesa_amount	REAL NOT NULL
                );

                CREATE TABLE IF NOT EXISTS "on_credit" (
                    timestamp_	TIMESTAMP NOT NULL PRIMARY KEY,
                    date	DATE NOT NULL,
                    credit_cost	REAL NOT NULL,
                    cp_mobile_no	BIGINT NOT NULL,
                    FOREIGN KEY("cp_mobile_no") REFERENCES "credit_person"("cp_mobile_no")
                );
                CREATE TABLE IF NOT EXISTS "on_cheque" (
                    timestamp_	TIMESTAMP NOT NULL PRIMARY KEY,
                    date	DATE NOT NULL,
                    cheque_amount	REAL NOT NULL,
                    cheque_maturity_date	DATE NOT NULL
                );
                CREATE TABLE IF NOT EXISTS "on_cash" (
                    timestamp_	TIMESTAMP NOT NULL,
                    date	DATE NOT NULL,
                    cash_cost	REAL NOT NULL,
                    PRIMARY KEY("timestamp_")
                );
                CREATE TABLE IF NOT EXISTS "discount" (
                    date	DATE NOT NULL,
                    amount	REAL NOT NULL,
                    PRIMARY KEY("date")
                );
                CREATE TABLE IF NOT EXISTS "debt_pay" (
                    debt_pay_id   SERIAL NOT NULL PRIMARY KEY,
                    cp_mobile_no  BIGINT NOT NULL,
                    debt_pay_amount   REAL NOT NULL,
                    debt_pay_date DATE NOT NULL,
                    debt_balance REAL NOT NULL,
                    FOREIGN KEY("cp_mobile_no") REFERENCES "credit_person"("cp_mobile_no")
                );
                CREATE TABLE IF NOT EXISTS "debt" (
                    debt_id   SERIAL NOT NULL PRIMARY KEY,
                    cp_mobile_no  BIGINT NOT NULL,
                    debt_amount   REAL NOT NULL,
                    debt_day  DATE NOT NULL,
                    debt_due  DATE NOT NULL,
                    debt_balance REAL NOT NULL,
                    FOREIGN KEY("cp_mobile_no") REFERENCES "credit_person"("cp_mobile_no")
                );
                COMMIT;

                ''')
                self.connection.commit()
                self.super_admin()

            except Exception as e:
                print("Error Creating Tables :: "+str(e))
                
    def check_if_exists(self,table_x,col_x,var_x):
        try:
            sql = '''SELECT count(*) FROM "{}" WHERE "{}"= '{}' '''.format(table_x,col_x,var_x)
            self.cursor.execute(sql)
            ret = self.cursor.fetchall()
            if ret[0][0] == 0:
                return False
            else:
                return True
        except Exception as E:
            print('<< Error Checking if exists >> ',str(E))
            r = 4
            return r

class PasswordActions:
    def hash_password(self,password):
        salt = uuid.uuid4().hex
        return hashlib.sha256(salt.encode()+password.encode()).hexdigest()+':'+salt

    def check_password(self,hashed_password,user_password):
        password,salt = hashed_password.split(':')
        return password == hashlib.sha256(salt.encode()+user_password.encode()).hexdigest()

class Login:
    '''
    Handle all login activities
    '''
    def login(self,username,password):

        self.db = Database().connect_db()
        a1= PasswordActions()
        sql = """SELECT password,count(*) FROM "user" WHERE username = '{}' GROUP BY password""".format(username)

        try:
            self.cursor = self.db.cursor()
            self.cursor.execute(sql)
            ret = self.cursor.fetchone()
            if ret[0] == 1:
                return False
            else:
                b = a1.check_password(ret[0],password)
                return b

        except Exception as a:
            print('>> Error at Login :: '+str(a)+" >>")
