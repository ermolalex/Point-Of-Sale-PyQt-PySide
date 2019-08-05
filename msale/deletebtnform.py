from PyQt5 import QtWidgets, QtCore, QtGui, uic

from msale.database import db

from msale.icons import resources


class DeleteBtn(QtWidgets.QWidget):
    def __init__(self,table,daddy,user):
        QtWidgets.QWidget.__init__(self)

        self.table = table
        self.daddy = daddy
        self.user = user

        self.widget = uic.loadUi("msale/forms/delbtnform.ui",self)
        self.widget.deleteBtn.setIcon(QtGui.QIcon(":/icons/delete_r.png"))
        self.widget.deleteBtn.clicked.connect(self.delete_item)

    def delete_item(self):
        self.db = db.Database().connect_db()
        self.cursor = self.db.cursor()

        sender = self.sender()
        index = self.table.indexAt(sender.parent().pos())
        row = index.row()
        
        name = self.table.item(row,0).text()
        sql = """DELETE from "stock" WHERE item_name = '{}'""".format(name)
        sql1 = """DELETE from "item" WHERE item_name = '{}'""".format(name)


        try:
            self.cursor.execute(sql)
            self.cursor.execute(sql1)
            if self.user[2] == 3:
                self.db.commit()
                self.message('Successfully Deleted the item','')
                self.daddy.filter_input()
                self.daddy.close()
            else:
                self.db.rollback()
                self.message('Failed to delete item, this action can be done only by Database Administrators, \nContact your administrator for assistance.','Error')
                self.daddy.close()

        except Exception as a:
            m = 'Could not complete delete operation\n'+str(a)
            self.message(m,'Error!')

        self.db.close()

    def message(self,m,n):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle(n)
        msg.setStyleSheet("*{background-color:rgb(54,54,54);color:white;font: 12pt \"MS Shell Dlg 2\";}\
            QPushButton{border-radius:1px;border:1px solid grey;min-height:34px;\
                min-width:50px;}\
                QPushButton:hover{border:2px solid white;}\
                    QPushButton:pressed{border:3px solid orange;}")
        msg.setText(m)
        msg.exec_()

