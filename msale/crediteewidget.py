from PyQt5 import QtWidgets, QtCore, QtGui, uic

from msale.database import db
import pendulum

class CrediteeWidget(QtWidgets.QWidget):
    def __init__(self,daddy,name,mobile):
        QtWidgets.QWidget.__init__(self)
        self.daddy = daddy
        
        self.widget = uic.loadUi("msale/forms/crediteewidget.ui",self)

        self.widget.nameLbl.setText(name)
        self.widget.mobileBtn.setText("0"+str(mobile))

        self.db = db.Database().connect_db()
        self.cursor = self.db.cursor()

        self.widget.opendetailsBtn.clicked.connect(self.openDetails)

    def openDetails(self):
        self.daddy.open_user("0"+self.widget.mobileBtn.text())