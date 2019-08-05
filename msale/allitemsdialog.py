from PyQt5 import QtWidgets, QtCore, QtGui, uic

from msale.database import db

from msale.icons import resources

class AllItemsDialog(QtWidgets.QDialog):
    def __init__(self):

        """
        All items Window for the MS Point of sale software
        //Initialize dynamically the ui
        //set the icons not loaded dynamically by the UiLoader
        """
        QtWidgets.QDialog.__init__(self)
        
        self.widget = uic.loadUi("msale/forms/allitemsdialog.ui",self)
        self.widget.refreshBtn.setIcon(QtGui.QIcon(":/icons/reload_w.png"))

        self.widget.filterLineEdit.textChanged.connect(self.filter_input)
        self.widget.refreshBtn.clicked.connect(self.load_all_items)
        self.load_all_items()

        self.setWindowIcon(QtGui.QIcon(":/icons/icon.png"))

    def load_all_items(self):
        self.mydb = db.Database().connect_db()
        self.cursor = self.mydb.cursor()
        self.widget.tableWidget.setRowCount(0)

        sql = """SELECT item.item_name, item_sp FROM "item"\
            INNER JOIN "stock" ON "item".item_name = "stock".item_name"""

            
        try:
            self.cursor.execute(sql)
            ret = self.cursor.fetchall()
            g = 0
            r = len(ret)
            self.widget.tableWidget.setRowCount(r)

            for row in ret:
                name = row[0]
                sp = row[1]
                
                self.widget.tableWidget.setItem(g,0,QtWidgets.QTableWidgetItem(name))
                self.widget.tableWidget.setItem(g,1,QtWidgets.QTableWidgetItem(str(sp)))
                g+=1

        except Exception as aa:
            print('>> Error at All Items Window :: ',str(aa))

    def filter_input(self):
        if len(self.widget.filterLineEdit.text()) == 0:
            self.load_all_items()

        else:
            self.mydb = db.Database().connect_db()
            self.cursor = self.mydb.cursor()
            self.widget.tableWidget.setRowCount(0)

            searchText = self.widget.filterLineEdit.text()

            sql = """SELECT item.item_name, item_sp FROM "item"\
                INNER JOIN "stock" ON "item".item_name = "stock".item_name WHERE item.item_name ILIKE '%{}%'""".format(searchText)

            
            try:
                self.cursor.execute(sql)
                ret = self.cursor.fetchall()
                g = 0
                r = len(ret)
                self.widget.tableWidget.setRowCount(r)

                for row in ret:
                    name = row[0]
                    sp = row[1]
                    
                    self.widget.tableWidget.setItem(g,0,QtWidgets.QTableWidgetItem(name))
                    self.widget.tableWidget.setItem(g,1,QtWidgets.QTableWidgetItem(str(sp)))
                    g+=1

            except Exception as aa:
                print('>> Error at All Items Dialog :: ',str(aa))