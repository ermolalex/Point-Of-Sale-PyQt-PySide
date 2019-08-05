from PyQt5 import QtWidgets, QtCore, QtGui, uic

from msale.dialog import Dialog
from msale.database import db
from msale.updatestockdialog import StockUpdateDialog
from msale.icons import resources

class StockForm(QtWidgets.QWidget):
    def __init__(self,user):

        """
        Stock Window for the MS Point of sale software
        //Initialize dynamically the ui
        //set the icons not loaded dynamically by the UiLoader
        """
        QtWidgets.QWidget.__init__(self)
        self.user = user
        
        self.widget = uic.loadUi("msale/forms/stockform.ui",self)
        self.widget.stockTableWidget.setStyleSheet("QHeaderView::section{background-color:rgb(90,90,90);color:white;}")

        # Setup Icons
        self.widget.addStockBtn.setIcon(QtGui.QIcon(":/icons/add_stock_w.png"))
        self.widget.reduceStockBtn.setIcon(QtGui.QIcon(":/icons/remove_w.png"))
        self.widget.reloadStockBtn.setIcon(QtGui.QIcon(":/icons/reload_w.png"))

        self.load_stock()
        self.widget.addStockBtn.clicked.connect(self.add_stock)
        self.widget.reduceStockBtn.clicked.connect(self.reduce_stock)
        self.widget.reloadStockBtn.clicked.connect(self.reload_stock)
        self.widget.filterLineEdit.textChanged.connect(self.filter_stock)

    def load_stock(self):

        self.mydb = db.Database().connect_db()
        self.cursor = self.mydb.cursor()

        self.widget.stockTableWidget.setRowCount(0)

        sql_stock = """SELECT item.item_name, stock_qty, stock_last_update FROM "item"\
            INNER JOIN "stock" ON item.item_name=stock.item_name ORDER BY item.item_name DESC"""
        try:
            self.cursor.execute(sql_stock)
            ret = self.cursor.fetchall()
            g = 0
            r = len(ret)
            self.widget.stockTableWidget.setRowCount(r)

            for row in ret:
                name = row[0]
                qty = row[1]
                date = row[2]
                
                self.widget.stockTableWidget.setItem(g,0,QtWidgets.QTableWidgetItem(name))
                self.widget.stockTableWidget.setItem(g,1,QtWidgets.QTableWidgetItem(str(qty)))
                self.widget.stockTableWidget.setItem(g,2,QtWidgets.QTableWidgetItem(str(date)))
                g+=1

        except Exception as aa:
            print('>> Error at stock :: ',str(aa))

    def filter_stock(self):

        if len(self.widget.filterLineEdit.text()) == 0:
            self.load_stock()

        else:
            self.mydb = db.Database().connect_db()
            self.cursor = self.mydb.cursor()
            self.widget.stockTableWidget.setRowCount(0)

            searchText = self.widget.filterLineEdit.text()

            #sql_stock = """SELECT item.item_name, stock_qty, stock_last_update FROM "item"\
            #    INNER JOIN "stock" ON item.item_name=stock.item_name ORDER BY item.item_name DESC"""
            sql = """SELECT item.item_name, stock_qty, stock_last_update FROM "item"\
                INNER JOIN "stock" ON "item".item_name = "stock".item_name WHERE item.item_name ILIKE '%{}%'""".format(searchText)

            
            try:
                self.cursor.execute(sql)
                ret = self.cursor.fetchall()
                g = 0
                r = len(ret)
                self.widget.stockTableWidget.setRowCount(r)

                for row in ret:
                    name = row[0]
                    qty = row[1]
                    date = row[2]
                    
                    self.widget.stockTableWidget.setItem(g,0,QtWidgets.QTableWidgetItem(name))
                    self.widget.stockTableWidget.setItem(g,1,QtWidgets.QTableWidgetItem(str(qty)))
                    self.widget.stockTableWidget.setItem(g,2,QtWidgets.QTableWidgetItem(str(date)))
                    g+=1

            except Exception as aa:
                print('>> Error at stock :: ',str(aa))

    def reload_stock(self):
        self.load_stock()

    def add_stock(self):
        StockUpdateDialog("Add Stock","add",self,self.user).exec_()

    def reduce_stock(self):
        StockUpdateDialog("Reduce Stock","tear",self,self.user).exec_()