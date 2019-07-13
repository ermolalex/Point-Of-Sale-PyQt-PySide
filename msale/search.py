from PyQt5 import QtWidgets, QtCore, QtGui, uic

#from msale.database import db

class Ui_Search(QtWidgets.QWidget):
    def __init__(self):

        """
        Search window for the MS Point of sale software
        //Initialize dynamically the ui
        //set the icons not loaded dynamically by the UiLoader
        //Setup slot functions for the signals sent by the dynamic Ui
        """
        QtWidgets.QWidget.__init__(self)
        self.setWindowFlags(QtCore.Qt.Window|QtCore.Qt.CustomizeWindowHint)

        #Load Ui
        self.widget = uic.loadUi("msale/forms/search.ui",self)

        #Insert Icons
        self.widget.SearchBtn.setIcon(QtGui.QIcon("msale/icons/search_more_64_white.png"))
        self.widget.CloseThis.setIcon(QtGui.QIcon("msale/icons/close_x_48px_white.png"))
        self.widget.AddToTable.setIcon(QtGui.QIcon("msale/icons/add_shopping_cart_white.png"))
        self.widget.SearchTable.setColumnWidth(0,60)
        #Database
        #self.mydb = db.Database().connect_db()
        #self.cursor = self.mydb.cursor()

    @QtCore.pyqtSlot()
    def search(self):
        #Get text from search lineedit box and do a search in the database
        pass
        '''
        searchText = self.widget.SearchBox.text()
        if len(searchText) == 0:
            self.widget.SearchTable.setRowCount(0)

        else:
            # clear tables
            self.widget.SearchTable.setRowCount(0)

            sql = """SELECT item.item_name, item_sp, id, stock_qty FROM "item" INNER JOIN "stock" ON 
            "item".item_name = "stock".item_name WHERE item.item_name ILIKE '%{}%'""".format(searchText)

            try:
                self.cursor.execute(sql)
                ret = self.cursor.fetchall()

                for rows in ret:
                    name = str(rows[0])
                    sp = str(rows[1])
                    id = str(rows[2])
                    qty = str(rows[3])

                    x = self.widget.SearchTable.rowCount()
                    self.widget.SearchTable.insertRow(x)

                    self.widget.SearchTable.setItem(x,0,QtWidgets.QTableWidgetItem(id))
                    self.widget.SearchTable.setItem(x,1,QtWidgets.QTableWidgetItem(name))
                    self.widget.SearchTable.setItem(x,2,QtWidgets.QTableWidgetItem(qty))
                    self.widget.SearchTable.setItem(x,3,QtWidgets.QTableWidgetItem(sp))

            except Exception as e1:
                print(e1)'''

    @QtCore.pyqtSlot()
    def advance_itemSearch(self):
        pass

    @QtCore.pyqtSlot()
    def advanced_itemSearch(self):
        pass


    @QtCore.pyqtSlot()
    def closeWindow(self):
        self.widget.close()

    @QtCore.pyqtSlot()
    def add_toTable(self):
        pass