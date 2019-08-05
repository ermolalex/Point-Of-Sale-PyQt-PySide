from PyQt5 import QtWidgets, QtCore, QtGui, uic

from msale.database import db
from msale.deletebtnform import DeleteBtn
from msale.icons import resources

class DeleteDialog(QtWidgets.QDialog):
    def __init__(self,user):

        """
        Delete Window for the MS Point of sale software
        //Initialize dynamically the ui
        //set the icons not loaded dynamically by the UiLoader
        """
        QtWidgets.QDialog.__init__(self)
        self.user = user
        
        self.widget = uic.loadUi("msale/forms/deletedialog.ui",self)
        self.widget.tableWidget.setColumnWidth(2,80)

        self.widget.searchLineEdit.textChanged.connect(self.filter_input)

        self.setWindowIcon(QtGui.QIcon(":/icons/icon.png"))


    def filter_input(self):
        if len(self.widget.searchLineEdit.text()) == 0:
            self.widget.tableWidget.setRowCount(0)

        else:
            self.mydb = db.Database().connect_db()
            self.cursor = self.mydb.cursor()
            self.widget.tableWidget.setRowCount(0)

            searchText = self.widget.searchLineEdit.text()

            sql = """SELECT item.item_name, stock_qty FROM "item"\
                INNER JOIN "stock" ON "item".item_name = "stock".item_name WHERE item.item_name ILIKE '%{}%'""".format(searchText)

            
            try:
                self.cursor.execute(sql)
                ret = self.cursor.fetchall()
                g = 0
                r = len(ret)
                self.widget.tableWidget.setRowCount(r)

                for row in ret:
                    name = row[0]
                    qty = row[1]
                    
                    btn = DeleteBtn(self.widget.tableWidget,self,self.user)
                    

                    self.widget.tableWidget.setItem(g,0,QtWidgets.QTableWidgetItem(name))
                    self.widget.tableWidget.setItem(g,1,QtWidgets.QTableWidgetItem(str(qty)))
                    self.widget.tableWidget.setCellWidget(g,2,btn)
                    g+=1

            except Exception as aa:
                print('>> Error at stock :: ',str(aa))


    