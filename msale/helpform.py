from PyQt5 import QtWidgets, QtCore, QtGui, uic

from msale.icons import resources

import webbrowser

class HelpForm(QtWidgets.QWidget):
    def __init__(self):

        """
        Help Window for the MS Point of sale software
        //Initialize dynamically the ui
        //set the icons not loaded dynamically by the UiLoader
        //Setup slot functions for the signals sent by the dynamic Ui
        """
        QtWidgets.QWidget.__init__(self)
        
        self.widget = uic.loadUi("msale/forms/helpform.ui",self)

        # Setup Icons
        self.widget.githubBtn.setIcon(QtGui.QIcon(":/icons/github_w.png"))
        self.widget.docsBtn.setIcon(QtGui.QIcon(":/icons/documentation_w.png"))
        self.widget.emailBtn.setIcon(QtGui.QIcon(":/icons/email_w.png"))
        self.widget.tripBtn.setIcon(QtGui.QIcon(":/icons/overview_w.png"))

        self.widget.githubBtn.clicked.connect(self.view_sourcecode)

    def view_sourcecode(self):
        webbrowser.open_new_tab("https://github.com/lalan-ke/Point-Of-Sale-PyQt-PySide")