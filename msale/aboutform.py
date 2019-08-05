from PyQt5 import QtCore, QtGui, QtWidgets, uic
from msale.icons import resources
import webbrowser

class AboutForm(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.widget = uic.loadUi("msale/forms/aboutform.ui",self)

        self.widget.pyBtn.setIcon(QtGui.QIcon(":/icons/py_w.png"))
        self.widget.pyqtBtn.setIcon(QtGui.QIcon(":/icons/pyqt_w.png"))
        self.widget.psqlBtn.setIcon(QtGui.QIcon(":/icons/psql_w.png"))
        self.widget.icons8Btn.setIcon(QtGui.QIcon(":/icons/icons8_w.png"))

        self.widget.pyBtn.clicked.connect(self.open_py)
        self.widget.pyqtBtn.clicked.connect(self.open_pyqt5)
        self.widget.psqlBtn.clicked.connect(self.open_psql)
        self.widget.icons8Btn.clicked.connect(self.open_icons8)

    def open_py(self):
        # open python.org

        webbrowser.open_new_tab("https://www.python.org/")

    def open_pyqt5(self):
        # Open pyqt5 website

        webbrowser.open_new_tab("https://www.riverbankcomputing.com/software/pyqt/intro")

    def open_psql(self):
        # Open postgresql

        webbrowser.open_new_tab("https://www.postgresql.org/")

    def open_icons8(self):
        #from bs4 import BeautifulSoup
        #page = urlopen()
        #soup =  BeautifulSoup(page, "html.parser" ).encode('UTF-8')
        #print (soup)

        #Open icons8.com

        webbrowser.open_new_tab("https://icons8.com/")

'''
IN NO EVENT SHALL THE UNIVERSITY OF CALIFORNIA BE LIABLE TO ANY PARTY FOR DIRECT, 
INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF THE UNIVERSITY OF CALIFORNIA HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

THE UNIVERSITY OF CALIFORNIA SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, 
BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A 
PARTICULAR PURPOSE. THE SOFTWARE PROVIDED HEREUNDER IS ON AN "AS IS" BASIS, AND 
THE UNIVERSITY OF CALIFORNIA HAS NO OBLIGATIONS TO PROVIDE MAINTENANCE, SUPPORT,
 UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
'''