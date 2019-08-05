from PyQt5 import QtWidgets, QtCore, QtGui, uic

from msale.database import db

from msale.icons import resources

class SellToolWidget(QtWidgets.QWidget):
    def __init__(self,daddy,table):
        QtWidgets.QWidget.__init__(self)
        self.daddy = daddy
        self.table = table
        
        self.widget = uic.loadUi("msale/forms/qtychangewidget.ui",self)

        self.widget.addqtyBtn.setIcon(QtGui.QIcon(":/icons/add_g.png"))
        self.widget.deleterowBtn.setIcon(QtGui.QIcon(":/icons/x_r.png"))

        self.widget.addqtyBtn.clicked.connect(self.edit_added_row)
        self.widget.deleterowBtn.clicked.connect(self.remove_added_row)
    
    def remove_added_row(self):
        # function to remove a row from the cart
        sender = self.sender()
        row = self.table.indexAt(sender.parent().pos()).row()
        self.table.removeRow(row)
        self.daddy.reload_totals()

    def edit_added_row(self):

        # function to edit quantity added to the table
        # get quantity from database of the row item and compare it to entered quantity
        
        self.mydb = db.Database().connect_db()
        self.cursor = self.mydb.cursor()

        sender = self.sender()
        row = self.table.indexAt(sender.parent().pos()).row()
        c_qty =  self.table.item(row,2).text()
        cost = float(self.table.item(row,1).text())

        x = QtWidgets.QInputDialog()
        x.setStyleSheet("QLabel{},QPushButton{border:1px solid grey;},\
            QSpinBox{min-height:35px;}")

        i, okPressed = x.getInt(self,"Enter New Quantity","Quantity",int(c_qty),1,1000)
        if okPressed:
            sql_qty = """SELECT stock_qty FROM "stock" WHERE item_name = '{}'""".format(self.table.item(row,0).text())
            try:
                self.cursor.execute(sql_qty)
                ret = self.cursor.fetchall()
                _qty = ret[0][0]

                if len(ret) != 0:
                    __qty = 0

                    _item_name = self.table.item(row,0).text()
                    for x in range(self.table.rowCount()):
                        if _item_name == self.table.item(x,0).text():
                            __qty += int(self.table.item(x,2).text())
                    if _qty >= (i + __qty):
                        self.table.setItem(row,2,QtWidgets.QTableWidgetItem(str(i)))
                        self.table.setItem(row,4,QtWidgets.QTableWidgetItem(str(i*cost)))
                        self.daddy.reload_totals()
                    else:
                        print("Operation Cancelled!\nQuantity to be added exceeds item's stock quantity")
                else:
                    print("Fetching stock quantity of the item failed\n Check if item's stock details exist.")

            except Exception as e1:
                print(str(e1))
        
